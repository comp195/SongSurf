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

def get_album(a1,a2,a3):
	# Get tags of songs/albums/albums that the user inputted
	albums = [a1[0],a2[0],a3[0]]
	artists = [a1[1],a2[1],a3[1]]
	top_tags = []

	for i in range(len(albums)):
		# ----- PSEUDOCODE -----
		# if album in database
			# retrieve tags from database
		# else
			# call api
		# ----------------------

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

	top_5_albums = comparer.compare_and_output_top_5(top_tags, 'album', albums)
	return top_5_albums

def get_album_info(a1):
	payload = {
		'api_key': API_KEY,
		'method': 'album.getinfo',
		'format': 'json',
		'artist': a1[0],
		'album':a1[1]
	}

	print(a1[0])
	print(a1[1])

	r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
	data = json.loads(r.text)

	print(data)

	image_url=data["album"]["image"][-1]["#text"]	# currently the requested data from last.fm does not return image urls, check later

	print(f"Image URL: {image_url}")

# test
# albums = get_album(('The Dark Side of the Moon','Pink Floyd'), ('Rumours','Fleetwood Mac'), ('Nevermind','Nirvana'))