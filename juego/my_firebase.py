import os.path
import firebase_admin
from juego import constants
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
this_file_dir = '/'.join(os.path.realpath(__file__).split('/')[0:-1])
cred = credentials.Certificate(f'{this_file_dir}/../secretKey.json')

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
