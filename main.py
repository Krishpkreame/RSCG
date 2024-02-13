from reddit import RedditAPI
from tiktokvoice import tts, get_duration, merge_audio_files
from srt import gen_srt_file

reddit = RedditAPI("AmItheAsshole")

# x = reddit.get_from_url("""
# https://www.reddit.com/r/AmItheAsshole/comments/11e01qq/aita_for_not_giving_my_sister_her_wedding_dress/
# """)

x = reddit.get_top_posts(5)[3]


print(x["title"])
print(x["subreddit"])
print(x["time"])
print(x["id"])
print(len(x["content"]))

script = []
content = [x["title"]] + x["content"]
for item, i in zip(content, range(0, len(content))):
    filename = f"outputs/reddit_{x['id']}_{i}.mp3"
    tts(item, "en_us_006", filename, 1.15)
    dur = get_duration(filename)
    script.append((item, dur))
gen_srt_file(script, f"outputs/{x['id']}.srt", 0.1)
totaldur = merge_audio_files(f"outputs/{x['id']}.wav", 0.1)
print("Merged audio duration:", totaldur, "seconds")
