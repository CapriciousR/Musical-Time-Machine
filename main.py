from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint

year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
SPOTIFY_CLIENT_ID = os.environ.get('spotify_client_id')
SPOTIFY_CLIENT_SECRET = os.environ.get('spotify_client_secret')
SPOTIFY_USER_ID = os.environ.get('spotify_user_id')
redirect_uri = "http://localhost:8888/callback"

BILLBOARD_URL = f"https://www.billboard.com/charts/hot-100/{year}/"

response = requests.get(url=BILLBOARD_URL)

soup = BeautifulSoup(response.text, 'html.parser')

track_list = []

first_song_block = soup.find('li', class_ = "o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-1@mobile-max")
first_song = first_song_block.find('h3').text.strip() 
content = first_song_block.find('h3').text.strip() + ' - ' + first_song_block.find('span').text.strip() + '\n'
track_list.append(first_song)
song_blocks = soup.find_all('li', class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-050 lrv-u-padding-l-1@mobile-max")

for song_block in song_blocks:
    song = song_block.find('h3').text.strip()
    singer = song_block.find('span').text.strip()
    content += song + ' - ' + singer + '\n'
    track_list.append(song)
    
with open(f'{year}.txt', 'w', encoding='UTF-8') as file:
    file.write(content)
 
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=redirect_uri))

track_ids = []
for song in track_list:
    tracks = spotify.search(q=f'track:{song} year:{int(year.split("-")[0])-5}-{int(year.split("-")[0])+5}', limit=2)
    try:
        track_id = tracks['tracks']['items'][0]['id']
        track_ids.append(track_id)
    except IndexError:
        continue
    
print(track_ids)

id = spotify.user_playlist_create(user=SPOTIFY_USER_ID, name=f'{year} Billboard 100', public='False', description='')['id']

spotify.user_playlist_add_tracks(user=SPOTIFY_USER_ID, playlist_id=id, tracks=track_ids)

print(id)

#code