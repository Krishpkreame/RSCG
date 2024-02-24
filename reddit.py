from datetime import datetime
import praw
from ftfy import ftfy


class RedditAPI:
    def __init__(self, client_id: str = None, client_secret: str = None, username: str = None, password: str = None):
        """
        Initializes a Reddit object with the provided credentials.

        Args:
            client_id (str): The client ID for the Reddit API.
            client_secret (str): The client secret for the Reddit API.
            username (str): The username for the Reddit account.
            password (str): The password for the Reddit account.

        Raises:
            ValueError: If any of the required credentials are not provided.
        """
        # Raise error if the environment variables are not set
        if not client_id:
            raise ValueError(
                "REDDIT_CLIENT_ID not set correctly, delete credentials.txt and setup again")
        if not client_secret:
            raise ValueError(
                "REDDIT_CLIENT_SECRET not set correctly, delete credentials.txt and setup again")
        if not username:
            raise ValueError(
                "REDDIT_USERNAME not set correctly, delete credentials.txt and setup again")
        if not password:
            raise ValueError(
                "REDDIT_PASSWORD not set correctly, delete credentials.txt and setup again")

        # Create the Reddit instance
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='RSCG',
            username=username,
            password=password)
        # Set the config to decode HTML entities
        self.reddit.config.decode_html_entities = True

    def __utc_to_datetimestr(self, utc: float):
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

    def __filter_content(self, textstr: str):
        """
        Filters the content by replacing certain words and splitting it into sentences.

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

    def get_from_url(self, url: str):
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

    def get_top_posts(self, subreddit: str, limit: int = 10):
        """
        Retrieves the top posts from a specified subreddit.

        Args:
            subreddit (str): The name of the subreddit.
            limit (int, optional): The maximum number of posts to retrieve. Defaults to 10.

        Returns:
            list: A list of dictionaries containing information about each top post.
                Each dictionary contains the following keys:
                - subreddit: The name of the subreddit.
                - id: The unique identifier of the post.
                - title: The title of the post.
                - time: The creation time of the post.
                - content: The filtered content of the post.
        """
        # Set the subreddit
        self.subreddit = self.reddit.subreddit(subreddit)

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
