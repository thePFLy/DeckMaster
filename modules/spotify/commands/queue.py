class Queue:
    def __init__(self, spotify, artists):
        self.spotify = spotify
        self.artists = artists

    def queue(self):
        result = {}
        for [index, queue] in enumerate(self.spotify.queue()['queue'], 1):
            result[str(index).zfill] = f"{queue['name']} [{self.artists}]"
        return None