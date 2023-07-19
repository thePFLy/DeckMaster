class Volume:
    def __init__(self, arg, spotify):
        self.arg = arg
        self.spotify = spotify
        self.volume

    @property
    def volume(self):
        if self.arg == 'volume':
            print("You need to give a volume value in percent...")
            return None

        elif len(self.arg) > 1:
            if '%' in self.arg[1]:
                integer = int(self.arg[1].replace('%', ''))
            else:
                integer = int(self.arg[1])
            if integer > 100 or integer < 0:
                print("Volume must be between 0 and 100")
            if type(integer).__name__ == 'int':
                self.spotify.volume(integer)
                print(f'Volume set to {integer}% !')
        return None
