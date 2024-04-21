import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv
import os
import datetime

month_dict = {
    1  : "January",
    2  : "Februrary",
    3  : "March",
    4  : "April",
    5  : "May",
    6  : "June",
    7  : "July",
    8  : "August",
    9  : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

load_dotenv()

# Load the JSON file
def make_playlist(file_path, era_date:datetime):
    with open(file_path, 'r') as file:
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
    playlist = sp.user_playlist_create(sp.me()['id'], f"{data[0]['vibe']} era", public=False)
    playlist_id = playlist['id']
    playlist_description = f'Your {month_dict[era_date.month]} {era_date.year} vibe: '
    words = data[0]['words']

    for i in range(len(words)-1):
        playlist_description = playlist_description + words[i] + ", "
    playlist_description = playlist_description + words[len(words)-1]
    
    sp.playlist_change_details(playlist_id, description=playlist_description)

    # Add songs to the playlist
    track_uris = []
    for song in songs:
        title = song['title']
        artist = song['artist']
        results = sp.search(q='track:' + title + ' artist:' + artist, type='track')
        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])

    sp.playlist_add_items(playlist['id'], track_uris)