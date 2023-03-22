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

def compare_and_output_top_5(top_tags, type):
	"""
    1) Compare input tags and grab the top 5 most common tags
	2) Use the top 5 tags to request for top 50 artists, and output their names
    
    Parameters:
    tags (list): list of tags to compare to
    type (string): output type can be any of these 3 ['artist', 'album', 'track']

    Returns:
    top_5 (list): list of artists or albums or tracks
    """
	if (type == 'artist'):
		METHOD_KEY = 'tag.getTopArtists'
		JSON_KEY_1 = 'topartists'
	elif (type == 'album'):
		METHOD_KEY = 'tag.getTopAlbums'
		JSON_KEY_1 = 'albums'
	elif (type == 'track'):
		METHOD_KEY = 'tag.getTopTracks'
		JSON_KEY_1 = 'tracks'
		
		

	# Get the 5 most common tags
	# Output is a tuple e.g. ('rap', 5) where rap appears 5 times
	counter = Counter(top_tags)
	most_common_tuples = counter.most_common(5)
	most_common_tags = [t[0] for t in most_common_tuples]	# get the most common tags from the tuples
	print(most_common_tags)

	# Use the tags to search for the top artists in those tags
	# Search the top artists for those tags
	# Find the most common artists from all the tags
	# If no common artists, take the top artists from each tag in sequential order

	top_items = []

	for tag in most_common_tags:
		# Get top 50 artists for tag
		limit = 50

		payload = {
			'api_key': API_KEY,
			'method': METHOD_KEY,
			'format': 'json',
			'limit': limit,
			'tag': tag
		}

		r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)

		if r.status_code == 200:
			items = r.json()[JSON_KEY_1][type]
			for item in items:
				top_items.append(item['name'])
		else:
			print(f'Request failed with status code {r.status_code}')

		time.sleep(1)


	counter = Counter(top_items)
	top_5_tuples = counter.most_common(5) # grab 5 most common items
	print(top_5_tuples)
	top_5_items = [t[0] for t in top_5_tuples]	# get the most common tags from the tuples
	print(top_5_items)

	return top_5_items
