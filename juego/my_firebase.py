import os
import json
import firebase_admin
from juego import constants
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
this_file_dir = '/'.join(os.path.realpath(__file__).split('/')[0:-1])
secrets_file_path = f'{this_file_dir}/../secretKey.json'

# Si es en heroku y el archivo no existe hay que crearlo
if not os.path.isfile(secrets_file_path):
    secrets = {
        'type': os.environ.get('TYPE'),
        'project_id': os.environ.get('PROJECT_ID'),
        'private_key_id': os.environ.get('PRIVATE_KEY_ID'),
        'private_key': os.environ.get('PRIVATE_KEY'),
        'client_email': os.environ.get('CLIENT_EMAIL'),
        'client_id': os.environ.get('CLIENT_ID'),
        'auth_uri': os.environ.get('AUTH_URI'),
        'token_uri': os.environ.get('TOKEN_URI'),
        'auth_provider_x509_cert_url': os.environ.get('AUTH_PROVIDER_X509_CERT_URL'),
        'client_x509_cert_url': os.environ.get('CLIENT_X509_CERT_URL'),
    }

    json.dump(secrets, open(secrets_file_path, 'w'))

cred = credentials.Certificate(secrets_file_path)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': constants.DATABASE_URL
})

ref = db.reference('server')

games = ref.child('games')
public_games = ref.child('public')

def register_game(game):
    """Guarda un juego en la base de datos"""
    try:
        serialized = game.serializar()
        if game.id is None:
            new_game_game_ref = games.push(serialized)
            new_game_game_ref.update({
                'id': new_game_game_ref.key
            })
            game.id = new_game_game_ref.key
            public_games.update({
                game.id: {
                    'posiciones': len(game.tablero.colores),
                    'created_at': game.created_at,
                    'jugadores': 0,
                }
            })

        else:
            game_ref = games.child(game.id)
            game_ref.set(serialized)

        return game.id
    except KeyError:
        # to do: catch real exeptions
        return False

def public_registry_update(game):
    """Actualiza los datos de una partida pública"""
    public_games.child(game.id).update({
        'jugadores': len(game.jugadores)
    })

def public_registry_delete(game):
    """Elimina una partida pública cuando ya inicia"""
    public_games.child(game.id).delete()

def get_game(id: str):
    """Trae el juego desde la base de datos"""
    return games.child(id).get()

def list_public():
    return public_games.get()
