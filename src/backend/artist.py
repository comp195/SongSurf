import requests # pip install requests
import time
from collections import Counter
import comparer

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

		time.sleep(1)

	top_5_artists = comparer.compare_and_output_top_5(top_tags, 'artist')
	return top_5_artists

# test
# artists = get_artist('Malz Monday', 'J Cole', 'Bas')