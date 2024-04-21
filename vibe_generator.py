# vibe_generator.py

import google.generativeai as genai
import os
import json
import sys
import hashlib
from pathlib import Path
from dotenv import load_dotenv
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

def username_to_eras_playlist(username):
  pics_per_era = get_era_posts(username)

  for i in range(len(pics_per_era)):
    if (pics_per_era[i][0] > 1):
      prompt_parts = [
        "input: What is the vibe of these images (in lowercase), and list 5 songs (in appropriate caps) that match the vibe of these images. try not to repeat artists, but if they do they should repeat at most once. Use gen-z language when describing the vibe. List 8 words (in lowercase) that describe the vibe of these images. The generated file should have a vibe key, a songs key which then contains the title and artist of every song, and a words key"
      ]
    
      for j in range(pics_per_era[i][0]):
        prompt_parts.append(*upload_if_needed(f"assets/{username}-era{i+1}[{j}].jpg"))
      
      prompt_parts.append("")
      prompt_parts.append("output: ")

    else:
      prompt_parts = [
        "input: What is the vibe of this image (in lowercase), and list 5 songs (in appropriate caps) that match the vibe of this image. try not to repeat artists, but if they do they should repeat at most once. Use gen-z language when describing the vibe. List 8 words (in lowercase) that describe the vibe of the image. The generated file should have a vibe key, a songs key which then contains the title and artist of every song, and a words key"
      ]

      prompt_parts.append(*upload_if_needed(f"assets/{username}-era{i+1}[0].jpg"))
      prompt_parts.append("")
      prompt_parts.append("output: ")

    response = model.generate_content(prompt_parts).text

    json_obj = {"text": response}

    f = open("song_list.txt", "w")
    f.write(response)
    f.close()

    make_playlist("song_list.txt", pics_per_era[i][1])


    for uploaded_file in uploaded_files:
      genai.delete_file(name=uploaded_file.name)
    uploaded_files.clear()
  print("playlists created")
