import os
import openai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import time
import requests
import random
import subprocess
import shlex


openai.api_key = '#REDACTED'

# Initialize GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Authenticate / create an API client
client_secrets_file = "client_secret.json"  # client secrets file path
scopes = ['https://www.googleapis.com/auth/youtube.upload']

flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_local_server()
youtube = build('youtube', 'v3', credentials=credentials)

x = 0

while x < 9999:
    try:
        # Generate idea
        video_idea_prompt = "Generate an inspirational quote for a YouTube short targeting the age group 12-20 in the format of: [##insert quote here] Do not elaborate or explain the quote at all, I only want the quote"
        video_idea = generate_response(video_idea_prompt).strip()

        # Generate title, description, and tags
        video_title_prompt = "Generate a title for a YouTube short about " + video_idea
        video_title = generate_response(video_title_prompt).strip()

        video_description_prompt = "Generate a description for a YouTube short about " + video_idea
        video_description = generate_response(video_description_prompt).strip()

        video_tags_prompt = "Generate tags for a YouTube short about " + video_idea
        video_tags = generate_response(video_tags_prompt).strip()

        # Choose a random video file
        video_files = ['#REDACTED']
        chosen_video = random.choice(video_files)

        # Generate the text clip with the generated text
        generated_text = video_idea.replace('"', '\\"')  # Escape any existing double quotes in the text      
        text_overlay = f'drawtext=text="{generated_text}":fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.5'

        # Create the ffmpeg command to add text overlay
        ffmpeg_command = 'ffmpeg -i {chosen_video} -vf "{text_overlay}" -codec:v libx264 -crf 18 output.mp4'
        print(f"Running command: {ffmpeg_command}")  # Print the command before executing it
        result = subprocess.run(ffmpeg_command, shell=True, capture_output=True, text=True)
        print(f"Return code: {result.returncode}")  # Print the return code
        print(result.stdout)
        print(result.stderr)

        # Choose a random music file
        music_files = ['#REDACTED']
        chosen_music = random.choice(music_files)

        # Create the ffmpeg command to add background music
        ffmpeg_command = f'ffmpeg -i output.mp4 -i {chosen_music} -c copy -shortest final_output.mp4'
        print(f"Running command: {ffmpeg_command}")  # Print the command before executing it
        result = subprocess.run(ffmpeg_command, shell=True, capture_output=True, text=True)
        print(f"Return code: {result.returncode}")  # Print the return code
        print(result.stdout)
        print(result.stderr)

        # Create a media file upload object and initialize the request to upload the video file
        media = MediaFileUpload('final_output.mp4', chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": video_title,
                    "description": video_description,
                    "tags": video_tags
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=media
        )

        # Execute and upload
        response = request.execute()
        print(response)

        # Avoid hitting rate limits, might need to adjust this
        time.sleep(60)

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(60)
        x = x + 1
        print (x)