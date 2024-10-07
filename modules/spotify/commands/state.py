class State:
    def __init__(self, spotify: object):
        self.spotify = spotify.socket

    def is_playing(self):
        return self.spotify.current_user_playing_track()['is_playing']

    def pause(self):
        return self.spotify.pause_playback() if self.is_playing() else None

    def resume(self):
        return self.spotify.start_playback() if not self.is_playing() else None

    def skip(self):
        return self.spotify.next_track()

    def previous(self):
        return self.spotify.previous_track()

    def change_position(self, seconds: int):
        sec = int(seconds)
        return self.spotify.seek_track(position_ms=int(sec * 1000))
