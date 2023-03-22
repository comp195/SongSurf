# EXAMPLE PYTHON FILE TO DEMONSTRATE HOW TO MAKE AN API CALL TO LAST.FM

import requests # pip install requests
import json

def jprint(obj):
	trext = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

#############################
# IMPORTANT FOR API USE!
# MUST INCLUDE USER_AGENT AS A HEADER AND API KEY IN PAYLOAD!
# FAILURE TO INCLUDE WILL RISK BAN
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

# If using loops put a sleep statement to prevent overuse of the API
time.sleep(1)

# r means response
# params converts payload into query string
# headers are used in an http request to provide information about request context, so 
# server can tailor the response

r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
r.status_code

print(r.json()) # print out response in json format
