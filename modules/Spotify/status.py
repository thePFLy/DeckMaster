import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep


class Status:
    def __init__(self, credential):
        """
        Description:
        Save the most needed information. Read variables for better understanding

        Variables:
        self.client_id      :str:       -> Client ID got from the credential class
        self.secret_id      :str:       -> Secret ID got from the credential class
        self.redirect_uri   :str:       -> Callback URL got from the credential class
        self.last_title     :str:       -> Title of the current track. Used for avoid multiple loop in short time.
        self.client_id      :str:       -> Client ID got from the credential class
        self.sp             :obj:       -> Object got from Spotify API Library. Contain a token who allow communication with
                                           Spotify server.
        self.data           :obj:       -> Variable filled in the update_data method. Contain all data related to the current playing state
        """
        self.client_id = credential['client_id']
        self.client_secret = credential['client_secret']
        self.redirect_uri = credential['callback_url']
        self.last_title = None
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope="user-read-currently-playing"
            )
        )
        self.data = None
        self.main()

    @property
    def update_data(self):
        """
        Description:
        Simply fill the self.data variable and return all curent's track status
        """
        self.data = self.sp.current_user_playing_track()
        return self.data

    def main(self):
        """
        Description:
        For the momennt we use a while, but asynchronous methods will be use into the nexts releases.
        Each 2 seconds, we update the current status playing by calling update_data.
        Once is done, and that the title has change, we print all information about current track
        """
        while True:
            sleep(2)
            self.update_data
            if self.last_title != self.data['item']['name']:
                self.last_title = self.data['item']['name']
                print(f"Titre: {self.data['item']['name']}\n"
                      f"Artiste: {self.data['item']['artists'][0]['name']}\n"
                      f"Affiche: {self.data['item']['album']['images'][0]['url']}\n"
                      f"Année de sortie: {str(self.data['item']['album']['release_date']).split('-')[0]}\n"
                      f"--------------------------------------\n")
