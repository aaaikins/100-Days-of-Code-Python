import requests
from bs4 import BeautifulSoup
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "9c467e2cb4b04af6a178d759e923b911"
CLIENT_SECRET = "29b253fcceac4cd38d3e0f70402008b1"
REDIRECT_URI = "http://example.com"
scope = "playlist-modify-private"

def get_billboard_top_100(date):
    url = f"https://www.billboard.com/charts/hot-100/{date}"
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    song_names_spans = soup.select("li ul li h3")
    song_names = [song.getText().strip() for song in song_names_spans]
    return song_names

def authenticate_spotify():
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=scope,
                            show_dialog=True)
    auth_url = sp_oauth.get_authorize_url()
    print(f'Please navigate to the following URL to authorize the application: {auth_url}')
    response = input('Enter the URL you were redirected to: ')
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code=code)
    sp = Spotify(auth=token_info['access_token'])
    return sp

def create_playlist(sp, user_id, date):
    playlist_name = f"Billboard Hot 100 - {date}"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    return playlist['id']

def get_song_uri(sp, song_name):
    result = sp.search(q=song_name, limit=1, type='track')
    tracks = result['tracks']['items']
    if tracks:
        return tracks[0]['uri']
    else:
        return None

def main():
    date = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD?\n")
    songs = get_billboard_top_100(date)
    sp = authenticate_spotify()
    user_id = sp.current_user()["id"]
    playlist_id = create_playlist(sp, user_id, date)
    song_uris = []

    for song in songs:
        uri = get_song_uri(sp, song)
        if uri:
            song_uris.append(uri)

    for i in range(0, len(song_uris), 100):
        sp.playlist_add_items(playlist_id, song_uris[i:i + 100])

    print(f"Playlist '{playlist_id}' created and songs added!")

if __name__ == "__main__":
    main()
