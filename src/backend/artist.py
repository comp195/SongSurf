# TO-DO
# CALL THIS CLASS FROM APP.PY AND USE USER INPUT AS ARTISTS
# RETURN RESULTS TO APP.PY

import requests # pip install requests
import time
from collections import Counter

### IMPORTANT API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
	'user-agent': USER_AGENT
}
###########################

def get_artist(a1,a2,a3):
	# Get tags of songs/artists/albums that the user inputted
	artist1 = a1
	artist2 = a2
	artist3 = a3

	artists = [artist1, artist2, artist3]

	toptags = []

	for artist in artists:
		payload = {
			'api_key': API_KEY,
			'method': 'artist.getTopTags',
			'format': 'json',
			'artist': artist,
			'autocorrect': 1,	# corrects if user mispelled the artist
		}

		r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)

		if r.status_code == 200:
			tags = r.json()['toptags']['tag']

			# Add tags to toptag array
			for tag in tags:
				toptags.append(tag['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(1)

	# Prints all tags acquired for debugging
	#for tag in toptags:
	#	print(tag)

	# Get the 5 most common tags
	# Output is a tuple e.g. ('rap', 5) where rap appears 5 times
	counter = Counter(toptags)
	most_common_tuples = counter.most_common(5)
	most_common_tags = [t[0] for t in most_common_tuples]	# get the most common tags from the tuples
	print(most_common_tags)

	# Use the tags to search for the top artists in those tags
	# Search the top artists for those tags
	# Find the most common artists from all the tags
	# If no common artists, take the top artists from each tag in sequential order

	topartists = []

	for tag in most_common_tags:
		# Get top 50 artists for tag
		limit = 50

		payload = {
			'api_key': API_KEY,
			'method': 'tag.gettopartists',
			'format': 'json',
			'limit': limit,
			'tag': tag
		}

		r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
		if r.status_code == 200:
			artists = r.json()['topartists']['artist']
			for artist in artists:
				topartists.append(artist['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(1)

	# Prints all artists acquired for debugging
	#for artist in topartists:
	#	print(artist)

	counter = Counter(topartists)
	most_common_tuples = counter.most_common(5)
	print(most_common_tuples)
	most_common_artists = [t[0] for t in most_common_tuples]	# get the most common tags from the tuples
	print(most_common_artists)