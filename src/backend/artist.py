import requests # pip install requests
import json

def jprint(obj):
	trext = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

### IMPORTANT FOR API USE ###
USER_AGENT = 'wbuop'
API_KEY = 'ebc5386ea6b0af15cae300e0da5a3af5'

headers = {
	'user-agent': USER_AGENT
}

payload = {
	'api_key': API_KEY,
	'method': 'chart.gettopartists',
	'format': 'json'
}
##############################

r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
r.status_code

print(r.json())