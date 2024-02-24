from reddit import RedditAPI
from tiktokvoice import tts, get_duration, merge_audio_files
from srt import gen_srt_file
from editor import VideoEditor
import subprocess
import os


def setup_credentials():
    print("\n"*10, "-"*30, "\nSetting up the credentials\n")
    print("You will need to create a Reddit app and get the client id and client secret\n")
    print("You will also need to enter your Reddit username and password\n")
    print("These credentials will be stored in a file called credentials.txt\n")
    print("This file will be stored locally and will only be used to authenticate with Reddit and to get the post text\n")
    print("Goto https://github.com/Krishpkreame/RSCG and follow the instructions\n")
    print("I would recommend creating a new throwaway Reddit account\n")
    print("This will only run the first time you run the program\n")
    client_id = input("Enter the client id:\n")
    client_secret = input("Enter the client secret:\n")
    username = input("Enter the username:\n")
    password = input("Enter the password:\n")
    with open("credentials.txt", "w") as f:
        f.write(f"{client_id}\n{client_secret}\n{username}\n{password}")


if __name__ == "__main__":
    # Check if ffmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("ffmpeg is not installed. Please install ffmpeg to continue.")
        exit(1)

    # Check if the credentials file exists
    if not os.path.exists("credentials.txt"):
        print("No credentials file found, going through the setup - ")
        setup_credentials()

    # Check if the outputs folder exists
    if not os.path.exists("outputs"):
        os.mkdir("outputs")
        print("Created inputs folder\n - This is where final videos will be saved.")
    # Check if the inputs folder exists
    if not os.path.exists("inputs"):
        os.mkdir("inputs")
        print("Created inputs folder\n - This is where input video files will need to be stored\n - The srt and wav files will also be stored here.")

    # Check if any mp4 files are present in the inputs folder
    if len([i for i in os.listdir("inputs") if i.endswith(".mp4")]) == 0:
        print("No input video files found in the inputs folder, Add your input video files to this folder")
        exit(1)

    # Read the credentials from the file
    with open("credentials.txt", "r") as f:
        creds = f.readlines()

    # Try create the Reddit instance with the credentials.
    try:
        reddit = RedditAPI(
            creds[0].strip(),  # client_id
            creds[1].strip(),  # client_secret
            creds[2].strip(),  # username
            creds[3].strip())  # password
    except:
        print("credentials not set correctly, delete credentials.txt and setup again")
        exit(1)

    print("\n"*10, "-"*30, "\nWelcome to the Reddit to TikTok Video Creator\n")

    url = input("Enter the Reddit post URL:\n")

    # Get the post from the URL
    post = reddit.get_from_url(url)

    # Print the post details
    print("Title :", post["title"])
    print("Subred :", post["subreddit"])
    print("Time :", post["time"])
    print("ID :", post["id"])
    print("No. of lines :", len(post["content"]))

    # Ask if the user wants to proceed
    proceed = input("Do you want to proceed? (y/n)\n")
    if proceed.lower() != "y":
        print("Exiting")
        exit(0)

    # Create the audio files for each sentence using the script
    script = []
    content = [post["title"]] + post["content"]

    for item, i in zip(content, range(0, len(content))):
        filename = f"outputs/temp_{post['id']}_{i}.mp3"
        tts(item, "en_us_001", filename, 1.15)
        dur = get_duration(filename)
        script.append((item, dur))
    print("Created audio files for script")

    # Create the srt using the script
    srt_path = f"inputs/{post['id']}.srt"
    gen_srt_file(script, srt_path, 0.1)

    # Merge the audio files into one
    wav_path = f"inputs/{post['id']}.wav"
    totaldur = merge_audio_files(wav_path, 0.1)
    print("Merged audio duration:", totaldur, "seconds")

    # Create the video
    v = VideoEditor(totaldur, srt_path, wav_path, False)
    v.start_render(f"outputs/{post['id']}.mp4")
