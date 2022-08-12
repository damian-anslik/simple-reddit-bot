import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser


def get_access_token(config: ConfigParser) -> dict[str, str]:
    auth_config = config['AUTH']
    auth_url = auth_config['auth_url']
    client_auth = HTTPBasicAuth(auth_config['client_id'], auth_config['client_secret'])
    headers = {"User-Agent": get_user_agent(config)}
    post_data = {
        'grant_type': 'password',
        'username': auth_config['username'],
        'password': auth_config['password'],
    }
    response = requests.post(auth_url, auth=client_auth, data=post_data, headers=headers)
    if not response.ok:
        return response.raise_for_status()
    return response.json()

def get_user_agent(config: ConfigParser) -> str:
    default_config = config['DEFAULT']
    auth_config = config['AUTH']
    return "{app_name}/{app_version} by {username}".format_map({
        "app_name": default_config['app_name'],
        "app_version": default_config['app_version'],
        "username": auth_config['username']
    })

def create_request_header(access_token: str, user_agent: str) -> dict[str, str]:
    return {
        "User-Agent": user_agent,
        "Authorization": f"bearer {access_token}"
    }