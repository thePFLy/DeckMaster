from spotipy import Spotify, SpotifyOAuth
from core.system import System
from core.api import app, update_swagger
from core.modules import Modules


def trad(key: str):
    return System().show_traduction(key=key, module="spotify")


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
        import_creds()
        return True
    except:
        return False


def setup():
    import_creds()
    return trad(key="setup_message")


def import_creds():
    @app.get(
        path="/spotify/set_credentials",
        name=trad(key="set_credentials_name"),
        description=trad(key="set_credentials_desc"),
        tags=["Spotify"]
    )
    async def spotify_set_credentials(client_id: str, client_secret: str, callback_url: str):
        module = Modules()
        module.module = "spotify"
        module.set_key(module="spotify", key="client_id", value=client_id)
        module.set_key(module="spotify", key="client_secret", value=client_secret)
        module.set_key(module="spotify", key="redirect_uri", value=callback_url)
        return {
            "response": "Success ! Credentials has been set !"
        }

    @app.get(
        path="/spotify/get_credentials",
        name=trad(key="get_credentials_name"),
        description=trad(key="get_credentials_desc"),
        tags=["Spotify"]
    )
    async def spotify_get_credentials():
        module = Modules()
        module.module = "spotify"
        return module.credentials(module="spotify")

    update_swagger()
