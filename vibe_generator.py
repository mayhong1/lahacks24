import google.generativeai as genai
import os
import json
import sys
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from download import download_user
from playlistmaker import make_playlist
from download import *

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1]]

# Downloading the images

def username_to_playlist(username):

  #Download images
  get_era_posts(username)

  # Modify prompt and image path here
  prompt_parts = [
    "input: What is the vibe of this image (in lowercase), and list 5 songs (in appropriate caps) that match the vibe of this image. try not to repeat artists, but if they do they should repeat at most once. Use gen-z language when describing the vibe. List 8 words (in lowercase) that describe the vibe of the image. The generated file should have a vibe key, a songs key which then contains the title and artist of every song, and a words key"
    ]

  for filename in os.listdir(username):
      prompt_parts.append(*upload_if_needed(f"{username}/{filename}"))

  prompt_parts.append("")
  prompt_parts.append("output: ")

  response = model.generate_content(prompt_parts).text

  json_obj = {"text": response}

  with open('song_list.txt', 'w') as file:
    # Write the content to the file
    file.write(response)

  make_playlist("song_list.txt")

  for uploaded_file in uploaded_files:
    genai.delete_file(name=uploaded_file.name)
  
  print("Playlist generated")