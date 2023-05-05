import requests # pip install requests
import time
from collections import Counter
import comparer
import json
import database
from googleapiclient.discovery import build

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

### IMPORTANT YOUTUBE API INFO ###
# MUST RUN IN CMD: pip install --upgrade google-api-python-client
YOUTUBE_API_KEY = 'AIzaSyCGFt8DKXyW_i1RYNJHUCJ7OJt0m4coCTQ'

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

##################################

### IMPORTANT Last.fm API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
	'user-agent': USER_AGENT
}
###########################

def get_artist_recommendations(app, user_id, a1,a2,a3):
	# Get tags of songs/artists/albums that the user inputted
	artists = [a1, a2, a3]
	top_tags = []

	for artist in artists:
		payload = {
			'api_key': API_KEY,
			'method': 'artist.getTopTags',
			'format': 'json',
			'artist': artist,
			'autocorrect': 1,	# corrects if user mispelled the artist
		}

		# API Call to last.fm
		r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)

		if r.status_code == 200: # if successful
			tags = r.json()['toptags']['tag']

			# Add the tags to toptag array
			for tag in tags:
				top_tags.append(tag['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(0.7)

	comparer.compare_and_output_top_21(app, user_id, top_tags, 'artist', artists)


def get_artist_info(a1):
	payload = {
		'api_key': API_KEY,
		'method': 'artist.getinfo',
		'format': 'json',
		'artist': a1,
	}

	r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
	data = json.loads(r.text)

	image_url=data["artist"]["image"][-1]["#text"]
	bio = data["artist"]["bio"]["summary"].split("<a")[0]
	artist_link = data["artist"]["url"]

	video_link = get_artist_video(a1)

	info = {'image': image_url, 'description': bio, 'video_link': video_link, 'url_link': artist_link}

	return info

def get_artist_audio(a1):
	print("Retrieving audio...")

	artist_name = a1

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

	return track_uri

def get_artist_image(a1):
	print("Retrieving image...")

	artist_name = "a1"

	results = sp.search(q='artist:' + artist_name, type='artist')	# search fr artist
	
	if len(results['artists']['items']) > 0:
	    artist_uri = results['artists']['items'][0]['uri']	# get artist uri
	else:
	    print("No results found for " + artist_name)

	artist = sp.artist(artist_id)
    picture_url = artist['images'][0]['url']

    return picture_url


def test_artist(app):
	database.add_item(app, 'artist', 'Malz Monday', 'mm.jpg', 'Man of god walking with the devil', 'https://www.last.fm/music/Malz+Monday')
	artists = get_artist_recommendations(app, 1,'Malz Monday', 'J Cole', 'Bas')

def get_artist_video(a1):
	print("Retrieving video...")
	youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

	search_query = a1
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
		#print(f'Video ID: {video["video_id"]}, Video Title: {video["video_title"]}')
		video_link = "https://www.youtube.com/embed/" + video["video_id"]
		return video_link
