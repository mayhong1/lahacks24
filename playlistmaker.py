import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Load the JSON file

with open('song_list.txt', 'r') as file:
    # Load the JSON data from the file into a Python object
    data = json.load(file)

# Extract the songs from the JSON data
songs = data[0]['songs']

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri='http://localhost:3000/callback',
                                               scope='playlist-modify-private'))

# Create a new playlist
playlist = sp.user_playlist_create(sp.me()['id'], data[0]['vibe'], public=False)

# Add songs to the playlist
track_uris = []
for song in songs:
    title = song['title']
    artist = song['artist']
    results = sp.search(q='track:' + title + ' artist:' + artist, type='track')
    if results['tracks']['items']:
        track_uris.append(results['tracks']['items'][0]['uri'])

sp.playlist_add_items(playlist['id'], track_uris)
