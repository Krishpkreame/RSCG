from reddit import RedditAPI
from tiktokvoice import tts, get_duration, merge_audio_files
from srt import gen_srt_file
from editor import VideoEditor
reddit = RedditAPI("AmItheAsshole")

# x = reddit.get_from_url("""
# https://www.reddit.com/r/AmItheAsshole/comments/11e01qq/aita_for_not_giving_my_sister_her_wedding_dress/
# """)

x = reddit.get_top_posts(10)[8]


print("Title :", x["title"])
print("Subred :", x["subreddit"])
print("Time :", x["time"])
print("ID :", x["id"])
print("No. of lines :", len(x["content"]))

script = []
content = [x["title"]] + x["content"]
for item, i in zip(content, range(0, len(content))):
    filename = f"outputs/temp_{x['id']}_{i}.mp3"
    tts(item, "en_us_001", filename, 1.15)
    dur = get_duration(filename)
    script.append((item, dur))
print("Created audio files for script")
srt_path = f"inputs/{x['id']}.srt"
gen_srt_file(script, srt_path, 0.1)
wav_path = f"inputs/{x['id']}.wav"
totaldur = merge_audio_files(wav_path, 0.1)
print("Merged audio duration:", totaldur, "seconds")

v = VideoEditor(totaldur, srt_path, wav_path, False)
v.start_render(f"outputs/{x['id']}.mp4")
