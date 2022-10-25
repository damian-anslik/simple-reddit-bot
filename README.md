# A simple Reddit bot

A Python library that makes it easy to build Reddit bots. The library provides a simple wrapper around Reddit's REST API. 

## Getting Started

1. Register your bot with Reddit. 
    - Navigate to https://www.reddit.com/prefs/apps 
    - Scroll down to the bottom of the page and click on 'Create an app'
    - Enter a name for the app 
    - Select the script option 
    - You can enter http://www.example.com/unused/redirect/uri for the redirect URL

    Note the client ID (located in the upper right corner, under the name of the app), the client secret and app name

2. Create a **config.ini** file in the root of your project. This file configures your bot, and the data contained within it are used to prepare requests and retrieve authorization. It should be of the following format:

    ```
    [DEFAULT]
    app_name = the-name-of-your-app-as-registered-with-reddit
    app_version = the-version-of-your-app
    timeout = time-out-between-each-iteration-in-seconds

    [AUTH]
    auth_url = https://www.reddit.com/api/v1/access_token
    client_id = your-apps-client-id-as-registered-with-reddit
    client_secret = your-apps-client-secret-as-registered-with-reddit
    username = the-username-associated-with-the-bot
    password = the-password-for-the-bot-account

    [ACCESS_TOKEN]

    [LOGGING]
    log_name = client
    log_level = DEBUG
    log_dir = logs
    ```

3. Create a client class that inherits from the `RedditClient` class.

4. Implement the `main` method in the client class. This method contains the actions your bot should undertake on each iteration, for example you might want to get a list of unread messages, or retrieve a list of recent submissions from a particular subreddit.

5. Call the client's `run` method. The `run` method continously call the `main` method. It's also responsible for checking if your current access token is still valid, and if not, requests a new one from the OAuth service.

6. To stop the bot call the `stop` method from within `main`.

## What is the rate limit for requests?

The Reddit API has a rate limit of 60 requests per minute. 