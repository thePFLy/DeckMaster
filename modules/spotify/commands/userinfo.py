class Userinfo:
    def __init__(self, spotify):
        self.spotify = spotify.socket

    def userinfo(self):
        return {
            "user_display": self.spotify.me()['display_name'],
            "picture": self.spotify.me()['images'][0]['url'],
            "account_type": 'Free' if self.spotify.me()['product'] == 'free' else 'Premium'
        }
