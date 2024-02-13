from datetime import datetime
import praw
import os
from ftfy import ftfy


class RedditAPI:
    def __init__(self, subreddit):
        """
        Initializes the RedditAPI class.

        Parameters:
        - subreddit (str): The name of the subreddit.

        Raises:
        - ValueError: If any of the required environment variables are not set.
        """
        # Raise error if the environment variables are not set
        if not os.environ['REDDIT_CLIENT_ID']:
            raise ValueError("REDDIT_CLIENT_ID env var not set")
        if not os.environ['REDDIT_CLIENT_SECRET']:
            raise ValueError("REDDIT_CLIENT_SECRET env var not set")
        if not os.environ['REDDIT_USERNAME']:
            raise ValueError("REDDIT_USERNAME env var not set")
        if not os.environ['REDDIT_PASSWORD']:
            raise ValueError("REDDIT_PASSWORD env var not set")
        if not subreddit:
            raise ValueError("Subreddit not set")

        # Create the Reddit instance
        self.reddit = praw.Reddit(
            client_id=os.environ['REDDIT_CLIENT_ID'],
            client_secret=os.environ['REDDIT_CLIENT_SECRET'],
            user_agent='RSCG (by u/RedditThrowaway4723)',
            username=os.environ['REDDIT_USERNAME'],
            password=os.environ['REDDIT_PASSWORD'])
        # Set the config to decode HTML entities
        self.reddit.config.decode_html_entities = True
        # Set the subreddit
        self.subreddit = self.reddit.subreddit(subreddit)

    def __utc_to_datetimestr(self, utc):
        """
        Convert a UTC timestamp to a formatted string representing the corresponding datetime.

        Args:
            utc (float): The UTC timestamp to convert.

        Returns:
            str: The formatted string representing the datetime in the format "dd-mm-yyyy HH:MM:SS".
        """
        # Convert UTC timestamp to datetime object
        self.__datetime_obj = datetime.utcfromtimestamp(float(utc))
        # Convert datetime object to formatted string and return
        return self.__datetime_obj.strftime("%d-%m-%Y %H:%M:%S")

    def __filter_content(self, textstr):
        """
        Filter the content by replacing certain words and removing empty strings.

        Args:
            textstr (str): The input text to be filtered.

        Returns:
            list: A list of filtered sentences.

        """
        # Grammer fix for better TTS
        self.__unfiltered = ftfy(textstr)
        # Check words matched with replace words
        self.__chkWords = ("\n", '."', "UPDATE:", "AITA")
        self.__repWords = (". ", '". ', ". UPDATE:. ", "Am I the asshole")

        # Replace all occurrences of check words with replace words
        for check, replace in zip(self.__chkWords, self.__repWords):
            self.__unfiltered = self.__unfiltered.replace(check, replace)

        # Split content and filter out empty strings, then return
        return [f"{s.strip()}" for s in self.__unfiltered.split(". ") if len(s) > 1]

    def get_from_url(self, url):
        """
        Retrieves information about a Reddit post from its URL.

        Parameters:
        - url (str): The URL of the Reddit post.

        Returns:
        - dict: A dictionary containing the following information about the Reddit post:
            - subreddit (str): The name of the subreddit.
            - id (str): The ID of the post.
            - title (str): The title of the post.
            - time (str): The creation time of the post in the format "dd-mm-yyyy hh:mm:ss".
            - content (list): A list of sentences extracted from the post's content.
        """
        # Get post from URL
        self.post = self.reddit.submission(url=url)
        return {
            "subreddit": self.post.subreddit.display_name,
            "id": self.post.id,
            "title": self.post.title,
            "time": self.__utc_to_datetimestr(self.post.created_utc),
            "content": self.__filter_content(self.post.selftext)
        }

    def get_top_posts(self, limit=10):
        """
        Retrieves information about the top posts from the subreddit.

        Parameters:
        - limit (int): The maximum number of posts to retrieve. Default is 10.

        Returns:
        - list: A list of dictionaries containing information about the top posts.
                Each dictionary contains the following keys:
                - subreddit (str): The name of the subreddit.
                - id (str): The ID of the post.
                - title (str): The title of the post.
                - time (str): The timestamp of the post in the format "dd-mm-yyyy HH:MM:SS".
                - content (list): A list of sentences extracted from the post's content.
        """
        self.final = []  # Init final list to store data
        # Get top posts from subreddit
        for iter_post in self.subreddit.top(limit=limit):
            self.final.append({
                "subreddit": iter_post.subreddit.display_name,
                "id": iter_post.id,
                "title": iter_post.title,
                "time": self.__utc_to_datetimestr(iter_post.created_utc),
                "content": self.__filter_content(iter_post.selftext)
            })
        return self.final

    def get_hot_posts(self, limit=10):
        """
        Retrieves information about the hot posts from the subreddit.

        Parameters:
        - limit (int): The maximum number of posts to retrieve. Default is 10.

        Returns:
        - list: A list of dictionaries containing information about the hot posts.
            Each dictionary contains the following keys:
            - subreddit (str): The name of the subreddit.
            - id (str): The ID of the post.
            - title (str): The title of the post.
            - time (str): The timestamp of the post in the format "dd-mm-yyyy HH:MM:SS".
            - content (list): A list of sentences from the post's content.
        """
        self.final = []  # Init final list to store data
        # Get top posts from subreddit
        for iter_post in self.subreddit.hot(limit=limit):
            # Split content into sentences
            self.content = self.post.selftext.replace('\n', ' ').split(". ")
            self.final.append({
                "subreddit": iter_post.subreddit.display_name,
                "id": iter_post.id,
                "title": iter_post.title,
                "time": self.__utc_to_datetimestr(iter_post.created_utc),
                "content": self.__filter_content(iter_post.selftext)
            })
        return self.final
