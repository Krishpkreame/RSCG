from reddit import RedditAPI
from tiktokvoice import tts

reddit = RedditAPI("AmItheAsshole")

x = reddit.get_from_url("""
https://www.reddit.com/r/AmItheAsshole/comments/11e01qq/aita_for_not_giving_my_sister_her_wedding_dress/
""")

print(x["title"])
print(x["subreddit"])
print(x["time"])
print(x["id"])
print(len(x["content"]))

z = 0
for item, i in zip(x["content"], range(len(x["content"]))):
    if z > 5:
        break
    tts(item, "en_us_001", f"outputs/reddit_{x['id']}_{i}.wav", 1.15)
    z += 1
