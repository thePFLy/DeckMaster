"""
This script allows getting the status of the Spotify service.

Needed:
    - spotipy: Python package to connect to the Spotify API
    - argparse: Library for parsing command-line arguments
    - time: Allows pausing the program

Usage:
    - View help arg
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
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
                scope="user-read-currently-playing"
            )
        )
        self.data = None
        self.main()

    def update_data(self):
        """
        Update the self.data variable with the current track's status.
        """
        self.data = self.spotify.current_user_playing_track()
        return self.data

    def main(self):
        """
        Main method to continuously update and print the current track's status.
        """
        while True:
            sleep(2)
            self.update_data()
            if self.last_title != self.data['item']['name']:
                self.last_title = self.data['item']['name']
                release_date = str(self.data['item']['album']['release_date'])
                release_year = release_date.split('-', maxsplit=1)[0]
                print(
                    f"Title: {self.data['item']['name']}\n"
                    f"Artist: {self.data['item']['artists'][0]['name']}\n"
                    f"Cover: {self.data['item']['album']['images'][0]['url']}\n"
                    f"Release Year: {release_year}\n"
                    f"--------------------------------------\n"
                )


if __name__ == '__main__':
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description='''
        Help description\n
        ----------------------\n
        1. Create a Spotify developer app\n
        2. Load secrets\n
        3. Get status\n
        ''')
