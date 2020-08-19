import argparse
from files import read_file, is_component_cached, write_component_to_cache, read_component, \
    write_component_to_overwritten
from dependency import convert_maven, construct_lib_description, Component, convert_node
from clearlydefined import download_definition
import logging
import json
from npmjs import get_license


def make_notice(args):
    logging.info("Making notice")
    components = []
    if args.maven:
        components.extend(convert_maven(read_file(args.maven)))
    if args.node:
        components.extend(convert_node(read_file(args.node)))
    logging.info("Update the cache")
    for component in components:
        if not is_component_cached(component):
            write_component_to_cache(component, download_definition(component))
    logging.info("Collect licenses")
    lib_description = []
    for component in components:
        data = read_component(component)
        if data:
            try:
                description = construct_lib_description(data)
            except KeyError:
                logging.error(f'package {component.to_string()} have bad representation')
                continue
            if description.license in ['OTHER', 'NOASSERTION']:
                logging.error(f'package {component.to_string()} have not defined license')
            lib_description.append(construct_lib_description(data))
        else:
            logging.error(f'component {component.to_string()} is not defined')
    with open('NOTICE', 'w') as notice:
        notice.write('## Third-party Content\n')
        for lib in sorted(lib_description, key=lambda item: item.name):
            notice.write(f'\n{lib.name} ({lib.version})\n\n * License: {lib.license}\n')


def overwrite(args):
    component = Component.from_string(args.library)

    definition = {
        'described': {
            'sourceLocation': {
                'name': component.name,
                'revision': component.revision
            }},
        'licensed': {
            'declared': args.license
        }
    }
    write_component_to_overwritten(component, json.dumps(definition))


def overwrite_from_npmjs(args):
    component = Component.from_string(args.library)
    license = get_license(component)
    print(f'License: {license}')
    definition = {
        'described': {
            'sourceLocation': {
                'name': component.name,
                'revision': component.revision
            }},
        'licensed': {
            'declared': license
        }
    }
    write_component_to_overwritten(component, json.dumps(definition))


def no_subcommand(args):
    logging.error("You must specify one of valid commands.")


def create_argparse():
    parser = argparse.ArgumentParser(description="Process project dependencies for assemble NOTICE file with libraries "
                                                 "and licenses. This tool keeps cache in '.noticeCreator' folder "
                                                 "inside user directory.")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.set_defaults(func=no_subcommand)
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='you must specify one of the valid commands',
                                       help='sub-command help')
    parser_notes = subparsers.add_parser('notice', help='processing dependencies file and generate NOTICE')
    parser_notes.add_argument('-m', '--maven', help='specify file generated by command: '
                                                    'mvn dependency:list | grep -Poh "\\S+:(system|provided|compile)" '
                                                    '| sort | uniq > maven.deps')
    parser_notes.add_argument('-n', '--node', help='specify package-lock.json file')
    parser_notes.set_defaults(func=make_notice)
    parser_overwrite = subparsers.add_parser('overwrite', help='overwrite local cache to manually specify the license')
    parser_overwrite.add_argument('library')
    parser_overwrite.add_argument('license')
    parser_overwrite.set_defaults(func=overwrite)
    parser_overwrite_npmjs = subparsers.add_parser('overwrite_npmjs', help='overwrite local cache with license taken '
                                                                           'from npmjs repo')
    parser_overwrite_npmjs.add_argument('library')
    parser_overwrite_npmjs.set_defaults(func=overwrite_from_npmjs)
    return parser


if __name__ == '__main__':
    args = create_argparse().parse_args()
    log_format = '%(levelname)s - %(message)s'
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format=log_format)
    else:
        logging.basicConfig(format=log_format)
    args.func(args)
