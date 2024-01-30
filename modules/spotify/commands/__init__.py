"""
This file will load all commands, and this init file will be imported from status.py
This has been made to have just to update this file if in the next releases of the spotify's modules.
Also, it's more clean, no ? ;)
"""
from modules.spotify.commands.state import State
from modules.spotify.commands.queue import Queue
from modules.spotify.commands.now import Now
from modules.spotify.commands.playlists import Playlists
from modules.spotify.commands.userinfo import Userinfo
from modules.spotify.commands.volume import Volume
