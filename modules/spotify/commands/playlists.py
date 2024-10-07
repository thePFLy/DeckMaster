class Playlists:
    def __init__(self, spotify):
        self.spotify = spotify.socket
        self.data = self.spotify.current_user_playing_track()

    def list_playlists(self, details: bool):
        if details:
            return self.spotify.current_user_playlists()['items']
        else:
            result = {}
            for [index, playlist] in enumerate(self.spotify.current_user_playlists()["items"], 1):
                result[str(index)] = {
                    "name": playlist["name"],
                    "id": playlist["id"],
                    "public": playlist["public"]
                }
            return result

    @staticmethod
    def make_artists_list(artist_dict: dict):
        if len(artist_dict) == 1:
            return artist_dict[0]["name"]
        else:
            result = ""
            for artists in artist_dict:
                result += f"{artists['name']}, "
            return result[:-2]

    def list_playlist_content(self, playlist_id: str, details: bool):
        if details:
            return self.spotify.playlist_items(playlist_id=playlist_id)
        else:
            result = {}
            for [index, track] in enumerate(self.spotify.playlist_items(playlist_id=playlist_id)["items"], 1):
                result[str(index)] = {
                    "added_by": track["added_by"]["id"],
                    "explicit": track["track"]["explicit"],
                    "title": track["track"]["name"],
                    "album_name": track["track"]["album"]["name"],
                    "release": str(track["track"]["album"]["release_date"]).split("-")[0],
                    "album_image": track["track"]["album"]["images"][0]["url"],
                    "artists": self.make_artists_list(artist_dict=track["track"]["artists"]),
                    "duration": f"{str(int(track['track']['duration_ms'] / 1000 / 60)).zfill(2)}"
                                f":"
                                f"{str(int(track['track']['duration_ms'] / 1000 % 60)).zfill(2)}"
                }
            return result

    def get_playlist_id(self, playlist_name: str):
        for playlist_index in self.list_playlists(details=False):
            if playlist_name == self.list_playlists(details=False)[playlist_index]["name"]:
                return self.list_playlists(details=False)[playlist_index]["id"]

    def get_playlist_name(self, playlist_id: str):
        for playlist_index in self.list_playlists(details=False):
            if playlist_id == self.list_playlists(details=False)[playlist_index]["id"]:
                return self.list_playlists(details=False)[playlist_index]["name"]

    def is_present_in_playlist(self, playlist_id: str):
        for track in self.spotify.playlist_items(playlist_id=playlist_id, limit=None)['items']:
            if track['track']['id'] == self.data["item"]["id"]:
                return True

    def get_index_track_in_playlist(self, playlist_id: str):
        for [index, track] in enumerate(self.spotify.playlist_items(playlist_id=playlist_id, limit=None)['items']):
            if track['track']['id'] == self.data["item"]["id"]:
                return index

    def playlist_exist(self, playlist_name: str):
        for playlist in self.spotify.current_user_playlists()["items"]:
            if playlist_name == playlist["name"]:
                return True

    def delete_from_playlist(self, playlist_id: str):
        if self.playlist_exist(playlist_name=self.get_playlist_name(playlist_id=playlist_id)):
            if self.is_present_in_playlist(playlist_id=playlist_id):
                self.spotify.playlist_remove_specific_occurrences_of_items(
                    playlist_id=playlist_id,
                    items=[
                        {
                            "uri": self.data["item"]["id"],
                            "positions": self.get_index_track_in_playlist(playlist_id=playlist_id)
                        }
                    ]
                )
                return "TRACK_SUCCESS_DELETED"
            else:
                return "TRACK_NOT_IN_PLAYLIST"

    def add_to_playlist(self, playlist_id: str):
        if self.playlist_exist(playlist_name=self.get_playlist_name(playlist_id=playlist_id)):
            if not self.is_present_in_playlist(playlist_id=playlist_id):
                self.spotify.playlist_add_items(
                    playlist_id=playlist_id,
                    items=[self.data["item"]["uri"]]
                )
                return "TRACK_SUCCESS_ADDED"
            else:
                return "TRACK_ALREADY_IN_PLAYLIST"
        else:
            return "PLAYLIST_NOT_EXIST"

    def create_playlist(self, name: str, public: bool):
        if not self.playlist_exist(playlist_name=name):
            self.spotify.user_playlist_create(
                name=name,
                public=public,
                user=self.spotify.me()["id"]
            )
            return "PLAYLIST_SUCCESS_CREATED"
        else:
            return "PLAYLIST_NAME_ALREADY_EXIST"

    def delete_playlist(self, playlist_id: str):
        if self.playlist_exist(playlist_name=self.get_playlist_name(playlist_id=playlist_id)):
            self.spotify.current_user_unfollow_playlist(
                playlist_id=playlist_id
            )
            return "PLAYLIST_SUCCESS_CREATED"
        else:
            return "PLAYLIST_NOT_EXIST"

    def edit_playlist(self, playlist_id: str, name: str, public: bool):
        if self.playlist_exist(playlist_name=self.get_playlist_name(playlist_id=playlist_id)):
            self.spotify.user_playlist_change_details(
                playlist_id=playlist_id,
                user=self.spotify.me()["id"],
                name=name,
                public=public
            )
            return "PLAYLIST_SUCCESS_UPDATED"
        else:
            return "PLAYLIST_NOT_EXIST"

    def queue(self, details: bool):
        if details:
            return self.spotify.queue()
        else:
            result = {}
            for [index, track] in enumerate(self.spotify.queue()["queue"], 1):
                result[str(index)] = {
                    "title": track["name"],
                    "artists": self.make_artists_list(artist_dict=track["artists"]),
                    "album": track["album"]["name"],
                    "duration": f"{str(int(track['duration_ms'] / 1000 / 60)).zfill(2)}"
                                f":"
                                f"{str(int(track['duration_ms'] / 1000 % 60)).zfill(2)}",
                    "url_cover": track['album']['images'][0]["url"]
                }
            return result
