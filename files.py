import os
from dependency import Component


def get_work_folder() -> str:
    home = os.path.expanduser("~")
    work_folder = os.path.join(home, '.noticeCreator')
    if not os.path.exists(work_folder):
        os.mkdir(work_folder)
    return work_folder


def get_cache_folder() -> str:
    cache_folder = os.path.join(get_work_folder(), 'cache')
    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)
    return cache_folder


def get_overwrite_folder() -> str:
    overwrite_folder = os.path.join(get_work_folder(), 'overwrite')
    if not os.path.exists(overwrite_folder):
        os.mkdir(overwrite_folder)
    return overwrite_folder


def make_file_name(component: Component) -> str:
    return f'{component.type}_{component.provider}_{component.namespace}_{component.name}_{component.revision}.json'\
        .replace('/', '_')


def is_component_cached(component: Component) -> bool:
    return os.path.exists(os.path.join(get_cache_folder(), make_file_name(component)))


def is_component_overwritten(component: Component) -> bool:
    return os.path.exists(os.path.join(get_overwrite_folder(), make_file_name(component)))


def write_component_to_cache(component: Component, data: str):
    with open(os.path.join(get_cache_folder(), make_file_name(component)), 'w') as file:
        file.write(data)


def write_component_to_overwritten(component: Component, data: str):
    with open(os.path.join(get_overwrite_folder(), make_file_name(component)), 'w') as file:
        file.write(data)


def read_file(name: str) -> str:
    with open(name, 'r') as file:
        return file.read()


def read_component(component: Component) -> str:
    if is_component_overwritten(component):
        return read_file(os.path.join(get_overwrite_folder(), make_file_name(component)))
    return read_file(os.path.join(get_cache_folder(), make_file_name(component)))
