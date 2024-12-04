class Volume:
    def __init__(self, spotify):
        self.spotify = spotify.socket

    def volume(self, level: int):
        self.spotify.volume(volume_percent=level)
        return "VOLUME_SET"
