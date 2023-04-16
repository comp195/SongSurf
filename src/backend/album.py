import requests # pip install requests
import time
from collections import Counter
import comparer
import json
from database import *
from googleapiclient.discovery import build

### IMPORTANT YOUTUBE API INFO ###
# MUST RUN IN CMD: pip install --upgrade google-api-python-client
YOUTUBE_API_KEY = 'AIzaSyCGFt8DKXyW_i1RYNJHUCJ7OJt0m4coCTQ'
##################################

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

		time.sleep(0.8)

	comparer.compare_and_output_top_5(app, user_id, top_tags, 'album', albums)

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

	image_url=data["album"]["image"][-1]["#text"]
	album_link = data["album"]["url"]
	#release_date = data["album"]["releasedate"]
	release_date = "last.fm doesnt support release_date for albums"
	track_names = [track["name"] for track in data["album"]["tracks"]["track"]]
	image_url = data["album"]["image"][-1]["#text"]

	try:
		bio = data["album"]["wiki"]["summary"]
	except KeyError:
		bio = "No bio available for this album."

	video_link = get_album_video(album, album_artist)

	info = {'image': image_url, 'description': bio, 'video_link': video_link, 'url_link': album_link}
	return (info, track_names)

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

	#(info, track_names) = get_album_info("The Dark Side of the Moon", "Pink Floyd")
	#add_item(app, 'album', "The Dark Side of the Moon", "daydreamer.jpg", "welcome to the dark side", get_artist_object(app, 'Pink Floyd').artist_id, None, datetime(1973, 3, 1))
	albums = get_album_recommendations(app, 1, ('The Dark Side of the Moon','Pink Floyd'), ('Rumours','Fleetwood Mac'), ('Nevermind','Nirvana'))