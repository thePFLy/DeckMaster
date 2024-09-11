class State:
    def __init__(self, spotify: object):
        self.spotify = spotify

    def action(self, arg: str):
        if arg == 'pause':
            return self.pause()
        elif arg == 'resume':
            return self.resume()
        elif arg == 'skip':
            return self.skip()
        elif arg == 'previous':
            return self.previous()
        else:
            return print(f"{arg} don't exist !")

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
