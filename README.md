# Creating a Reddit stock bot using the Reddit API and TWS API

In this article I will create a Reddit stock bot using the official Reddit REST API and Interactive Brokers TWS API.
The bot works in a similar fashion to other bots currently found on Reddit. A user interested in market data for a particular 
stock can call the bot in a comment along with the ticker symbol for the instrument. 
The mention is intercepted by the bot along with the requested ticker.
Using TWS API the bot requests stock data for the particular instrument. The bot then uses the data to send a response 
to the user.

1. # Sign up for a free Reddit account

    In order to create a bot, we'll need to create a Reddit account. Go ahead, choose a name suitable for the bot you're developing.
    In this case, we will call the bot, market-data-bot.

2. # Navigate to the Apps page

    The apps page can be found here: https://www.reddit.com/prefs/apps. On the bottom you will need to press the 'Create a new app' button.
    Enter a name for the application, this will usually be similar to what your bot username is. 

3. # Request an OAuth token

    https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example

4. # Create the request headers

5. # Setting up the required endpoints

6. # Test the bots reading / response capabilities