class Queue:
    def __init__(self, spotify, artists):
        self.spotify = spotify
        self.artists = artists
        self.queue

    @property
    def queue(self):
        print("\n\033[4mQueue:\033[0m")
        for [index, queue] in enumerate(self.spotify.queue()['queue'], 1):
            print(f"{str(index).zfill(2)}) {queue['name']} [{self.artists}]")
        return None
