import os
from PIL import Image
import imagehash
import requests
from bs4 import BeautifulSoup
import json
import time
from io import BytesIO
import json
import magic
import configparser
from mastodon import Mastodon

def post_story(imgfile, tootText, altText):
                medialist = []
                # connect to mastodon
                mastodonBot = Mastodon(
                           access_token=config['mastodon']['access_token'],
                           api_base_url=config['mastodon']['app_url']
                ) 
                # upload image
                try:
                       mime = magic.Magic(mime=True)
                       mimetype = mime.from_file(imgfile)
                       mediaid = mastodonBot.media_post(imgfile, mime_type=mimetype, description=altText)
                       medialist.append(mediaid)
                except Exception as e:
                       print ("Unable to upload image.")
                       print (e)
                     # post toot
                postedToot = mastodonBot.status_post(tootText,None,medialist,False,feedvisibility)


# Load the config
config = configparser.ConfigParser()
config.read('config.ini')

feedname = config['feed']['feed_name']
feedvisibility = config['feed']['feed_visibility']
feedtags = config['feed']['feed_tags']
imageurl = config['feed']['image_url']
texturl = config['feed']['text_url']
try:
   max_image_size  = int(config['mastodon']['max_image_size'])
except:
   max_image_size = 1600
try:
   feeddelay  = int(config['feed']['feed_delay'])
except:
   feeddelay = 600 #10 minute default 

storyhash = ""

while (1):
# try:
     response = requests.get(imageurl)
     wxtext = requests.get(texturl).text
     img = Image.open(BytesIO(response.content))
     hashedImage = imagehash.average_hash(img)
     if(storyhash!=str(hashedImage)):
            print ("NEW IMAGE!")
            storyhash = str(hashedImage)
            # shrink image for posting
            if ((img.size[0]>max_image_size) or (img.size[1]>max_image_size)):
                    origx = img.size[0]
                    origy = img.size[1]
                    if (origx>origy):
                            newx = int(max_image_size)
                            newy = int(origy * (max_image_size/origx))
                    else:
                            newy = int(max_image_size)
                            newx = int(origx * (max_image_size/origy))
                    img = img.resize((newx,newy))
            imgfile = "wxstory.png"
            img.save(imgfile)
            post_story(imgfile, wxtext+" "+feedtags, wxtext)
            print("Posted:",wxtext)
     else:
         print ("image  has not changed.") 

     time.sleep(feeddelay) # wait for next update
# except:
#  print("-Unknown error,  backing off") 
#  time.sleep(feeddelay*5) # wait for next update


