import requests
from bs4 import BeautifulSoup
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

# Spotify API credentials and constants
CLIENT_ID = "9c467e2cb4b04af6a178d759e923b911"
CLIENT_SECRET = "a33aea5b6b0e4aed91fdf8a728cd7ec5"
REDIRECT_URI = "http://example.com"
scope = "playlist-modify-private"


def get_billboard_top_100(date):
    """
    Fetches the Billboard Hot 100 songs for a given date.
    """

    url = f"https://www.billboard.com/charts/hot-100/{date}"
    response = requests.get(url)
    content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')
    song_names_spans = soup.select("li ul li h3")

    # Extract song names
    song_names = [song.getText().strip() for song in song_names_spans]
    return song_names


def authenticate_spotify():
    """
    Authenticates the application with Spotify using OAuth and returns a Spotify client object.

    """
    # Set up the Spotify OAuth object
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=scope,
                            show_dialog=True)

    # Get the authorization URL and prompt the user to authorize the application
    auth_url = sp_oauth.get_authorize_url()
    st.write(f'Please navigate to the following URL to authorize the application: [Authorize Spotify]({auth_url})')

    # Capture the redirect URL containing the authorization code
    response = st.text_input('Enter the URL you were redirected to after authorization:', '')

    if response:
        # Extract the authorization code from the redirect URL
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code=code)

        # Create a Spotify client object using the access token
        sp = Spotify(auth=token_info['access_token'])
        return sp
    return None


def create_playlist(sp, user_id, date):
    """
    Creates a new private playlist on Spotify.
    """
    playlist_name = f"Billboard Hot 100 - {date}"

    # Create a new private playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    return playlist['id']


def get_song_uri(sp, song_name):
    """
    Searches for a song on Spotify by name and returns its URI.
    """
    result = sp.search(q=song_name, limit=1, type='track')
    tracks = result['tracks']['items']
    if tracks:
        return tracks[0]['uri']
    else:
        return None


def main():
    """
    Main function to execute the workflow of fetching Billboard songs and creating a Spotify playlist.
    """
    st.title('Billboard Hot 100 Playlist Generator')
    # Prompt the user for a date
    date = st.text_input("What year do you want to travel to? Type the date in this format YYYY-MM-DD?\n")

    if date:
        # Fetch the Billboard Hot 100 songs for the specified date
        songs = get_billboard_top_100(date)

        # Authenticate with Spotify
        sp = authenticate_spotify()
        if sp:
            # Get the current user's Spotify ID
            user_id = sp.current_user()["id"]

            # Create a new playlist on Spotify
            playlist_id = create_playlist(sp, user_id, date)
            song_uris = []

            # Get the URIs of the songs and collect them in a list
            for song in songs:
                uri = get_song_uri(sp, song)
                if uri:
                    song_uris.append(uri)

            # Add songs to the playlist in batches of 100 (due to Spotify API limit)
            for i in range(0, len(song_uris), 100):
                sp.playlist_add_items(playlist_id, song_uris[i:i + 100])

            st.success(f"Playlist '{playlist_id}' created and songs added!")


if __name__ == "__main__":
    main()
