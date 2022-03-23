import requests
import random
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import os
from dotenv import load_dotenv
load_dotenv()


music_list = []
username = os.environ.get("USERNAME")
scope = os.environ.get("SCOPE")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = os.environ.get("REDIRECT_URI")

token = util.prompt_for_user_token(username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri
                                   )
endpoint_url = "https://api.spotify.com/v1/recommendations?"

# OUR FILTERS
limit = 5
market = "US"
seed_genres = 'soul'

query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'

bearer = "Bearer " + token
response = requests.get(query,
                        headers={"Content-Type": "application/json",
                                 "Authorization": bearer})
json_response = response.json()
artists = []
songs = []
external_urls = []
for i in json_response['tracks']:
    # print(i['artists'][0]['external_urls']['spotify'])
    artists.append(i['artists'][0]['name'])
    songs.append(i['name'])
    external_urls.append(i['artists'][0]['external_urls']['spotify'])

for music in zip(artists, songs, external_urls):
    music_list.append(music)

chosen = random.choice(music_list)
# print(chosen)

music_list = [chosen[0] + ' by ' + chosen[1]]
music_url = chosen[2]

print(music_url)
