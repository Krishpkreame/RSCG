# Reddit Short-Form Content Generator (RSCG)

RSCG is a Python-based project for automated short-form video content creation using Reddit data. It leverages Reddit API, AI text-to-speech (TTS), and code-based video editing to transform engaging Reddit threads into shareable videos.

## How to setup:

### Step 1: Download RSCG and all dependencies

1. Download Python for you computer
2. Download RSCG by using git clone or clicking on the green **Code** button and clicking **Download Zip**
3. Extract and open the folder in any terminal app
4. Run ```pip install -r requirements.txt```
5. **FFMPEG** is an important requirement needed to render the final video, follow setup [Here](https://gist.github.com/barbietunnie/47a3de3de3274956617ce092a3bc03a1)

### Step 2: Obtaining Reddit API Credentials

1. Go to [Reddit](https://www.reddit.com/) and log in (I would recommend creating a throwaway account)
2. Navigate to [Reddit Apps](https://www.reddit.com/prefs/apps).
3. Scroll down to the "Developed Applications" section and click on the "Create App" button.
4. Fill out the required fields:
   - **Name**: Choose a name for your application.
   - **App type**: Select "Script".
   - **About URL**: You can leave this blank.
   - **Redirect URI**: Enter `http://localhost:8080`.
5. Click on the "Create app" button.
6. After creating the app, you'll see your **client ID** and **client secret**. Keep these safe; you'll need them to authenticate your application.

### Step 3: Run RSCG script

1. After downloading RSCG open the folder in any terminal
2. **Run** `python main.py`. - (try `python3 main.py` if it doesnt work)
3. On first run it will run through setup where you put in the credentials you got from Step 2 (Setup once the first time you run it)
4. You will need to put a mp4 video that will be used as a background video into the **inputs** folder, the longer the video the better.
5. Here is a input video you could use, it is minecraft parkour and sized for tiktok - [Video](https://www.dropbox.com/scl/fi/d83qxfqc6e9dai1mnx6bv/background1.mp4?rlkey=ee9ttg8ctiaq4kdx6rzdg0upq&dl=0)
6. After setting up you can enter any reddit link into the program and it will create a tiktok style video in the **outputs** folder

## Example

##### Here is an example of a video made with RSCG
Reddit story used - [here](https://www.reddit.com/r/AmItheAsshole/comments/1ayhgo1/aita_for_refusing_to_share_some_of_my_food_with/)



https://github.com/Krishpkreame/RSCG/assets/79666419/79b46267-d5d1-4330-ba3f-f1969f73d037



## Functionality:

### Reddit PRAW API:

- Fetches data from specified Reddit threads or subreddits.
- Filters scraped content based on certain criteria.

### AI Text-to-Speech:

- Converts filtered text content into audio using TikTok TTS service.
- Supports multiple voices and languages.

### Code-Based Video Editing:

- Utilizes Python libraries (MoviePy) to create video sequences.
- Overlays audio on randomly cut background video.
- Basic editing capabilities (text overlays).

## Output:

- Generates short-form videos (e.g., TikTok, YouTube Shorts format) ready for sharing.

## Technical Details:

- Programming Language: Python
- Dependencies:
  - PRAW (Reddit API)
  - AI TTS service API
  - MoivePy as the video editing library

## Contributing:

- Contributions and feature enhancements are welcome. Please fork this repository, make your changes, and submit a pull request with a detailed description of the proposed changes.
