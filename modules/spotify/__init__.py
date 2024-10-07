def load():
    from core.api import app
    from core.modules import Modules
    from modules.spotify.commands.state import State
    from modules.spotify.commands.now import Now
    from modules.spotify.commands.playlists import Playlists
    from modules.spotify.commands.userinfo import Userinfo
    from modules.spotify.commands.volume import Volume
    from spotipy import Spotify, SpotifyOAuth
    from core.system import System

    def trad(key: str):
        return System().show_traduction(key=key, module="spotify")

    class SpotifySocket:
        def __init__(self):
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

    @app.get(
        path="/spotify/status/pause",
        name=trad(key="pause_name"),
        description=trad(key="pause_desc"),
        tags=["Spotify"]
    )
    async def spotify_pause():
        State(spotify=spotify).pause()
        return {
            "message": "Lecture mise en pause !"
        }

    @app.get(
        path="/spotify/status/resume",
        name=trad(key="resume_name"),
        description=trad(key="resume_desc"),
        tags=["Spotify"]
    )
    async def spotify_resume():
        State(spotify=spotify).resume()
        return {
            "message": "Lecture remise en lecture !"
        }

    @app.get(
        path="/spotify/status/next",
        name=trad(key="next_name"),
        description=trad(key="next_desc"),
        tags=["Spotify"]
    )
    async def spotify_next():
        State(spotify=spotify).skip()
        return {
            "message": "Passer au prochain morceau !"
        }

    @app.get(
        path="/spotify/status/previous",
        name=trad(key="previous_name"),
        description=trad(key="previous_desc"),
        tags=["Spotify"])
    async def spotify_previous():
        State(spotify=spotify).previous()
        return {
            "message": "Réecouter le morceau précédent !"
        }

    @app.get(
        path="/spotify/status/seek",
        name=trad(key="seek_name"),
        description=trad(key="previous_desc"),
        tags=["Spotify"]
    )
    async def seek(seconds: str):
        State(spotify=spotify).change_position(seconds)
        return {
            "message": "Déplacement effectué"
        }

    @app.get(
        path="/spotify/now",
        name=trad(key="now_name"),
        description=trad(key="now_desc"),
        tags=["Spotify"]
    )
    async def spotify_now():
        return Now(spotify=spotify).now()

    @app.get(
        path="/spotify/playlists/list",
        name=trad(key="playlist_list_name"),
        description=trad(key="playlist_list_desc"),
        tags=["Spotify"]
    )
    async def list_playlists(details: bool = False):
        return Playlists(spotify=spotify).list_playlists(details=details)

    @app.get(
        path="/spotify/playlist/show_content",
        name=trad(key="playlist_show_content_name"),
        description=trad(key="playlist_show_content_desc"),
        tags=["Spotify"]
    )
    async def show_playlist_content(playlist_id: str, details: bool = False):
        return Playlists(spotify=spotify).list_playlist_content(playlist_id=playlist_id, details=details)

    @app.get(
        path="/spotify/playlist/add_track",
        name=trad(key="playlist_add_track_name"),
        description=trad(key="playlist_add_track_desc"),
        tags=["Spotify"]
    )
    async def add(playlist_id: str):
        return Playlists(spotify=spotify).add_to_playlist(playlist_id=playlist_id)

    @app.get(
        path="/spotify/playlist/delete_track",
        name=trad(key="playlist_delete_track_name"),
        description=trad(key="playlist_delete_track_desc"),
        tags=["Spotify"]
    )
    async def delete(playlist_id: str):
        return Playlists(spotify=spotify).delete_from_playlist(playlist_id=playlist_id)

    @app.get(
        path="/spotify/playlist/get_id",
        name=trad(key="playlist_get_id_name"),
        description=trad(key="playlist_get_id_desc"),
        tags=["Spotify"]
    )
    async def get_id(playlist_name: str):
        return Playlists(spotify=spotify).get_playlist_id(playlist_name=playlist_name)

    @app.get(
        path="/spotify/playlist/create",
        name=trad(key="playlist_create_name"),
        description=trad(key="playlist_create_desc"),
        tags=["Spotify"]
    )
    async def create(name: str, public: bool = True):
        return Playlists(spotify=spotify).create_playlist(name=name, public=public)

    @app.get(
        path="/spotify/playlist/delete",
        name=trad(key="playlist_delete_name"),
        description=trad(key="playlist_delete_desc"),
        tags=["Spotify"]
    )
    async def delete(playlist_id: str):
        return Playlists(spotify=spotify).delete_playlist(playlist_id=playlist_id)

    @app.get(
        path="/spotify/playlist/edit",
        name=trad(key="playlist_edit_name"),
        description=trad(key="playlist_edit_desc"),
        tags=["Spotify"]
    )
    async def edit(playlist_id: str, name: str, public: bool):
        return Playlists(spotify=spotify).edit_playlist(playlist_id=playlist_id, name=name, public=public)

    @app.get(
        path="/spotify/queue",
        name=trad(key="queue_name"),
        description=trad(key="queue_desc"),
        tags=["Spotify"]
    )
    async def queue(details: bool = False):
        return Playlists(spotify=spotify).queue(details=details)

    @app.get(
        path="/spotify/user_info",
        name=trad(key="user_name"),
        description=trad(key="user_desc"),
        tags=["Spotify"]
    )
    async def user_info():
        return Userinfo(spotify=spotify).userinfo()

    @app.get(
        path="/spotify/volume/set_level",
        name=trad(key="volume_name"),
        description=trad(key="volume_desc"),
        tags=["Spotify"]
    )
    async def volume(level_vol: int):
        if 0 > level_vol > 100:
            return "VOLUME_NOT_BETWEEN_0_AND_100"
        else:
            return Volume(spotify=spotify).volume(level=level_vol)
