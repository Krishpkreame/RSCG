# Function to generate an SRT file from subtitles
def gen_srt_file(subtitles: list, file_path: str, delay: int = 0.1):
    """
    Generate an SRT file from a list of subtitles.

    Args:
        subtitles (tuple): A tuple of (sentence, duration) pairs representing the subtitles.
        file_path (str): The file path where the SRT file will be saved.
        delay (float, optional): The delay in seconds to be added after each subtitle. Defaults to 0.0.
    """

    # Function to format the duration in HH:MM:SS,mmm format
    def format_duration(duration):
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        milliseconds = int((duration - int(duration)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    srt_content = ""  # Variable to store the content of the SRT file
    current_time = 0.0  # Variable to keep track of the current time
    for index, (sentence, duration) in enumerate(subtitles, start=1):
        start_time = format_duration(current_time)  # Format the start time
        current_time += duration  # Update the current time
        end_time = format_duration(current_time)  # Format the end time
        # Add the subtitle to the SRT content
        srt_content += f"{index}\n{start_time} --> {end_time}\n{sentence}\n\n"
        current_time += delay  # Add delay after each subtitle
    with open(file_path, "w") as f:
        f.write(srt_content)  # Write the SRT content to the file
