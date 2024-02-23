# wxstory-single

A quick set of python scripts for checking a US National Weather Service (NWS) weather story graphic, and posting it automatically Mastodon. Created by AI6YR (Ben)

## Mastodon setup

In order to have this script work, you need the following:
1. A dedicated Mastodon user account created on a server.
2. An "access key" for your app created for that user account. (under yourserver/settings/applications)

## Python setup
Make sure to install the following Python packages

`pip3 install bs4 pillow mastodon.py feedparser imagehash configparser`

## Script setup

All configuration for the script will ultimately reside in config.ini

### Mastodon configuration
* access_token = Mastodon access token
* app_url = Mastodon server
* max_image_size = max image size accepted by server

### Feed configuration
* feed_url = URL of the RSS feed you want to query
* feed_name = What you want to name this feed
* feed_visibility = public, unlisted, etc. (per Mastodon.py)
* feed_tags = #your #additional #tags here will be appended to the toot
* feed_delay = delay in seconds between checking on the image file
- image_url = URL of the gif/png/jpg you want to check for changes
- text_url = URL of where text for the alt text for the image is located

## Running the script

python3 story.py

## Unattended/background operation

If you want to run this unattended:

screen

nohup python3 -u story.py &


