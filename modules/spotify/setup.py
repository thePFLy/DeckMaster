from spotipy import Spotify, SpotifyOAuth
from core.system import System


def trad(key: str):
    System().show_traduction(key=key, module="spotify")


def try_init(credentials: dict) -> bool:
    try:
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


def setup():
    return trad(key="setup_message")