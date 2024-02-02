class Playlists:
    def __init__(self, arg, data, spotify, account):
        self.arg = arg
        self.spotify = spotify
        self.data = data
        self.playlist_name = None
        self.account = account

        if type(self.arg).__name__ == 'list':
            if self.arg[0] == 'favorite':
                self.playlist_name = ' '.join(self.arg[1:])
                self.add_to_playlist()
            elif self.arg[0] == 'playlist' and self.arg[1] in ['create', 'delete', 'list']:
                if self.arg[1] == 'create':
                    if len(self.arg) < 3:
                        print("You need to give a name to the playlist to create.\n")
                        return None
                    else:
                        self.playlist_name = ' '.join(self.arg[2:])
                        self.create()
                elif self.arg[1] == 'list':
                    self.list()
                elif self.arg[1] == 'delete':
                    self.playlist_name = ' '.join(self.arg[2:])
                    self.delete()
            else:
                print(f'{" ".join(arg)} is not a known command...')
                return None
        else:
            if self.arg == 'favorite':
                print(f'{arg} need as second argument a playlist name.\n')
            elif self.arg == 'playlist':
                print(f'{arg} need as second argument an action instruction.\n')

    def playlist(self, playlist_name):
        response = {
            "response": None,
            "id": None
        }
        for playlist in self.spotify.current_user_playlists()['items']:
            if playlist['name'] == playlist_name:
                response['response'] = True
                response['id'] = playlist['id']
                return response
        response['response'] = False
        return response

    def in_playlist(self, playlist_id, uri):
        response = {
            "response": None,
            "position": None
        }
        for [index, track] in enumerate(self.spotify.playlist_items(playlist_id, limit=None)['items']):
            if track['track']['uri'] == uri:
                response['response'] = True
                response['position'] = index
                return response
        else:
            response['response'] = False
            return response

    def add_to_playlist(self):
        if self.arg == 'favorite':
            print("You need to give a playlist name with the favorite command...")
            return False

        elif len(self.arg) < 3:
            if self.playlist(self.playlist_name)['response']:
                if self.in_playlist(self.playlist(self.playlist_name)['id'], self.data['item']['uri'])['response']:
                    print(f'{self.data["item"]["name"]} is already in {self.playlist_name}...')
                    if input(f'Remove it from {self.playlist_name} (y/Y): ').capitalize() == 'Y':
                        self.spotify.playlist_remove_specific_occurrences_of_items(
                            self.playlist(self.playlist_name)['id'],
                            [{
                                "uri": self.data['item']['id'],
                                "positions": [
                                    int(self.in_playlist(self.playlist(self.playlist_name)['id'],
                                                         self.data['item']['uri'])['position'])
                                ]
                            }]
                        )
                        return print(f'{self.data["item"]["name"]} has been removed from {self.playlist_name}...')
                    else:
                        print(f'{self.data["item"]["name"]} has not been removed from {self.playlist_name}...')
                        return None
                else:
                    print(f'{self.data["item"]["name"]} is not added in {self.playlist_name}...')
                    if input(f'Add it in {self.playlist_name} (y/Y): ').capitalize() == 'Y':
                        self.spotify.playlist_add_items(self.playlist(self.playlist_name)['id'],
                                                        [self.data['item']['uri']])
                        return print(f'{self.data["item"]["name"]} has been added in {self.playlist_name}...')
                    else:
                        print(f'{self.data["item"]["name"]} has not been added in {self.playlist_name}...')
                        return None
            else:
                print(f"The playlist {self.playlist_name} don't exist...")
                return None

    def create(self):
        if self.playlist(self.playlist_name)['response']:
            print(f'Playlist: {self.playlist_name} already exist.\nPlease choose an another name...')
            return None
        else:
            public = input('Do you want that this playlist become public (y/Y): ').capitalize() == 'Y'
            print(f"Playlist {self.playlist_name} created...")
            self.spotify.user_playlist_create(name=self.playlist_name, public=public,
                                              user=self.account['id'])

    def list(self):
        for [index, playlist] in enumerate(self.spotify.current_user_playlists()['items'], 1):
            print(f"{str(index).zfill(2)}) {playlist['name']}")

    def delete(self):
        if self.playlist(self.playlist_name)['response']:
            id_playlist = self.playlist(self.playlist_name)['id']
            if not id:
                print(f"{self.playlist_name} has not been found...")
                return None
            self.spotify.current_user_unfollow_playlist(id_playlist)
            print(f"Playlist {self.playlist_name} deleted...")
            return None
        else:
            print(f"Playlist: {self.playlist_name} don't exist.\nPlease use: playlist list !")
            return None
