from reddit import RedditAPI

reddit = RedditAPI("AmItheAsshole")
x = reddit.get_from_url(
    'https://www.reddit.com/r/AmItheAsshole/comments/11e01qq/aita_for_not_giving_my_sister_her_wedding_dress/')

print(x.title)
print(x.selftext)
