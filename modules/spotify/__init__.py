from modules.spotify.status import Status
from core.modules import Modules
from spotipy import Spotify, SpotifyOAuth
from webbrowser import open_new_tab
from modules.spotify.status import Status


def credentials(module: object) -> bool:
    module.set_credential(key='client_id', value=input("client_id >> "))
    module.set_credential(key='client_secret', value=input("client_secret >> "))
    module.set_credential(key='callback_url', value=input("callback_url >> "))
    return test_connection(module=module, is_temp=True)


def test_connection(module: object, is_temp=True) -> bool:
    client_id = module.temp_credentials['client_id'] if is_temp else module.get_credential('client_id')
    client_secret = module.temp_credentials['client_secret'] if is_temp else module.get_credential('client_secret')
    callback_url = module.temp_credentials['callback_url'] if is_temp else module.get_credential('callback_url')
    try:
        # Attempt to create a Spotify object with the provided credentials
        Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=callback_url,
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
        if is_temp:
            print("Credentials are correct.")
        return True
    except Exception as e:
        print(
            f"\n{e}\nPlease retry !\n")
        return False


def run(parameters: dict):
    module = Modules(module=parameters['name'])
    if not parameters['initialized'] or not test_connection(module=module, is_temp=False):
        module.empty_credential()
        open_new_tab("https://developer.spotify.com/dashboard")
        print('Welcome to the initial setup of Spotify for DeckMaster')
        print(
            "Go to https://developer.spotify.com/dashboard for creating an app.\n"
            "Also don't forget to set a callback_url !\n"
            "For more facility, set http://localhost:8000"
        )
        print('----------------------------')
        while not credentials(module=module):
            pass
        module.save()
    Status(module=module)
