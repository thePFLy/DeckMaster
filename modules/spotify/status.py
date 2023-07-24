"""
This script allows getting the status of the Spotify service.

Needed:
    - spotipy: Python package to connect to the Spotify API
    - argparse: Library for parsing command-line arguments
    - time: Allows pausing the program
"""
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import modules.spotify.commands as control
from json import loads


class Status:
    """
    Class to handle Spotify status updates.
    """

    def __init__(self, credential):
        self.last_title = None
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=credential['client_id'],
                client_secret=credential['client_secret'],
                redirect_uri=credential['callback_url'],
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
        self.account = self.spotify.current_user()
        self.premium = self.account['product'] == 'premium'
        self.data = None
        self.main()

    @staticmethod
    def spotify_options():
        with open('modules/spotify/commands/help.json') as command:
            return loads(command.read())

    def action(self, word):
        need_premium = "You have to be Premium for this action"
        self.update_data()
        if len(word) == 0:
            print('No argument gived...')
            return None

        if len(word.strip().split(' ')) > 1:
            arg = word.strip().split(' ')
            is_list = True
        else:
            arg = word.strip()
            is_list = False

        ########################################
        #  Begin of commands                   #
        ########################################
        #  Here would be wrote all conditions  #
        #  to call actions for Spotify_CLI     #
        ########################################

        if is_list and arg[0] == 'help' or arg == 'help':
            control.Help(arg, self.spotify_options())

        elif arg in ['pause', 'resume', 'skip', 'previous']:
            if self.premium:
                control.State(arg, self.spotify)
            else:
                print(need_premium)

        elif arg == 'queue':
            if self.premium:
                control.Queue(self.spotify, self.artists)
            else:
                print(need_premium)

        elif arg == 'now':
            control.Now(self.spotify, self.artists, self.data)

        elif is_list and arg[0] in ['favorite', 'playlist'] or arg in ['favorite', 'playlist']:
            control.Playlists(arg, self.data, self.spotify, self.spotify_options(), self.account)

        elif arg == 'userinfo':
            control.Userinfo(self.account)

        elif arg[0] == 'volume' or arg == 'volume':
            if self.premium:
                control.Volume(arg, self.spotify)
            else:
                print(need_premium)

        else:
            print(f"Command {word} not known...")
            return False

    def update_data(self):
        """
        Update the self.data variable with the current track's status.
        """
        while self.spotify.current_user_playing_track() is None:
            print('No metadata has been got.\nNew try in 5 seconds...')
            sleep(5)
        self.data = self.spotify.current_user_playing_track()
        return self.data

    def main(self):
        """
        Main method
        """
        self.update_data()
        control.Now(self.spotify, self.artists, self.data)
        while self.on_change():
            self.action(input('SpotCLI> '))

    def on_change(self):
        if self.spotify.current_user_playing_track() is None:
            print("No listener...")
            sleep(3)
            return False
        elif self.data['item']['uri'] == self.spotify.current_user_playing_track()['item']['uri']:
            return True
        elif self.data['item']['uri'] != self.spotify.current_user_playing_track()['item']['uri']:
            self.update_data()
            control.Now(self.spotify, self.artists, self.data)
            return True
        else:
            return True

    @property
    def artists(self):
        artists = []
        for artist in self.data['item']['artists']:
            artists.append(artist['name'])
        return ', '.join(artists)
