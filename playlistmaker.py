import os
import datetime
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


# Dictionary to convert from month numbers to string
month_dict = {
    1  : "january",
    2  : "februrary",
    3  : "march",
    4  : "april",
    5  : "may",
    6  : "june",
    7  : "july",
    8  : "august",
    9  : "september",
    10 : "october",
    11 : "november",
    12 : "december"
}

# Load the .env folder
load_dotenv()

def make_playlist(file_path, era_date:datetime):

    # Load the JSON file
    f = open(file_path, "r")
    data = json.load(f)
    f.close()

    # Extract the songs from the JSON data
    songs = data[0]["songs"]

    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                                client_secret=os.getenv("CLIENT_SECRET"),
                                                redirect_uri="http://localhost:3000/callback",
                                                scope="playlist-modify-private"))

    # Create a new playlist
    playlist = sp.user_playlist_create(sp.me()["id"], f"{data[0]['vibe']} era", public=False)
    playlist_id = playlist["id"]

    # Create playlist description 
    playlist_description = f"your {month_dict[era_date.month]} {era_date.year} vibes: "
    words = data[0]["words"]

    for i in range(len(words)-1):
        playlist_description = playlist_description + words[i] + ", "
    playlist_description = playlist_description + words[len(words)-1]
    
    sp.playlist_change_details(playlist_id, description=playlist_description)

    # Add songs to the playlist
    track_uris = []
    for song in songs:
        title = song["title"]
        artist = song["artist"]
        results = sp.search(q=f"track:{title} artist:{artist}", type="track")
        if results["tracks"]["items"]:
            track_uris.append(results["tracks"]["items"][0]["uri"])

    sp.playlist_add_items(playlist["id"], track_uris)