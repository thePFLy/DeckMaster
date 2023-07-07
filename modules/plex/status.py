from time import sleep
from plexapi.myplex import MyPlexAccount, PlexServer
from core.credentials import Credentials


class Status:
    def __init__(self, server_instance):
        self.credentials = Credentials('plex')
        self.servers = server_instance
        self.servers.update_plex
        self.plex = MyPlexAccount(self.credentials.values['username'], self.credentials.values['password'])
        self.servers = self.update_plex
        self.waited_seconds = 30
        self.sessions = {
            'counter': 0,
            'sessions': []
        }
        self.main

    @property
    def main(self):
        while True:
            media = self.listen
            print(f"Activity:\n"
                  f" - Title: {media['title']}\n"
                  f" - Episode Title: {media['name']}\n"
                  f" - Season: {media['season']}\n"
                  f" - Episode: {media['episod']}\n"
                  f" - Cover: {media['cover']}\n"
                  f" - Banner: {media['background']}\n"
                  f" - Duration: {media['duration'] // 1000 // 60}:{str(media['duration'] // 1000 % 60).zfill(2)}\n"
                  f" - Progression: {media['progress'] // 1000 // 60}:{str(media['progress'] // 1000 % 60).zfill(2)}")
            print("Pause now !")
            print(media['session'].player.skipPrevious())
            """
            print("Stop now !")
            media['session'].stop('Stream interrupted by DeckMaster !')
            """
            print(f"Next update in {self.waited_seconds} seconds...")
            sleep(self.waited_seconds)

    @property
    def update_plex(self):
        servers = []
        for server in self.plex.resources():
            if server.name != 'Generic':
                servers.append(server)
        return servers

    @property
    def listen(self):
        while True:
            for server in self.servers:
                for session in server.connect().sessions():
                    if session._username == self.plex.username:
                        return {
                            "session": session,
                            "title": session.show().title,
                            "name": session.title,
                            "episod": session.episodeNumber,
                            "season": session.seasonNumber,
                            "cover": session.show().posterUrl,
                            "background": session.show().artUrl,
                            "duration": session.duration,
                            "progress": session.viewOffset
                        }
            print(f"The user {self.plex.username} don't play something...\nNew try in {self.waited_seconds} seconds...")
            sleep(self.waited_seconds)
