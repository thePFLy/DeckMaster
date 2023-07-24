from modules.spotify.status import Status
from core.credentials import Credentials
from core.modules import Modules
from argparse import ArgumentParser, RawDescriptionHelpFormatter

credentials = Credentials('spotify')
if not Modules().initialized('spotify'):
    print('Welcome to the initial setup of Spotify for Deck')
    print(
        "Go to https://developer.spotify.com/dashboard for creating an app.\nAlso don't forget to set a callback_url "
        "!\nFor more facility, set http://localhost:8000 ")
    print('----------------------------')
    credentials.set('client_id', input('client_id: '))
    credentials.set('client_secret', input('client_secret: '))
    credentials.set('callback_url', input('callback_url: '))
    Modules().set_initialized('spotify')

Status(credentials.values)

if __name__ == '__main__':
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description='''
        Help description\n
        ----------------------\n
        1. Create a Spotify developer app\n
        2. Load secrets\n
        3. Get status\n
        ''')
