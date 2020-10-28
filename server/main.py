from typing import Optional

from fastapi import FastAPI
from juego import my_firebase
from juego import Game

app = FastAPI()

@app.get("/")
def list_servers():
    """Lista las partidas públicas a las que se puede unir"""
    return my_firebase.list_public()

@app.get("/games/new")
def new_game(posiciones: int = 4, public: bool = True):
    return Game.create(posiciones, public)

@app.get("/games/{game_id}")
def get_game(game_id: str):
    return Game.retrieve_from_database(game_id)

@app.get("/games/{game_id}/join")
def join_game(game_id: str, color: str, nickname: str):
    game = Game.retrieve_from_database(game_id)
    return game.join(color, nickname)

@app.get("/games/{game_id}/start")
def start(game_id: str):
    game = Game.retrieve_from_database(game_id)
    return game.start()

@app.get("/games/{game_id}/roll_dice")
def roll(game_id: str, player_key: str):
    game = Game.retrieve_from_database(game_id)
    return game.lanzar(player_key)

@app.get("/games/{game_id}/move")
def move(game_id: str, player_key: str, ficha: int, casillas: int):
    game = Game.retrieve_from_database(game_id)
    return game.mover(player_key, ficha, casillas)

@app.get("/games/{game_id}/get_out_jail")
def get_out_jail(game_id: str, player_key: str):
    game = Game.retrieve_from_database(game_id)
    return game.sacar_de_la_carcel(player_key)

@app.get("/games/{game_id}/snitch")
def snitch(game_id: str, player_key: str, ficha: int):
    game = Game.retrieve_from_database(game_id)

    return game.soplar(player_key, ficha)
