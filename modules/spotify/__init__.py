from core.api import app
from core.modules import Modules
from modules.spotify.commands.state import State
from modules.spotify.commands.now import Now
from spotipy import Spotify, SpotifyOAuth
from core.system import System


def trad(key: str):
    System().show_traduction(key=key, module="spotify")


class SpotifySocket:
    def __init__(self):
        print("Module Spotify initialisé")
        self.socket = None

    def create_socket(self):
        module = Modules()
        module.module = "spotify"
        credentials = module.credentials(module="spotify")
        self.socket = Spotify(
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
        )


spotify = SpotifySocket()
spotify.create_socket()
controleur = State(spotify=spotify.socket)


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
    module.set_key(module="spotify", key="callback_url", value=callback_url)
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


@app.get(
    path="/spotify/status/pause",
    name=trad(key="pause_name"),
    description=trad(key="pause_desc"),
    tags=["Spotify"]
)
async def spotify_pause():
    controleur.action(arg="pause")
    return {
        "message": "Lecture mise en pause !"
    }


@app.get(
    path="/spotify/status/resume",
    name=trad(key="resume_name"),
    description=trad(key="resume_desc"),
    tags=["Spotify"]
)
async def spotify_pause():
    controleur.action(arg="resume")
    return {
        "message": "Lecture remise en lecture !"
    }


@app.get(
    path="/spotify/status/next",
    name=trad(key="next_name"),
    description=trad(key="next_desc"),
    tags=["Spotify"]
)
async def spotify_pause():
    controleur.action(arg="skip")
    return {
        "message": "Passer au prochain morceau !"
    }


@app.get(
    path="/spotify/status/previous",
    name=trad(key="previous_name"),
    description=trad(key="previous_desc"),
    tags=["Spotify"])
async def spotify_pause():
    controleur.action(arg="previous")
    return {
        "message": "Réecouter le morceau précédent !"
    }


@app.get(
    path="/spotify/now",
    name=trad(key="now_name"),
    description=trad(key="now_desc"),
    tags=["Spotify"]
)
async def spotify_now():
    return Now(spotify=spotify.socket).now()
