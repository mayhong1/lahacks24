#!/bin/bash

# Access token obtained after authentication
access_token=$1

# Make a GET request to retrieve media
curl -X GET "https://graph.instagram.com/me/media?fields=id,media_type,media_url&access_token=$access_token" -o downloaded_media.json

# Process the response and extract image URLs
image_urls=$(jq -r '.data[] | select(.media_type == "IMAGE") | .media_url' downloaded_media.json)

# Download images
for url in $image_urls; do
    filename=$(basename "$url")
    curl -OJL "$url"
done
