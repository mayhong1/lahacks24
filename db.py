from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["retrotune"]
users_collection = db["users"]
# print(users_collection)


# push songs to db
def push_playlists_to_mongo(username, all_playlist_jsons):
    if isinstance(all_playlist_jsons, str):
        data_to_store = json.loads(all_playlist_jsons)
    else:
        data_to_store = all_playlist_jsons

    document = {
        "username": username,
        "playlists": data_to_store 
    }

    # Insert the document into the collection
    result = db["playlists"].insert_one(document)
    print(f"Inserted document with id: {result.inserted_id}")



def add_user(username, password):
    # Function to add a user to the 'users' collection
    user_doc = {
        "username": username,
        "password": password  # In production, you should hash the password
    }
    result = db.users.insert_one(user_doc)
    return str(result.inserted_id)  # Return the ID of the inserted document

def add_playlist(username, name, description, songs):
    # Find the user by username
    user = db.users.find_one({"username": username})
    if user:
        # Function to add a playlist to the 'playlists' collection
        playlist_doc = {
            "userId": user['_id'],
            "name": name,
            "description": description,
            "songs": songs
        }
        result = db.playlists.insert_one(playlist_doc)
        return str(result.inserted_id)  # Return the ID of the inserted document
    else:
        return "User not found"

def get_all_users():
    # Function to retrieve all users
    users = list(db.users.find())
    return users  # Return a list of user documents

def get_all_playlists():
    # Function to retrieve all playlists
    playlists = list(db.playlists.find())
    return playlists  # Return a list of playlist documents


# # Example usage
# username = "jordinho108"
# password = "myPassword"  # This should be securely hashed
# user_id = add_user(username, password)

# playlist_id = add_playlist(
#     username,
#     "lowkey chaotic",
#     "A chaotic childhood",
#     [
#         {"title": "HUMBLE.", "artist": "Kendrick Lamar"},
#         # More songs
#     ]
# )

# users = get_all_users()
# playlists = get_all_playlists()

# print("Users:")
# for user in users:
#     print(user['_id'], user)

# # print("\nPlaylists:")
# for playlist in playlists:
#     print(playlist['_id'], playlist)
