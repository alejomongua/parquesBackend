import firebase_admin
import constants
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('../serviceKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': constants.DATABASE_URL
})

def register_game():
  """Guarda un juego en la base de datos"""
