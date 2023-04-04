import requests # pip install requests
import time
from collections import Counter
import comparer
import json

### IMPORTANT API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
	'user-agent': USER_AGENT
}
###########################

def get_artist(a1,a2,a3):
	# Get tags of songs/artists/albums that the user inputted
	artists = [a1, a2, a3]
	top_tags = []

	for artist in artists:
		# ----- PSEUDOCODE -----
		# if artist in database
			# retrieve tags from database
		# else
			# call api
		# ----------------------

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
			# ----- PSEUDOCODE -----
			# add tags to database
			# ----------------------

			# Add the tags to toptag array
			for tag in tags:
				top_tags.append(tag['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(1)

	top_5_artists = comparer.compare_and_output_top_5(top_tags, 'artist', artists)
	return top_5_artists

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
	bio = data["artist"]["bio"]["summary"]

	print(f"Image URL: {image_url}")
	print(f"Bio: {bio}")

# test
# artists = get_artist('Malz Monday', 'J Cole', 'Bas')