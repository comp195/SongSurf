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

### IMPORTANT API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
	'user-agent': USER_AGENT
}
###########################

# *note - get_track() doesnt return album_id but has everything else. 
# so you have to use get_track_info() and then you get the album_id
#  - temporary solution: only set the album_id for tracks that were accessed by recommending albums. 
def get_track_recommendations(app, user_id, a1,a2,a3):
	# Get tags of songs/tracks/tracks that the user inputted
	tracks = [a1[0],a2[0],a3[0]]
	artists = [a1[1],a2[1],a3[1]]
	top_tags = []


	for i in range(len(tracks)):

		payload = {
			'api_key': API_KEY,
			'method': 'track.getTopTags',
			'format': 'json',
			'track': tracks[i],
			'artist': artists[i],
			'autocorrect': 1,	# corrects if user mispelled the track
		}

		# API Call to last.fm
		r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)

		# print(r.status_code)

		if r.status_code == 200: # if successful
			tags = r.json()['toptags']['tag']
			# ----- PSEUDOCODE -----
			# add tags to database
			# ----------------------

			# print(r.json())

			# Add the tags to toptag array
			for tag in tags:
				top_tags.append(tag['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(0.7)

	comparer.compare_and_output_top_21(app, user_id, top_tags, 'track', tracks)


def get_track_info(track, track_artist):
	payload = {
		'api_key': API_KEY,
		'method': 'track.getinfo',
		'format': 'json',
		'track': track,
		'artist': track_artist,
	}

	r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
	data = json.loads(r.text)

	try:
		image_url=data["track"]["album"]["image"][-1]["#text"]
	except KeyError:
		image_url = "No image available for this track"
	
	track_link = data["track"]["url"]
	try:
		album_name = data["track"]["album"]["title"] 
	except KeyError:
		album_name = "N/A"
	try:
		bio = data["track"]["wiki"]["summary"].split("<a")[0]
	except KeyError:
		bio = "No bio available for this track."

	video_link = get_track_video(track, track_artist)

	info = {'image': image_url, 'description': bio, 'video_link': video_link, 'url_link': track_link, 'album_name': album_name}
	return info

def get_track_audio(song_name, artist_name):
	print("Retrieving audio...")

	results = sp.search(q='track:' + song_name + ' artist:' + artist_name, type='track')	# search for track

	if len(results['tracks']['items']) > 0:
		track_uri = results['tracks']['items'][0]['uri']	# get track uri
	else:
		print("No results found for " + song_name + " by " + artist_name)

	return track_uri

def get_track_image(song_name, artist_name):
	print("Retrieving image...")

	results = sp.search(q='track:' + song_name + ' artist:' + artist_name, type='track')	# search for track

	if len(results['tracks']['items']) > 0:
		track_uri = results['tracks']['items'][0]['uri']	# get track uri
	else:
		print("No results found for " + song_name + " by " + artist_name)

	artist = sp.artist(artist_uri)
	picture_url = artist['images'][0]['url']

	return picture_url

def get_track_video(track, track_artist):
	print("Retrieving video...")
	youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

	search_query = track + ' ' + track_artist
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

# test
def test_track(app):
	database.add_item(app, 'track', 'Stress out', 'No image availabile for this track', '"Stressed Out" is a song written and recorded by American alternative hip hop band Twenty One Pilots for their fourth studio album, Blurryface (2015). Written by Tyler Joseph and produced by Mike Elizondo, the lyrics discuss the harsh end of adolescence and the transition to adulthood. The song was released as a single on April 28, 2015 on the Google Play Store and Amazon, and was issued to top 40 radio stations on November 10. "Stressed Out" reached number two on the US Billboard Hot 100, and number one on Hot Rock Songs and Mainstream Top 40.'
		   , 'https://www.youtube.com/embed/pXRviuL6vMY', 'https://www.last.fm/music/Twenty+One+Pilots/_/Stressed+Out')
	get_track_info('stressed out', 'twenty one pilots')
	#database.add_item(app, 'artist', 'Pink Floyd', 'solar.jpg', 'rock band')
	#database.add_item(app, 'track', 'Wish you were Here', 'daydreamer.jpg', 'Debut track', database.get_artist_object(app, 'Pink Floyd').artist_id)
	tracks = get_track_recommendations(app, 1, ('Wish you were Here','Pink Floyd'), ('Dreams','Fleetwood Mac'), ('Come as you are','Nirvana'))