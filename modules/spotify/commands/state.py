class State:
    def __init__(self, arg, spotify):
        self.spotify = spotify
        if arg == 'pause':
            self.pause
        elif arg == 'resume':
            self.resume
        elif arg == 'skip':
            self.skip
        elif arg == 'previous':
            self.previous
        else:
            return print(f"{arg} don't exist !\nPlease use: help")

    @property
    def is_playing(self):
        return self.spotify.current_user_playing_track()['is_playing']

    @property
    def pause(self):
        if self.is_playing:
            print("\nTrack has been paused...\n")
            return self.spotify.pause_playback()
        else:
            print("\nTrack already paused...\n")
        return None

    @property
    def resume(self):
        if not self.is_playing:
            print("\nTrack has been resumed...\n")
            self.spotify.start_playback()
        else:
            print("\nTrack already playing...\n")
        return None

    @property
    def skip(self):
        self.spotify.next_track()
        return None

    @property
    def previous(self):
        self.spotify.previous_track()
        return None
