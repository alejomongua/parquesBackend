"""Código del servidor web"""

from fastapi import FastAPI, Response
from juego import my_firebase
from juego import Game

app = FastAPI(
    title="Parqués a la colombiana",
    description="API para un juego de parqués, <a href='https://github.com/alejomongua/parquesBackend'>más información</a>",
    version="0.0.4"
)

@app.get("/juegos")
def listar_juegos_publicos():
    """Lista las partidas públicas a las que se puede unir"""
    return my_firebase.list_public()

@app.get("/juegos/crear_partida", status_code=201)
def nueva_partida(response: Response, posiciones: int = 4, publico: bool = True):
    game = Game.create(posiciones, publico)

    # Si es un diccionario es porque hubo un error
    if isinstance(game, dict):
        response.status_code = 400
        return game

    return game.public_state()

@app.get("/juegos/{id_juego}")
def informacion_del_juego(response: Response, id_juego: str):
    game = Game.retrieve_from_database(id_juego)

    if game is None:
        response.status_code = 400
        return {
            'error': True,
            'mensaje': 'El juego no existe, verifique el ID'
        }

    return game.public_state()

@app.get("/juegos/{id_juego}/unirse")
def unirse(response: Response, id_juego: str, color: str, nickname: str):
    game = Game.retrieve_from_database(id_juego)
    estado = game.join(color, nickname)

    if estado.get('error', None):
        response.status_code = 400

    return estado

@app.get("/juegos/{id_juego}/iniciar")
def iniciar(response: Response, id_juego: str):
    game = Game.retrieve_from_database(id_juego)
    estado = game.start()

    if estado.get('error', None):
        response.status_code = 400

    return estado

@app.get("/juegos/{id_juego}/lanzar_dado")
def lanzar(response: Response, id_juego: str, player_key: str):
    game = Game.retrieve_from_database(id_juego)
    estado = game.lanzar(player_key)

    if estado.get('error', None):
        response.status_code = 400

    return estado

@app.get("/juegos/{id_juego}/mover_ficha")
def mover(response: Response, id_juego: str, player_key: str, ficha: int, casillas: int):
    game = Game.retrieve_from_database(id_juego)
    estado = game.mover(player_key, ficha, casillas)

    if estado.get('error', None):
        response.status_code = 400

    return estado

@app.get("/juegos/{id_juego}/sacar_de_la_carcel")
def sacar_de_la_carcel(response: Response, id_juego: str, player_key: str):
    game = Game.retrieve_from_database(id_juego)
    estado = game.sacar_de_la_carcel(player_key)

    if estado.get('error', None):
        response.status_code = 400

    return estado

@app.get("/juegos/{id_juego}/soplar")
def soplar(response: Response, id_juego: str, player_key: str, ficha: int):
    game = Game.retrieve_from_database(id_juego)
    estado = game.soplar(player_key, ficha)

    if estado.get('error', None):
        response.status_code = 400

    return estado
