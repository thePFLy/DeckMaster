from spotipy import Spotify, SpotifyOAuth


def setup():
    print('Welcome to the initial setup of Spotify for DeckMaster')
    print(
        "Go to https://developer.spotify.com/dashboard for creating an app.\n"
        "Also don't forget to set a callback_url !\n"
        "For more facility, set http://localhost:8000"
    )
    print('----------------------------')


def try_init(credentials: dict, setup_mode: bool = False) -> bool:
    try:
        setup() if setup_mode else None
        Spotify(
            auth_manager=SpotifyOAuth(
                client_id=credentials["client_id"],
                client_secret=credentials["client_secret"],
                redirect_uri=credentials["redirect_uri"],
                scope=[
                    "user-read-currently-playing",
                    "user-read-private",
                    "user-read-playback-state",
                    "app-remote-control",
                    "streaming",
                    "playlist-read-private",
                    "playlist-modify-private",
                    "playlist-modify-public"
                ]
            )
        ).me()
        return True
    except:
        return False
