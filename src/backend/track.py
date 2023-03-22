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

def get_track(a1,a2,a3):
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

		if r.status_code == 200: # if successful
			tags = r.json()['toptags']['tag']

			# Add the tags to toptag array
			for tag in tags:
				top_tags.append(tag['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(1)

	top_5_tracks = comparer.compare_and_output_top_5(top_tags, 'track')
	return top_5_tracks

# test
# tracks = get_track(('Wish you were Here','Pink Floyd'), ('Dreams','Fleetwood Mac'), ('Come as you are','Nirvana'))