from core.api import app
from core.modules import Modules


@app.get(path="/spotify/set_credentials", name="Re-définir les credentials Spotify")
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


@app.get(path="/spotify/get_credentials", name="Vérifier les credentials Spotify")
async def spotify_get_credentials():
    """
    Permet de vérifier la valeur des credentials spotify via réponse GET
    """
    module = Modules()
    module.module = "spotify"
    return module.credentials()
