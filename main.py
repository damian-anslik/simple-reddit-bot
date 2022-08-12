import inspect
import requests
from auth import get_access_token, get_user_agent, create_request_header
from time import strftime, gmtime, time, sleep
from utils import is_valid_ticker, is_access_token_valid
from configparser import ConfigParser


def request_bot_data(request_headers: dict[str, str]) -> dict[str, str]:
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=request_headers)
    if not response.ok:
        return response.raise_for_status()
    return response.json()

def request_unread_messages(request_headers: dict[str, str]) -> dict[str, str]:
    response = requests.get("https://oauth.reddit.com/message/unread", headers=request_headers)
    if not response.ok:
        return response.raise_for_status()
    return response.json()

def post_reply(request_headers: dict[str, str], message_id: str, reply: str) -> dict[str, str]:
    response = requests.post(f"https://oauth.reddit.com/api/comment?thing_id={message_id}&text={reply}", headers=request_headers)
    if not response.ok:
        return response.raise_for_status()
    return response.json()

def read_messages(request_headers: dict[str, str], messages: list[str]) -> dict[str, str]:
    request_data = {"id": ",".join(messages)}
    response = requests.post("https://oauth.reddit.com/api/read_message", headers=request_headers, data=request_data)
    if not response.ok:
        response.raise_for_status()

def main(config_file: str) -> None:
    config = ConfigParser()
    config.read(config_file)
    access_token = config.get('ACCESS_TOKEN', 'access_token', fallback=None)
    access_token_expiry_time = config.get('ACCESS_TOKEN', 'access_token_expiry_time', fallback=None)
    if not access_token or not is_access_token_valid(access_token_expiry_time):
        access_token_data = get_access_token(config)
        access_token_expires_in = access_token_data['expires_in']
        access_token = access_token_data["access_token"]
        access_token_expiry_time = strftime("%Y-%m-%d %H:%M:%S", gmtime(time() + access_token_expires_in))
        with open("config.ini", "w") as config_file:
            config["ACCESS_TOKEN"]["ACCESS_TOKEN"] = access_token
            config["ACCESS_TOKEN"]["ACCESS_TOKEN_EXPIRY_TIME"] = access_token_expiry_time
            config.write(config_file)
    user_agent = get_user_agent(config)
    request_headers = create_request_header(access_token, user_agent)
    SLEEP_TIME = config.getint('DEFAULT', 'sleep_time', 10)
    # Continue to receive messages until the access token is valid or until the bot is stopped
    while is_access_token_valid(access_token_expiry_time):
        sleep(SLEEP_TIME) # Sleep in between requests to respect rate limiting
        unread_messages = request_unread_messages(request_headers)
        unread_message_list = unread_messages["data"]["children"]
        if len(unread_message_list) == 0:
            continue
        parsed_message_ids = []
        for message in unread_message_list:
            # Parse the unread messages, if messages are not mentions, or the message is not a valid ticker symbol, ignore the message
            # If the message is a valid ticker symbol, reply to the message with data for the requested ticker
            message_data = message["data"]
            message_id = message_data["name"]
            message_body = message_data["body"]
            message_type = message_data["type"]
            parsed_message_ids.append(message_id)
            if message_type != "username_mention":
                continue
            message_fields = message_body.split()
            if len(message_fields) != 2:
                continue
            _, ticker = message_fields
            if not is_valid_ticker(ticker):
                continue
            # Cleandoc to remove leading and trailing whitespace from each line of the string
            response_message = inspect.cleandoc(f"""
            Hello! Here is your requested data for {ticker}:

            - Test item 1
            - Test item 2

            Response time: {strftime("%Y-%m-%d %H:%M:%S")}
            """)
            post_reply(request_headers, message_id, response_message)
        read_messages(request_headers, parsed_message_ids) # Mark the messages as read so they are not processed again
    main()

if __name__ == "__main__":
    CONFIG = "config.ini"
    main(CONFIG)