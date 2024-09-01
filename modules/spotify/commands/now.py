class Now:
    def __init__(self, spotify, artists, data):
        self.spotify = spotify
        self.artists = artists
        self.data = data
        self.now

    @property
    def now(self):
        print("\033[4mNow:\033[0m")
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
            "artist": self.artists,
            "url_cover": self.data['item']['album']['images'][0]['url'],
            "date_release": calculated_datas['year'],
            "length": f"{calculated_datas['duration']['minutes']}:{calculated_datas['duration']['seconds']}",
            "progress": f"{calculated_datas['progress']['minutes']}:{calculated_datas['progress']['seconds']}"
        }
