from reddit import RedditAPI
from tiktokvoice import tts, get_duration

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
    filename = f"outputs/reddit_{x['id']}_{i}.mp3"
    tts(item, "en_us_001", filename, 1.15)
    dur = get_duration(filename)
    print(dur)
    z += 1
