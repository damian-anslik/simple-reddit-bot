from examples import SubredditDownloadBot

if __name__ == '__main__':
    bot = SubredditDownloadBot('config.ini', 'ireland')
    bot.run()