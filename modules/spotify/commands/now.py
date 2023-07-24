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

        print(
            f"Title: {self.data['item']['name']}\n"
            f"Artist: {self.artists}\n"
            f"Cover: {self.data['item']['album']['images'][0]['url']}\n"
            f"Release Year: {calculated_datas['year']}\n"
            f"Length: {calculated_datas['duration']['minutes']}:{calculated_datas['duration']['seconds']}\n"
            f"Progress: {calculated_datas['progress']['minutes']}:{calculated_datas['progress']['seconds']}"
        )
