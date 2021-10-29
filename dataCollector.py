import sys
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
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

playlist_ids = {
    'happy': ['37i9dQZF1DXdPec7aLTmlC', '37i9dQZF1DWSqBruwoIXkA', '37i9dQZF1DX3rxVfibe1L0', '37i9dQZF1DWYBO1MoTDhZI', '37i9dQZF1DWSf2RDTDayIx', '37i9dQZF1DX0UrRvztWcAU'],
    'sad': ['37i9dQZF1DX3YSRoSdA634', '37i9dQZF1DX59NCqCqJtoH', '37i9dQZF1DX6xZZEgC9Ubl', '37i9dQZF1DX9LT7r8qPxfa'],
    'energetic': ['37i9dQZF1DWZixSclZdoFE', '37i9dQZF1DWXLSRKeL7KwM', '37i9dQZF1DX4fpCWaHOned', '37i9dQZF1DXdxTsNp0Bzwq'],
    'romantic': ['37i9dQZF1DXcbAIldMQMIs', '37i9dQZF1DX6mvEU1S6INL', '37i9dQZF1DX7gIoKXt0gmx', '37i9dQZF1DX5IDTimEWoTd', '37i9dQZF1DX50QitC6Oqtn'],
    'chill': ['37i9dQZF1DX2yvmlOdMYzV', '37i9dQZF1DX0h2LvJ7ZJ15', '37i9dQZF1DX4WYpdgoIcn6', '37i9dQZF1DX889U0CL85jj', '37i9dQZF1DX0SM0LYsmbMT']
}


data = []

for mood in playlist_ids:
    count = 1
    for plist_id in playlist_ids[mood]:
        r = requests.get(BASE_URL + 'playlists/' + plist_id, headers=headers)
        r = r.json()
        track_ids = ''
        pl_length = 100
        if len(r['tracks']['items']) < 100:
            pl_length = len(r['tracks']['items'])
        for i in range(pl_length):
            obj = r['tracks']['items'][i]
            if obj['track'] is not None:
                track_ids += obj['track']['id']
                track_ids += '%2C'
        track_ids = track_ids[:-3]
        r = requests.get(BASE_URL + 'audio-features/?ids=' + track_ids, headers=headers)
        r = r.json()['audio_features']
        for obj in r:
            del obj['id']
            del obj['type']
            del obj['uri']
            del obj['track_href']
            del obj['analysis_url']
            obj['mood'] = mood
        data = data + r
        i = round(count / len(playlist_ids[mood]) * 50)
        count += 1
        sys.stdout.write('\r')
        sys.stdout.write("%s: [%-50s] %d%%" % (mood, '=' * i, 2 * i))
        sys.stdout.flush()
    print()


with open('song_mood_data.json', 'w') as outfile:
    json.dump(data, outfile)
