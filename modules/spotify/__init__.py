from core.api import app
from core.modules import Modules
from modules.spotify.commands.state import State
from spotipy import Spotify, SpotifyOAuth


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


@app.get(path="/spotify/set_credentials", name="Re-définir les credentials Spotify", tags=["Spotify"])
async def spotify_set_credentials(client_id: str, client_secret: str, callback_url: str):
    """
    Permet de re-définir les credentials de Spotify via des requêtes GET !
    """
    module = Modules()
    module.module = "spotify"
    module.set_key(key="client_id", value=client_id)
    module.set_key(key="client_secret", value=client_secret)
    module.set_key(key="callback_url", value=callback_url)
    return {
        "response": "Success ! Credentials has been set !"
    }


@app.get(path="/spotify/get_credentials", name="Vérifier les credentials Spotify", tags=["Spotify"])
async def spotify_get_credentials():
    """
    Permet de vérifier la valeur des credentials spotify via réponse GET
    """
    module = Modules()
    module.module = "spotify"
    return module.credentials()


@app.get(path="/spotify/status/pause", name="Mettre la lecture en pause", tags=["Spotify"])
async def spotify_pause():
    controleur.action(arg="pause")
    return {
        "message": "Lecture mise en pause !"
    }


@app.get(path="/spotify/status/resume", name="Mettre la lecture en lecture", tags=["Spotify"])
async def spotify_pause():
    controleur.action(arg="resume")
    return {
        "message": "Lecture remise en lecture !"
    }


@app.get(path="/spotify/status/next", name="Passer au prochain morceau", tags=["Spotify"])
async def spotify_pause():
    controleur.action(arg="skip")
    return {
        "message": "Passer au prochain morceau !"
    }


@app.get(path="/spotify/status/previous", name="Réecouter le morceau précédent", tags=["Spotify"])
async def spotify_pause():
    controleur.action(arg="previous")
    return {
        "message": "Réecouter le morceau précédent !"
    }
