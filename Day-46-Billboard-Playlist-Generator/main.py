import requests
from bs4 import BeautifulSoup
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import time

# Spotify API credentials (Store these securely)
CLIENT_ID = "9c467e2cb4b04af6a178d759e923b911"
CLIENT_SECRET = "a33aea5b6b0e4aed91fdf8a728cd7ec5"
REDIRECT_URI = "http://localhost:8080"  # Use localhost for Streamlit
SCOPE = "playlist-modify-private user-read-private"

def get_billboard_top_100(date):
    """Fetches the Billboard Hot 100 songs for a given date."""
    url = f"https://www.billboard.com/charts/hot-100/{date}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        st.error(f"Failed to fetch Billboard data: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting song names
    songs = [song.getText().strip() for song in soup.select("h3#title-of-a-story")]
    
    # Extracting artist names
    artists = [artist.getText().strip() for artist in soup.select("span.c-label")]

    # Ensure song and artist lists are the same length
    return list(zip(songs[:100], artists[:100]))

def authenticate_spotify():
    """Authenticates the user with Spotify and returns a Spotify client object."""
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True
    )

    auth_url = sp_oauth.get_authorize_url()
    st.write(f"[Click here to authorize Spotify]({auth_url})")

    # Capture user input
    response = st.text_input("Enter the redirected URL after authorization:", "")

    if response:
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
        return Spotify(auth=token_info["access_token"]) if token_info else None
    return None

def create_playlist(sp, user_id, date):
    """Creates a new private playlist on Spotify."""
    try:
        playlist = sp.user_playlist_create(user=user_id, name=f"Billboard Hot 100 - {date}", public=False)
        return playlist["id"]
    except Exception as e:
        st.error(f"Error creating playlist: {e}")
        return None

def get_song_uri(sp, song_name, artist_name):
    """Searches for a song on Spotify by name and artist, returning its URI."""
    query = f"track:{song_name} artist:{artist_name}"
    
    try:
        results = sp.search(q=query, limit=1, type="track")
        tracks = results["tracks"]["items"]
        return tracks[0]["uri"] if tracks else None
    except Exception as e:
        st.warning(f"Error searching for {song_name}: {e}")
        return None

def main():
    """Main workflow for generating a Spotify playlist from Billboard Hot 100."""
    st.title("🎵 Billboard Hot 100 to Spotify Playlist 🎵")

    date = st.text_input("Enter the date (YYYY-MM-DD):")
    
    if date:
        st.write("Fetching Billboard Hot 100 songs...")
        songs = get_billboard_top_100(date)
        
        if not songs:
            st.error("No songs found! Ensure the date is valid (e.g., 2000-12-01).")
            return
        
        sp = authenticate_spotify()
        if not sp:
            st.error("Spotify authentication failed!")
            return
        
        user_id = sp.current_user()["id"]
        playlist_id = create_playlist(sp, user_id, date)
        if not playlist_id:
            return
        
        song_uris = []
        for song, artist in songs:
            uri = get_song_uri(sp, song, artist)
            if uri:
                song_uris.append(uri)
        
        if not song_uris:
            st.error("No valid songs found on Spotify.")
            return

        # Add songs in batches of 100
        for i in range(0, len(song_uris), 100):
            sp.playlist_add_items(playlist_id, song_uris[i:i + 100])
            time.sleep(1)  # Avoid hitting rate limits

        st.success(f"✅ Playlist created successfully! [View on Spotify](https://open.spotify.com/playlist/{playlist_id})")

if __name__ == "__main__":
    main()
