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

    def __init__(self, module: object):
        """
        Create a instance between Spotify and DeckMaster
        @param credential: It's a simple dictionnary
        """
        self.last_title = None
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=module.get_credential('client_id'),
                client_secret=module.get_credential('client_secret'),
                redirect_uri=module.get_credential('callback_url'),
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

    def action(self, word: str) -> None:
        """
        @param word: A key word to execute a instruction
        @return: None, just to said that nothing has to been returned
        """
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
        #  Here would be written conditions    #
        #  to call actions for Spotify_CLI     #
        ########################################

        if arg in ['pause', 'resume', 'skip', 'previous']:
            if self.premium:
                control.State(
                    arg=arg,
                    spotify=self.spotify
                )
            else:
                print(need_premium)

        elif arg == 'queue':
            if self.premium:
                control.Queue(
                    spotify=self.spotify,
                    artists=self.artists
                )
            else:
                print(need_premium)

        elif arg == 'now':
            control.Now(
                spotify=self.spotify,
                artists=self.artists,
                data=self.data
            )

        elif is_list and arg[0] in ['favorite', 'playlist'] or arg in ['favorite', 'playlist']:
            control.Playlists(
                arg=arg,
                data=self.data,
                spotify=self.spotify,
                account=self.account
            )

        elif arg == 'userinfo':
            control.Userinfo(
                account=self.account
            )

        elif arg[0] == 'volume' or arg == 'volume':
            if self.premium:
                control.Volume(
                    arg=arg,
                    spotify=self.spotify
                )
            else:
                print(need_premium)

        else:
            print(f"Command {word} not known...")
            return False

    def update_data(self):
        """
        Update the self.data variable with the current track's status.
        @return: The data in himself. Partical if we need to save the value but use directly the result without recall
        the self.spotify variable
        """
        while self.spotify.current_user_playing_track() is None:
            print('No metadata has been got.\nNew try in 5 seconds...')
            sleep(5)
        self.data = self.spotify.current_user_playing_track()
        return self.data

    def main(self):
        """
        Main method, just a input command entry
        """
        self.update_data()
        control.Now(self.spotify, self.artists, self.data)
        while self.on_change():
            self.action(input('SpotCLI> '))

    def on_change(self):
        """
        This method will be used by the main() method;
        If there's no listeners, there's no need to have access to the CLI mod
        And simply, while the user will listen, you will come back in loop into the CLI entry.
        """
        if self.spotify.current_user_playing_track() is None:
            print("No listener...")
            sleep(3)
            return False
        # If the track is listened by the user, return True
        elif self.data['item']['uri'] == self.spotify.current_user_playing_track()['item']['uri']:
            return True
        # If the track is not listened by user, call the Now() method to print what is listened and return True
        elif self.data['item']['uri'] != self.spotify.current_user_playing_track()['item']['uri']:
            self.update_data()
            control.Now(self.spotify, self.artists, self.data)
            return True
        else:
            return True

    @property
    def artists(self):
        """
        Method used to just return a string for a more beautiful visual...
        @return: str
        """
        artists = []
        for artist in self.data['item']['artists']:
            artists.append(artist['name'])
        return ', '.join(artists)
