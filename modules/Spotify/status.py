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


class Status:
    """
    Class to handle Spotify status updates.
    """

    def __init__(self, credential):
        """
        Description:
        Save the most needed information. Read variables for better understanding

        Variables:
        self.client_id      :str:       -> Client ID obtained from the credential class
        self.secret_id      :str:       -> Secret ID obtained from the credential class
        self.redirect_uri   :str:       -> Callback URL obtained from the credential class
        self.last_title     :str:       -> Title of the current track. Used to avoid
                                            multiple loops in a short time.
        self.spotify        :obj:       -> Object obtained from the Spotify API Library.
                                            Contains a token that allows communication
                                            with the Spotify server and scope for permissions.
        self.account        :obj:       -> Contrain all need about current user for the self.action(str) method (userinfo)
        self.data           :obj:       -> Variable filled in the update_data method.
                                            Contains all data related to the current playing state
        """
        self.client_id = credential['client_id']
        self.client_secret = credential['client_secret']
        self.redirect_uri = credential['callback_url']
        self.last_title = None
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
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
        self.data = None
        self.main()

    def action(self, word):
        """
        All actions will be played here. Pauses, resumes, skip, etc...
        An object attributed to commands will be manually created and will contain some instructions for the final user.

        Message for devs: Bcs I have a premium version of Spotify, will you change the None value of premium for each command
        in commands by True or False ? (True if premium needed or False if not). How to know it ? Simple ! Run any instruction
        and if you got an error by the raise instruction, you will read premium need in logs...

        For the moment, event wait a letter (use with keyboard), but in next releases,
        we gona use id or this kind of things.
        """
        need_premium = "You have to be Premium for this action"
        played = self.spotify.current_user_playing_track()['is_playing']
        premium = self.spotify.current_user()['product'] == 'premium'
        commands = {
            "help": {
                "help": "Show this help menu !",
                "usage": "help",
                "premium": False
            },
            "pause": {
                "help": "Set the player to pause !",
                "usage": "pause",
                "premium": True
            },
            "resume": {
                "help": "Set the player to play after a pause !",
                "usage": "resume",
                "premium": True
            },
            "queue": {
                "help": "Show the current queue !",
                "usage": "queue",
                "premium": None
            },
            "now": {
                "help": "Show what currently playing !",
                "usage": "now",
                "premium": False
            },
            "favorite": {
                "help": "Add (if not added) or delete (if even added) the current song from one of your playlist !",
                "usage": "favorite <list_name>",
                "premium": None
            },
            "userinfo": {
                "help": "Show informations about current user !",
                "usage": "userinfo",
                "premium": False
            },
            "next": {
                "help": "Skip the current track to the next track of the queue...",
                "usage": "next",
                "premium": None
            },
            "previous": {
                "help": "Skip the current track to the previous track...",
                "usage": "previous",
                "premium": None
            },
            "volume": {
                "help": "Change the volume of the player !",
                "usage": "volume <percent>",
                "premium": None
            }
        }
        """
        Information: When running it, self.data will be updated ! So all self.data are updated in the commands here !
        """
        self.update_data()

        if word == 'help':
            for command in commands:
                print(
                    f"\033[4m[{command}]:\033[0m\n - Info: {commands[command]['help']}\n - Usage: {commands[command]['usage']}\n - Premium: {commands[command]['premium']}\n")
            return True

        elif word == 'pause':
            if premium and played:
                self.spotify.pause_playback()
                return True
            elif premium and not played:
                print("Already paused...")
                return True
            else:
                print(need_premium)
                return True

        elif word == 'resume':
            if premium and not played:
                self.spotify.start_playback()
                return True
            elif premium and not played:
                print("Already playing...")
                return True
            else:
                print(need_premium)
                return True

        elif word == 'queue':
            if premium:
                print("\n--------------------------------------")
                for [index, queue] in enumerate(self.spotify.queue()['queue'], 1):
                    print(f"{str(index).zfill(2)}) {queue['name']} [{queue['artists'][0]['name']}]")
                print("--------------------------------------\n")
                return True
            else:
                print(need_premium)
                return True

        elif word == 'now':
            release_date = str(self.data['item']['album']['release_date'])
            release_year = release_date.split('-', maxsplit=1)[0]
            print("\n--------------------------------------")
            print(
                f"Title: {self.data['item']['name']}\n"
                f"Artist: {self.data['item']['artists'][0]['name']}\n"
                f"Cover: {self.data['item']['album']['images'][0]['url']}\n"
                f"Release Year: {release_year}\n"
                f"Length: {str((self.data['item']['duration_ms'] // 1000) // 60).zfill(2)}:{str((self.data['item']['duration_ms'] // 1000) % 60).zfill(2)}\n"
                f"Progress: {str((self.data['progress_ms'] // 1000) // 60).zfill(2)}:{str((self.data['progress_ms'] // 1000) % 60).zfill(2)}"
                f"\n--------------------------------------\n"
            )
            return True

        elif word.split(' ')[0] == 'favorite':
            if len(word.split(' ')) < 2:
                """
                If the final user don't enter the command and the playlist name, it will make the script bug...
                """
                print("You need to give a playlist name with the favorite command...")
                return False
            for playlist in self.spotify.current_user_playlists()['items']:
                """
                We browse all playlists object...
                """
                if " ".join(word.split(' ')[1:]) == playlist['name']:
                    """
                    Because we split word, we join it to can compare with playlist names we browse!
                    """
                    for [index, track] in enumerate(self.spotify.playlist_items(playlist['id'])['items']):
                        if track['track']['uri'] == self.data['item']['uri']:
                            print(f"{self.data['item']['name']} has been removed from {' '.join(word.split(' ')[1:])}")
                            self.spotify.playlist_remove_specific_occurrences_of_items(playlist['id'], [
                                {"uri": track['track']['id'], "positions": [index]}])
                            return True
                    print(f"{self.data['item']['name']} has been added in {' '.join(word.split(' ')[1:])}...")
                    self.spotify.playlist_add_items(playlist['id'], [self.data['item']['uri']])
                    return True
            print(f"Playlist {' '.join(word.split(' ')[1:])} not found.\nUse help if you need help.")
            return False

        elif word == 'userinfo':
            print("\n--------------------------------------")
            print(f"User: {self.account['display_name']}")
            print(f"Image: {self.account['images'][0]['url']}")
            print(f"Type of account: {'Free' if self.account['product'] == 'free' else 'Premium'}")
            print("--------------------------------------\n")

        elif word == 'next':
            if premium:
                self.spotify.next_track()
                return True
            else:
                print(need_premium)
                return False

        elif word == 'previous':
            if premium:
                self.spotify.previous_track()
                return True
            else:
                print(need_premium)
                return False

        elif word.split(' ')[0] == 'volume':
            if len(word.split(' ')) < 2:
                print("You need to give a volume value in percent...")
                return False
            if '%' in word.split(' ')[1]:
                integer = int(word.split(' ')[1].replace('%', ''))
            else:
                integer = int(word.split(' ')[1])
            if integer > 100 or integer < 0:
                print("Volume must be between 0 and 100")
                return False
            if type(integer).__name__ == 'int':
                self.spotify.volume(integer)
                return True

        else:
            print(f"Command {word} not known...")
            return False

    def update_data(self):
        """
        Update the self.data variable with the current track's status.
        """
        while self.spotify.current_user_playing_track() is None:
            print("DeckMaster listening for update...")
            sleep(3)
        self.data = self.spotify.current_user_playing_track()
        return self.data

    def main(self):
        """
        Main method
        """
        while True:
            self.action(input('action> '))
