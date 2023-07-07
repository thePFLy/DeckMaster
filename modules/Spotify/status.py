"""
This script allows getting the status of the Spotify service.

Needed:
    - spotipy: Python package to connect to the Spotify API
    - argparse: Library for parsing command-line arguments
    - time: Allows pausing the program

Usage:
    - View help arg
"""
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from keyboard import on_press


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
                                            with the Spotify server.
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
                scope=["user-read-currently-playing", "user-read-private"]
            )
        )
        self.account = self.spotify.current_user()
        self.data = None
        self.main()

    def action(self, event):
        """
        All actions will be played here. For the moment, event wait a letter (use with keyboard), but in next releases,
        we gona use id or this kind of things.
        """
        if event.name == 'p':
            need_premium = "You have to be Premium for this action"

            if self.spotify.current_user()['product'] == 'Premium':
                self.spotify.pause_playback()
            else:
                print(need_premium)

    def update_data(self):
        """
        Update the self.data variable with the current track's status.
        """
        while self.spotify.current_user_playing_track() is None:
            print("DeckMaster listening for update...")
            sleep(5)
        self.data = self.spotify.current_user_playing_track()
        return self.data

    def main(self):
        """
        Main method to continuously update and print the current track's status.
        """
        print(f"User: {self.account['display_name']}")
        print(f"Image: {self.account['images'][0]['url']}")
        print(f"Type of account: {'Free' if self.account['product'] == 'free' else 'Premium'}")
        print("--------------------------------------\n\n")
        print()
        while True:
            sleep(2)
            self.update_data()
            if self.last_title != self.data['item']['name']:
                on_press(self.action)
                self.last_title = self.data['item']['name']
                release_date = str(self.data['item']['album']['release_date'])
                release_year = release_date.split('-', maxsplit=1)[0]
                print(
                    f"Title: {self.data['item']['name']}\n"
                    f"Artist: {self.data['item']['artists'][0]['name']}\n"
                    f"Cover: {self.data['item']['album']['images'][0]['url']}\n"
                    f"Release Year: {release_year}\n"
                    f"Length: {(self.data['item']['duration_ms'] // 1000) // 60}:{(self.data['item']['duration_ms'] // 1000) % 60}"
                    f"\n\n--------------------------------------\n\n"
                )
