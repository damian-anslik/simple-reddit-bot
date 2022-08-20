# A simple Reddit bot

A Python library that makes it easy to build Reddit bots. The library provides a simple wrapper around Reddit's REST API. 

## How to create a bot?

1. Register your app with Reddit. 
    - Navigate to https://www.reddit.com/prefs/apps 
    - Scroll down to the bottom of the page and click on 'Create an app'
    - Enter a name for the app 
    - Select the script option 
    - You can enter http://www.example.com/unused/redirect/uri for the redirect URL

    Note the client ID (located in the upper right corner, under the name of the app), the client secret and app name

2. Create a config.ini file in the root of your project. The configuration file should be of the following format:

    ```
    [DEFAULT]
    app_name = the-name-of-your-app-as-registered-with-reddit
    app_version = the-version-of-your-app
    timeout = time-out-between-each-iteration-in-seconds

    [AUTH]
    auth_url = https://www.reddit.com/api/v1/access_token
    client_id = your-apps-client-id-as-registered-with-reddit
    client_secret = your-apps-client-id-as-registered-with-reddit
    username = the-username-associated-with-the-bot
    password = the-password-for-the-bot-account

    [ACCESS_TOKEN]

    [LOGGING]
    log_name = client
    log_level = DEBUG
    log_dir = logs
    ```

3. Create a client class that inherits from the RedditClient app.

4. Add a `main` method in the client class. This method contains the actions your bot should undertake on each iteration. 

5. Call the run method on the client.

## What is the rate limit for requests?

The Reddit API has a rate limit of 60 requests per minute. 