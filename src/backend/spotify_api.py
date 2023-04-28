#EXAMPLE FILE FOR SPOTIFY API USAGE
#pip install spotipy --upgrade

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import requests

##### API INFORMATION ######
client_id = '52d2576fa6ce4b1b8c45eb1b35107ef4'
client_secret = '66c44d6c558b4b2eb90946c81d233390'
redirect_uri = 'http://127.0.0.1:8000'

os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri
#############################

# Authenticate with Spotify API using the client credentials flow
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

song_name = "Ambitionz Az A Ridah"
artist_name = "2Pac"

# Creates search query with song and artist name
results = sp.search(q='track:' + song_name + ' artist:' + artist_name, type='track')

# Get the URI of the first search result track, or set a default value if no results found
if len(results['tracks']['items']) > 0:
    track_uri = results['tracks']['items'][0]['uri']	# get track uri

    # Get devices that are playing Spotify
    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))

    devices = sp.devices()
    deviceID = devices['devices'][0]['id']

    # Play on first device found
    sp.start_playback(deviceID, None, [track_uri])
else:
    print("No results found for " + song_name + " by " + artist_name)