from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

client_id = '637454297514-dcdbbss9q462qte62jaokigpucq1kflg.apps.googleusercontent.com'
client_secret = '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'
redirect_uri = 'http://localhost:8000'

# Configuration de la portée d'accès
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Obtention du jeton d'accès
flow = InstalledAppFlow.from_client_secrets_file(
    'youtube/client_secret_637454297514-dcdbbss9q462qte62jaokigpucq1kflg.apps.googleusercontent.com.json',
    scopes=scopes
)
credentials = flow.run_local_server(port=8080)
token = credentials.token

# Création d'un objet d'accès à l'API YouTube
youtube = build('youtube', 'v3', credentials=credentials)

# Recherche de la vidéo par mot-clé
request = youtube.search().list(
    q='YOUR_KEYWORDS',
    part='id',
    type='video',
    maxResults=1
)
response = request.execute()

# Récupération de l'ID de la première vidéo de la réponse
video_id = response['items'][0]['id']['videoId']

# Lecture de la vidéo
request = youtube.videos().rate(
    id=video_id,
    rating='none'  # Vous pouvez également utiliser 'dislike' ou 'none'
)
response = request.execute()

# Mise en pause de la vidéo
request = youtube.videos().rate(
    id=video_id,
    rating='none'
)
response = request.execute()
