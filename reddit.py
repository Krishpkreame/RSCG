import praw
import os


class RedditAPI:
    def __init__(self, subreddit):
        self.reddit = praw.Reddit(
            client_id=os.environ['REDDIT_CLIENT_ID'],
            client_secret=os.environ['REDDIT_CLIENT_SECRET'],
            user_agent='RSCG (by u/RedditThrowaway4723)',
            username=os.environ['REDDIT_USERNAME'],
            password=os.environ['REDDIT_PASSWORD'])
        self.subreddit = self.reddit.subreddit(subreddit)

    def get_from_url(self, url):
        return self.reddit.submission(url=url)
