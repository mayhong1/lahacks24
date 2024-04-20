import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

load_dotenv()
firebase_credentials_path = os.getenv("SERVICE_ACCOUNT_KEY_PATH")

# Initialize Firebase Admin using a service account
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)

# Firestore database client
db = firestore.client()

def add_user(email, username):
    # Function to add a user to the 'users' collection
    user_data = {
        "email": email,
        "username": username
    }
    # Add user data to Firestore and return the document reference ID
    user_ref = db.collection('users').add(user_data)
    return user_ref[1].id

def add_playlist(user_id, name, description, songs):
    # Function to add a playlist to the 'playlists' collection
    playlist_data = {
        "userId": user_id,
        "name": name,
        "description": description,
        "songs": songs
    }
    playlist_ref = db.collection('playlists').add(playlist_data)
    return playlist_ref[1].id

def get_all_users():
    # Function to retrieve all users
    users_ref = db.collection('users').stream()
    users = {user.id: user.to_dict() for user in users_ref}
    return users

def get_all_playlists():
    # Function to retrieve all playlists
    playlists_ref = db.collection('playlists').stream()
    playlists = {playlist.id: playlist.to_dict() for playlist in playlists_ref}
    return playlists


#test

# Add a user
user_id = add_user("jordan@caffeinated.org", "jordinho108")

# Add a playlist for the user
playlist_id = add_playlist(
    user_id,
    "lowkey chaotic",
    "A chaotic childhood",
    [
        {"title": "HUMBLE.", "artist": "Kendrick Lamar"},
        # More songs
    ]
)

# Retrieve all users and playlists and print them
users = get_all_users()
playlists = get_all_playlists()

print("Users:")
for user_id, user_data in users.items():
    print(user_id, user_data)

print("\nPlaylists:")
for playlist_id, playlist_data in playlists.items():
    print(playlist_id, playlist_data)
