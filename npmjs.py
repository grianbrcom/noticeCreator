from dependency import Component
import urllib.request
import json


def get_license(component: Component) -> str:
    url = f'https://registry.npmjs.org/{component.name}/{component.revision}'
    headers = {'accept': '*/*', 'User-Agent': 'curl/7.71.1'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read())['license']
