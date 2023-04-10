import requests # pip install requests
import time
from collections import Counter
import comparer
import json
from database import *
### IMPORTANT API INFO ###
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

		time.sleep(1)

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



	info = {'image': image_url, 'description': bio, 'url_link': album_link}
	return (info, track_names)

# test
def test_album(app):

	#(info, track_names) = get_album_info("The Dark Side of the Moon", "Pink Floyd")
	#add_item(app, 'album', "The Dark Side of the Moon", "daydreamer.jpg", "welcome to the dark side", get_artist_object(app, 'Pink Floyd').artist_id, None, datetime(1973, 3, 1))
	albums = get_album_recommendations(app, 1, ('The Dark Side of the Moon','Pink Floyd'), ('Rumours','Fleetwood Mac'), ('Nevermind','Nirvana'))