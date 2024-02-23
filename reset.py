import os
from PIL import Image
import imagehash
import requests
from bs4 import BeautifulSoup
import json
import geopandas
import fiona
import time
from io import BytesIO
import json
import magic
import configparser
from mastodon import Mastodon

fiona.supported_drivers ['KML'] = 'rw'

def save_status(storyhash):
      myjson = json.dumps(storyhash)
      with open("status.json","w") as fp:
            fp.write(myjson)
            fp.close()

def read_status():
      with open("status.json","r") as fp:
            mydata = fp.read()
            myjson = json.loads(mydata)
            return myjson

def post_story(imgfile, tootText):
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
                       mediaid = mastodonBot.media_post(imgfile, mime_type=mimetype)
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
try:
   max_image_size  = int(config['mastodon']['max_image_size'])
except:
   max_image_size = 1600
try:
   feeddelay  = int(config['feed']['feed_delay'])
except:
   feeddelay = 600 #10 minute default 

#https://www.weather.gov/source/crh/croffices.json
#National Map
#https://www.weather.gov/wrh/weatherstory_map

storyhash = {}
storyhash = read_status()

if (1):
  print (storyhash)
  stories = geopandas.read_file("https://www.weather.gov/source/wrh/weatherstory/nwsweatherstory.kml",driver="KML")
  #print (stories)


  for index,office in stories.iterrows():
     officename = office['Name']
     data = office['Description']
     soup = BeautifulSoup(data,"html.parser")
     links = soup.find_all('img')
     for link in links:
         if ("weather.gov" not in link['src']):
#              print(officename, link['src'])
              parts = link['src'].split("/")
              officecode = parts[2]
              url = "https://www.weather.gov"+link['src']
              response = requests.get(url)
              img = Image.open(BytesIO(response.content))
              hashedImage = imagehash.average_hash(img)
              storyhash[officename] = str(hashedImage)
              save_status(storyhash)

