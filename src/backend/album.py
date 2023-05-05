import requests # pip install requests
import time
from collections import Counter
import comparer
import json
from database import *
from googleapiclient.discovery import build

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

### IMPORTANT YOUTUBE API INFO ###
# MUST RUN IN CMD: pip install --upgrade google-api-python-client
YOUTUBE_API_KEY = 'AIzaSyCGFt8DKXyW_i1RYNJHUCJ7OJt0m4coCTQ'
##################################

##### API INFORMATION ######
client_id = '52d2576fa6ce4b1b8c45eb1b35107ef4'
client_secret = '66c44d6c558b4b2eb90946c81d233390'
redirect_uri = 'http://127.0.0.1:8000'

os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#############################

### IMPORTANT LAST.FM API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
	'user-agent': USER_AGENT
}
###########################

def get_album_recommendations(app, user_id, a1,a2,a3):
	# Get tags of songs/albums/albums that the user inputted
	albums = [a1[0],a2[0],a3[0]]
	artists = [a1[1],a2[1],a3[1]]
	top_tags = []

	for i in range(len(albums)):

		payload = {
			'api_key': API_KEY,
			'method': 'album.getTopTags',
			'format': 'json',
			'album': albums[i],
			'artist': artists[i],
			'autocorrect': 1,	# corrects if user mispelled the album
		}

		# API Call to last.fm
		r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)

		if r.status_code == 200: # if successful
			tags = r.json()['toptags']['tag']
			# ----- PSEUDOCODE -----
			# add tags to database
			# ----------------------

			# Add the tags to toptag array
			for tag in tags:
				top_tags.append(tag['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(0.7)

	comparer.compare_and_output_top_21(app, user_id, top_tags, 'album', albums)

def get_album_info(album, album_artist):
	payload = {
		'api_key': API_KEY,
		'method': 'album.getinfo',
		'format': 'json',
		'artist': album_artist,
		'album': album
	}


	r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
	data = json.loads(r.text)
	# # special case
	# if (data["message"] == 'Album not found'):
	# 	print(album)
	# 	print(album_artist)
	# 	print(data)
	try:
		image_url=data["album"]["image"][-1]["#text"]
	except KeyError:
		image_url="N/A"
	
	album_link = data["album"]["url"]
	#release_date = data["album"]["releasedate"]
	release_date = "last.fm doesnt support release_date for albums"
	""" We dont get the tracks of each album as currently the info for each yt api call is too much """
	#track_names = [track["name"] for track in data["album"]["tracks"]["track"]]
	track_names = None
	image_url = data["album"]["image"][-1]["#text"]

	try:
		bio = data["album"]["wiki"]["summary"].split("<a")[0]
	except KeyError:
		bio = "No bio available for this album."

	audio_link = get_album_audio(album, album_artist)

	info = {'image': image_url, 'description': bio, 'audio_link': audio_link, 'url_link': album_link}
	return (info, track_names)

def get_album_audio(album_name, artist_name):
	print("Retrieving audio...")

	results = sp.search(q='album:' + album_name + ' artist:' + artist_name, type='album')	# search for album

	if len(results['albums']['items']) > 0:
		album_uri = results['albums']['items'][0]['uri']	# get album uri
		album_tracks = sp.album_tracks(album_uri)	# gets list of tracks from album
		if album_tracks['items']:
			track_uri = album_tracks['items'][0]['uri']	# get first track from album
	else:
		print("No results found for " + album_name + " by " + artist_name)
		album_uri = None
		track_uri = None

	return track_uri

def get_album_image(album_name, artist_name):
	print("Retrieving image...")

	results = sp.search(q='album:' + album_name + ' artist:' + artist_name, type='album')	# search for album

	if len(results['albums']['items']) > 0:
		album_uri = results['albums']['items'][0]['uri']	# get album uri
	else:
		print("No results found for " + album_name + " by " + artist_name)

	album = sp.album(album_uri)
	picture_url = album['images'][0]['url']

	return picture_url

def get_album_video(album, album_artist):
	print("Retrieving video...")
	youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

	search_query = album + ' ' + album_artist
	max_results = 1

	search_response = youtube.search().list(
		q=search_query,
		type='video',
		part='id,snippet',
		maxResults=max_results
	).execute()

	videos = []
	for item in search_response['items']:
		video_id = item['id']['videoId']
		video_title = item['snippet']['title']
		videos.append({'video_id':video_id, 'video_title': video_title})

	for video in videos:
		# print(f'Video ID: {video["video_id"]}, Video Title: {video["video_title"]}')
		video_link = "https://www.youtube.com/embed/" + video["video_id"]
		return video_link

# test
def test_album(app):
	get_album_info('Stan', 'Eminem')
	#(info, track_names) = get_album_info("The Dark Side of the Moon", "Pink Floyd")
	#add_item(app, 'album', "The Dark Side of the Moon", "daydreamer.jpg", "welcome to the dark side", get_artist_object(app, 'Pink Floyd').artist_id, None, datetime(1973, 3, 1))
	albums = get_album_recommendations(app, 1, ('The Dark Side of the Moon','Pink Floyd'), ('Rumours','Fleetwood Mac'), ('Nevermind','Nirvana'))