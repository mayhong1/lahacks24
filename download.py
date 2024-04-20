import instaloader, os


def download_user(username):
    loader = instaloader.Instaloader()

    loader.download_profile(username, profile_pic=False)

    os.system("find " + username + " -type f ! -name \"*.jpg\" -exec rm {} +")

    file_count = 0
    for filename in os.listdir(username):
        if filename.endswith('.jpg'):  # Assuming images are downloaded as .jpg files
            os.rename(os.path.join(username, filename), os.path.join(username, f'{file_count}.jpg'))
            file_count += 1