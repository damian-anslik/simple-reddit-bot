from time import sleep
from reddit_bot import RedditClient
from tinydb import TinyDB, where

class UserDownloadBot(RedditClient):
    def __init__(self, config_file: str, username: str) -> None:
        super().__init__(config_file)
        self.last_thing_name = None
        self.num_results = 0
        self.username = username

    def get_all_user_comments(self) -> None:
        self.db = TinyDB(f'comments-{self.username}.json', indent=4)
        user_comments = self.get_user_comments(self.username, after=self.last_thing_name, limit=100)
        if not user_comments:
            self.stop()
        for comment in user_comments:
            comment_data = comment['data']
            self.db.upsert(comment_data, where('name')==comment_data['name'])
        self.last_thing_name = user_comments[-1]['data']['name']
        self.num_results += len(user_comments)

    def get_all_user_submissions(self) -> None:
        self.db = TinyDB(f'submissions-{self.username}.json', indent=4)
        user_submissions = self.get_user_submissions(self.username, after=self.last_thing_name, limit=100)
        if not user_submissions:
            self.stop()
        for submission in user_submissions:
            submission_data = submission['data']
            self.db.upsert(submission_data, where('name')==submission_data['name'])
        self.last_thing_name = user_submissions[-1]['data']['name']
        self.num_results += len(user_submissions)

    def main(self):
        self.get_all_user_comments()

class SubredditDownloadBot(RedditClient):
    def __init__(self, config_file: str, subreddit: str, limit: int = 100) -> None:
        super().__init__(config_file)
        self.last_thing_name = None
        self.subreddit = subreddit
        self.num_results = 0
        self.max_num_pages = 2
        self.limit = limit
        self.max_results = self.max_num_pages * self.limit

    def get_subreddit_submissions(self) -> None:
        recent_submissions = self.get_recent_submissions(self.subreddit, after=self.last_thing_name, limit=self.limit)
        self.db = TinyDB(f'submissions-{self.subreddit}.json', indent=4)
        for submission in recent_submissions:
            submission_data = submission['data']
            self.db.upsert(submission_data, where('name')==submission_data['name'])
        self.last_thing_name = recent_submissions[-1]['data']['name']
        self.num_results += len(recent_submissions)
        if self.num_results >= self.max_results:
            self.num_results = 0
            self.last_thing_name = None
            sleep(60)

    def main(self):
        self.get_subreddit_submissions()

if __name__ == '__main__':
    subreddit_bot = SubredditDownloadBot('config.ini', 'ireland')
    subreddit_bot.run()