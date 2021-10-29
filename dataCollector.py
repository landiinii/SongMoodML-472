import requests

CLIENT_ID = '1ac56bed95e14099a932ec540a79080a'
CLIENT_SECRET = '3e30760e35524287a7fdc748b6d5f472'
AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '37i9dQZF1DXdPec7aLTmlC'

# actual GET request with proper header
r = requests.get(BASE_URL + 'playlists/' + track_id, headers=headers)
r = r.json()
playlist_ids = ''
for obj in r['tracks']['items']:
    playlist_ids += obj['track']['id']
    playlist_ids += '%2C'
playlist_ids = playlist_ids[:-3]
print(playlist_ids)
r = requests.get(BASE_URL + 'audio-features/?ids=' + playlist_ids, headers=headers)
r = r.json()['audio_features']
'''
         "tempo":116.011,
         "type":"audio_features",
         "id":"0mA7zotmg2ZFMRALljdZsS",
         "uri":"spotify:track:0mA7zotmg2ZFMRALljdZsS",
         "track_href":"https://api.spotify.com/v1/tracks/0mA7zotmg2ZFMRALljdZsS",
         "analysis_url":"https://api.spotify.com/v1/audio-analysis/0mA7zotmg2ZFMRALljdZsS",
'''
for obj in r:
    del obj['id']
    del obj['type']
    del obj['uri']
    del obj['track_href']
    del obj['analysis_url']

print(r)