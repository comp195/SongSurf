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

song_name = "Caroline, No"
artist_name = "The Beach Boys"
album_name = "Pet Sounds"

mode = "artist"

# GET TRACK 
if mode == "song":
	results = sp.search(q='track:' + song_name + ' artist:' + artist_name, type='track')	# search for track

	if len(results['tracks']['items']) > 0:
	    track_uri = results['tracks']['items'][0]['uri']	# get track uri
	else:
	    print("No results found for " + song_name + " by " + artist_name)

# GET TOP ARTIST TRACK
if mode == "artist":
	results = sp.search(q='artist:' + artist_name, type='artist')	# search fr artist
	
	if len(results['artists']['items']) > 0:
	    artist_uri = results['artists']['items'][0]['uri']	# get artist uri
	else:
	    print("No results found for " + artist_name)

	top_tracks = sp.artist_top_tracks(artist_uri)	# get top tracks from artist

	if len(top_tracks['tracks']) > 0:
	    track_uri = top_tracks['tracks'][0]['uri']	# get top track uri
	else:
	    print("No top tracks found for " + artist_name)

# GET FIRST TRACK FROM ALBUM
if mode == "album":
	results = sp.search(q='album:' + album_name + ' artist:' + artist_name, type='album')	# search for album
	
	if len(results['albums']['items']) > 0:
	    album_uri = results['albums']['items'][0]['uri']	# get album uri
	else:
	    print("No results found for " + album_name + " by " + artist_name)

	album_tracks = sp.album_tracks(album_uri)	# gets list of tracks from album

	if album_tracks['items']:
	    track_uri = album_tracks['items'][0]['uri']	# get first track from album
	else:
	    print("No tracks found for " + album_name + " by " + artist_name)

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