import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Credentials and callback url declaration
client_id = "client_id"
client_secret = "client_secret"
redirect_uri = "http://localhost:8000"

# var who avoir a loop more of one time while the same tracks is played
last_title = 'Empty'

# Create the object for listening the current user !
# If you meet a problem add scope="user-read-currently-playing" after redirect_uri
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri))

# call the method current_user_playing_track()
while True:
    results = sp.current_user_playing_track()
    if last_title != results['item']['name']:
        last_title = results['item']['name']
        time = results['progress_ms'] // 1000
        print(f"Titre: {results['item']['name']}\n"
              f"Artiste: {results['item']['artists'][0]['name']}\n"
              f"Temps: {str(time // 60).zfill(2)}:{str(time % 60).zfill(2)}\n"
              f"Affiche: {results['item']['album']['images'][0]['url']}\n"
              f"Année de sortie: {str(results['item']['album']['release_date']).split('-')[0]}\n"
              f"--------------------------------------\n")
