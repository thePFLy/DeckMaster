class Now:
    def __init__(self, spotify):
        self.spotify = spotify.socket
        self.data = self.spotify.current_user_playing_track()

    def get_artists(self):
        artists = []
        for artist in self.data['item']['artists']:
            artists.append(artist['name'])
        return ', '.join(artists)

    def now(self):
        calculated_datas = {
            "year": str(self.data['item']['album']['release_date']).split('-', maxsplit=1)[0],
            "duration": {
                "minutes": str((self.data['item']['duration_ms'] // 1000) // 60).zfill(2),
                "seconds": str((self.data['item']['duration_ms'] // 1000) % 60).zfill(2)
            },
            "progress": {
                "minutes": str((self.data['progress_ms'] // 1000) // 60).zfill(2),
                "seconds": str((self.data['progress_ms'] // 1000) % 60).zfill(2)
            }
        }

        return {
            "title": self.data['item']['name'],
            "artist": self.get_artists(),
            "url_cover": self.data['item']['album']['images'][0]['url'],
            "date_release": calculated_datas['year'],
            "length": f"{calculated_datas['duration']['minutes']}:{calculated_datas['duration']['seconds']}",
            "progress": f"{calculated_datas['progress']['minutes']}:{calculated_datas['progress']['seconds']}"
        }
