import requests # pip install requests

### IMPORTANT API INFO ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
	'user-agent': USER_AGENT
}
###########################

tag = 'rap'
limit = 10

payload = {
	'api_key': API_KEY,
	'method': 'tag.gettopartists',
	'format': 'json',
	'limit': limit,
	'tag': tag
}


r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
if r.status_code == 200:
	data = r.json()
	artists = data['topartists']['artist']
	for artist in artists:
		print(artist['name'])
else:
	print(f'Request failed with status code {r.status_code}')