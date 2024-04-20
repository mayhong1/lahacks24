import instaloader, os

def download_user(username, bool):
    loader = instaloader.Instaloader(
                download_pictures=True,
                download_videos=False,
                download_video_thumbnails=False,
                save_metadata=False,
                compress_json=False,
                post_metadata_txt_pattern=""
                )

    profile = instaloader.Profile.from_username(loader.context, username)

    loader.download_profiles({profile}, profile_pic=False)

def test_private_user():
    loader = instaloader.Instaloader(
                download_pictures=True,
                download_videos=False,
                download_video_thumbnails=False,
                save_metadata=False,
                compress_json=False,
                post_metadata_txt_pattern=""
                )
    
    loader.login("danielbonkowsky", "7iqSXo4iaua8NF")
    profile = instaloader.Profile.from_username(loader.context, "danielbonkowsky")
    loader.download_profiles({profile}, profile_pic=False)
