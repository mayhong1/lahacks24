import instaloader
import os
import datetime
import sys

def get_era_posts(username, private_user=False, password=""):

    # Removes any old images in assets/
    os.system("rm assets/*.jpg")

    # Initalize Instaloader object
    loader = instaloader.Instaloader(
                quiet=True,
                download_pictures=True,
                download_videos=False,
                download_video_thumbnails=False,
                save_metadata=False,
                compress_json=False,
                post_metadata_txt_pattern=""
                )
    
    # Login if user is private
    if (private_user):
        print(f"[{username}] Logging in...")
    
        loader.login(username, password)

        print(f"[{username}] Logged in!")

    # Load user profile
    profile = instaloader.Profile.from_username(loader.context, username)

    print(f"[{username}] Loading posts...")

    # Load user posts
    posts = []
    for post in profile.get_posts():
        if (not post.is_video):
            posts.append(post)

    print(f"[{username}] Posts loaded!")

    # Decide which posts to download
    # 
    # If they have more than three posts, take the first, last, and median post
    # (based on date). 
    download_posts = []
    if (len(posts) >= 3):
        dates = [post.date for post in posts]
        middle = dates[0] + (dates[len(dates)-1]-dates[0])/2

        small_index = 1
        smallest_delta = abs(middle-dates[1])

        for i in range(2, len(dates)-1):
            if (abs(middle-dates[i]) < smallest_delta):
                smallest_delta = abs(middle-dates[i])
                small_index = i

        download_posts = [posts[0], posts[small_index], posts[len(posts)-1]]

    else:
        download_posts = posts

    # Check for carousel posts and take the first 3 images in any carousel post
    urls = []
    for post in download_posts:
        if (post.mediacount > 1):
            slide_urls = []
            slides = [slide for slide in post.get_sidecar_nodes()]

            for i in range(3):
                if (i >= len(slides)):
                    break
                slide_urls.append(slides[i].display_url)
            urls.append(slide_urls)

        else:
            urls.append([post.url])

    print(f"[{username}] Downloading images...")

    # Download the actual images
    #   - Saved in the format <username>-era<1-3>[0-2]
    #
    # era_count is a list of tuples in the format: (number of slides, date post created)
    era_count = []
    for i in range(len(download_posts)):
        era_count.append((len(urls[i]), download_posts[i].date))
        for j in range(len(urls[i])):
            loader.download_pic(filename=f"assets/{username}-era{len(download_posts)-i}[{j}]", url=urls[i][j], mtime=download_posts[i].date)
            print(f"[{username}] Downloaded {username}-era{len(download_posts)-i}[{j}].jpg")

    
    # Currently era_count is saved era3 -> era1 (descending), but 
    # vibe_generator.py reads in ascending order, so we reverse the list
    era_count = era_count[::-1]

    return era_count