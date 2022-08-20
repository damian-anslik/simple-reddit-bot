from configparser import ConfigParser
from time import sleep, time, strftime
from requests import get, post
from requests.auth import HTTPBasicAuth
from os import path, mkdir
import logging


class RedditClient:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config = ConfigParser()
        self.config.read(config_file)
        self.__configure_logging()
        self.__get_user_agent()
        self.__get_access_token()
        self.__create_request_header()
        self.__set_timeout()
    
    def __configure_logging(self):
        log_dir = self.config.get('LOGGING', 'log_dir', fallback='logs')
        log_name = self.config.get('LOGGING', 'log_name', fallback='client')
        path.exists(log_dir) or mkdir(log_dir)
        log_fp = f'{log_dir}/{log_name}-{strftime("%Y%m%d-%H%M%S")}.log'
        logging.basicConfig(
            level=self.config.get('LOGGING', 'log_level', fallback='INFO'),
            filename=log_fp,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filemode='w',
        )

    def __get_access_token(self):
        self.access_token = self.config.get('ACCESS_TOKEN', 'access_token', fallback=None)
        self.access_token_expiry_time = self.config.get('ACCESS_TOKEN', 'access_token_expiry_time', fallback=None)
        if not self.access_token or not self.__is_access_token_valid(self.access_token_expiry_time):
            access_token_data = self.__request_new_access_token()
            self.access_token = access_token_data['access_token']
            self.access_token_expiry_time = access_token_data['expires_in'] + int(time())
            self.config.set('ACCESS_TOKEN', 'access_token', self.access_token)
            self.config.set('ACCESS_TOKEN', 'access_token_expiry_time', str(self.access_token_expiry_time))
            self.__save_config()
    
    def __request_new_access_token(self) -> dict[str, str]:
        client_id = self.config.get('AUTH', 'client_id')
        client_secret = self.config.get('AUTH', 'client_secret')
        username = self.config.get('AUTH', 'username')
        password = self.config.get('AUTH', 'password')
        auth_url = self.config.get('AUTH', 'auth_url')
        headers = {"User-Agent": self.user_agent}
        client_auth = HTTPBasicAuth(client_id, client_secret)
        post_data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
        }
        response = post(auth_url, auth=client_auth, data=post_data, headers=headers)
        if not response.ok:
            return response.raise_for_status()
        return response.json()

    def __is_access_token_valid(self, access_token_expiry_time: str) -> bool:
        return int(access_token_expiry_time) > int(time())

    def __save_config(self):
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

    def __get_user_agent(self):
        app_name = self.config.get('DEFAULT', 'app_name')
        app_version = self.config.get('DEFAULT', 'app_version')
        username = self.config.get('AUTH', 'username')
        self.user_agent = "{app_name}/{app_version} by {username}".format_map({
            "app_name": app_name,
            "app_version": app_version,
            "username": username
        })

    def __create_request_header(self):
        self.headers = {
            "User-Agent": self.user_agent,
            "Authorization": f"bearer {self.access_token}"
        }

    def __set_timeout(self):
        self.timeout = self.config.getint('DEFAULT', 'timeout', fallback=60)

    def get_recent_submissions(self, subreddit: str, before: str = None, after: str = None, limit: int = 100) -> list[dict[str, str]]:
        request_data = {
            'before': before,
            'after': after,
            'limit': limit,
        }
        response = get(f'https://oauth.reddit.com/r/{subreddit}/new', headers=self.headers, params=request_data)
        if not response.ok:
            raise Exception(f'Error getting recent submissions from {subreddit}: {response.text}')
        return response.json()['data']['children']
    
    def request_user_info(self) -> dict[str, str]:
        response = get("https://oauth.reddit.com/api/v1/me", headers=self.headers)
        if not response.ok:
            return response.raise_for_status()
        return response.json()

    def mark_messages_as_read(self, message_id_list: list[str]) -> dict[str, str]:
        request_data = {"id": ",".join(message_id_list)}
        response = post("https://oauth.reddit.com/api/read_message", headers=self.headers, data=request_data)
        if not response.ok:
            response.raise_for_status()

    def reply_to_message(self, message_id: str, message: str) -> dict[str, str]:
        response = post(f"https://oauth.reddit.com/api/comment?thing_id={message_id}&text={message}", headers=self.headers)
        if not response.ok:
            return response.raise_for_status()
        return response.json()

    def request_unread_messages(self) -> dict[str, str]:
        response = get("https://oauth.reddit.com/message/unread", headers=self.headers)
        if not response.ok:
            return response.raise_for_status()
        return response.json()

    def get_user_comments(self, username: str = None, after: str = None, before: str = None, limit: int = 100) -> list[dict[str, str]]:
        """ 
        Get a list of comments made by the user. Leave username blank to get comments made by the bot.
        """
        if not username:
            username = self.config.get('AUTH', 'username')
        request_data = {
            'before': before,
            'after': after,
            'limit': limit,
        }
        response = get(f"https://oauth.reddit.com/user/{username}/comments", params=request_data, headers=self.headers)
        logging.debug(f"Requested comments made by {username}: url={response.url}, data={request_data}, response={response.status_code}, response_length={len(response.text)}")
        if not response.ok:
            return response.raise_for_status()
        return response.json()['data']['children']
    
    def get_user_submissions(self, username: str = None, after: str = None, before: str = None, limit: int = 100) -> list[dict[str, str]]:
        """ 
        Get a list of submissions made by the user. Leave username blank to get comments made by the bot.
        """
        if not username:
            username = self.config.get('AUTH', 'username')
        request_data = {
            'before': before,
            'after': after,
            'limit': limit,
        }
        response = get(f"https://oauth.reddit.com/user/{username}/submitted", params=request_data, headers=self.headers)
        logging.debug(f"Requested submissions made by {username}: url={response.url}, data={request_data}, response={response.status_code}, response_length={len(response.text)}")
        if not response.ok:
            return response.raise_for_status()
        return response.json()['data']['children']

    def run(self) -> None:
        while self.__is_access_token_valid(self.access_token_expiry_time):
            self.main()
            sleep(self.timeout)
        self.__get_access_token()
        self.__create_request_header()
        self.run()

    def main(self):
        pass

    def stop(self):
        raise SystemExit