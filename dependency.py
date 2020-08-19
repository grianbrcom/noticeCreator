from dataclasses import dataclass
from typing import List
import json


@dataclass
class Component:
    type: str
    provider: str
    namespace: str
    name: str
    revision: str

    def to_string(self) -> str:
        return ':'.join([self.type, self.provider, self.namespace, self.name, self.revision])

    @staticmethod
    def from_string(string: str):
        type, provider, namespace, name, revision = string.split(':')
        return Component(type, provider, namespace, name, revision)


@dataclass
class LibDescription:
    name: str
    version: str
    license: str


def convert_maven(data) -> List[Component]:
    result = []
    for line in data.split('\n'):
        line = line.strip()
        if line:
            namespace, name, _, revision, dependency_type = line.split(':')
            if dependency_type != 'compile':
                continue
            result.append(Component('maven', 'mavencentral', namespace, name, revision))
    return result


def convert_node(data) -> List[Component]:
    result = []
    data = json.loads(data)
    for lib, description in data['dependencies'].items():
        if description.get('dev', False):
            continue
        result.append(Component('npm', 'npmjs', '-', lib, description['version']))
    return result


def construct_lib_description(data: str) -> LibDescription:
    data = json.loads(data)
    if 'coordinates' in data:
        name = data['coordinates']['name']
        version = data['coordinates']['revision']
    else:
        name = data['described']['sourceLocation']['name']
        version = data['described']['sourceLocation']['revision']
    license = data['licensed']['declared']
    return LibDescription(name, version, license)
