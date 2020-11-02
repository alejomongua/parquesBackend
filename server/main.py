"""Código del servidor web"""

from fastapi import FastAPI
from juego import my_firebase
from juego import Game

app = FastAPI(
    title="Parqués a la colombiana",
    description="API para un juego de parqués, <a href='https://github.com/alejomongua/parquesBackend'>más información</a>",
    version="0.0.3"
)

@app.get("/juegos")
def listar_juegos_publicos():
    """Lista las partidas públicas a las que se puede unir"""
    return my_firebase.list_public()

@app.get("/juegos/crear_partida")
def nueva_partida(posiciones: int = 4, publico: bool = True):
    return Game.create(posiciones, publico)

@app.get("/juegos/{id_juego}")
def informacion_del_juego(id_juego: str):
    return Game.retrieve_from_database(id_juego)

@app.get("/juegos/{id_juego}/unirse")
def unirse(id_juego: str, color: str, nickname: str):
    game = Game.retrieve_from_database(id_juego)
    return game.join(color, nickname)

@app.get("/juegos/{id_juego}/iniciar")
def iniciar(id_juego: str):
    game = Game.retrieve_from_database(id_juego)
    return game.start()

@app.get("/juegos/{id_juego}/lanzar_dado")
def lanzar(id_juego: str, player_key: str):
    game = Game.retrieve_from_database(id_juego)
    return game.lanzar(player_key)

@app.get("/juegos/{id_juego}/mover_ficha")
def mover(id_juego: str, player_key: str, ficha: int, casillas: int):
    game = Game.retrieve_from_database(id_juego)
    return game.mover(player_key, ficha, casillas)

@app.get("/juegos/{id_juego}/sacar_de_la_carcel")
def sacar_de_la_carcel(id_juego: str, player_key: str):
    game = Game.retrieve_from_database(id_juego)
    return game.sacar_de_la_carcel(player_key)

@app.get("/juegos/{id_juego}/soplar")
def soplar(id_juego: str, player_key: str, ficha: int):
    game = Game.retrieve_from_database(id_juego)

    return game.soplar(player_key, ficha)
