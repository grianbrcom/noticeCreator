import urllib.error
import urllib.request
from socket import timeout
from dependency import Component


def download_definition(component: Component) -> str:
    headers = {'accept': '*/*', 'User-Agent': 'curl/7.71.1'}
    url = (f'https://api.clearlydefined.io'
           f'/definitions/{component.type}/{component.provider}/{component.namespace}'
           f'/{component.name}/{component.revision}')
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError:
        return ""
    except timeout:
        return ""
