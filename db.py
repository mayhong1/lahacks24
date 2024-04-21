from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.retrotune

def add_user(email, username):
    # Function to add a user to the 'users' collection
    user_doc = {
        "email": email,
        "username": username
    }
    result = db.users.insert_one(user_doc)
    return str(result.inserted_id)  # Return the ID of the inserted document

def add_playlist(user_id, name, description, songs):
    # Function to add a playlist to the 'playlists' collection
    playlist_doc = {
        "userId": user_id,
        "name": name,
        "description": description,
        "songs": songs
    }
    result = db.playlists.insert_one(playlist_doc)
    return str(result.inserted_id)  # Return the ID of the inserted document

def get_all_users():
    # Function to retrieve all users
    users = list(db.users.find())
    return users  # Return a list of user documents

def get_all_playlists():
    # Function to retrieve all playlists
    playlists = list(db.playlists.find())
    return playlists  # Return a list of playlist documents


#test

# Example usage
user_id = add_user("jordan@caffeinated.org", "jordinho108")
playlist_id = add_playlist(
    user_id,
    "lowkey chaotic",
    "A chaotic childhood",
    [
        {"title": "HUMBLE.", "artist": "Kendrick Lamar"},
        # More songs
    ]
)

users = get_all_users()
playlists = get_all_playlists()

print("Users:")
for user in users:
    print(user['_id'], user)

print("\nPlaylists:")
for playlist in playlists:
    print(playlist['_id'], playlist)
