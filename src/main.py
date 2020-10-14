from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def list_servers():
    # to do: Array of servers
    return []

@app.get("/games/new")
def new_game(posiciones: int = 4, public: bool = True):
    # To do
    return {"game_id": 1}

@app.get("/games/{game_id}")
def get_game(game_id: int):
    # to do
    return {}

@app.get("/games/{game_id}/join")
def join_game(game_id: int, nickname: str):
    # to do
    return {}

@app.get("/games/{game_id}/start")
def start(game_id: int):
    # to do
    return {}

@app.get("/games/{game_id}/roll_dice")
def roll(game_id: int, player_key: str):
    # to do
    return {}

@app.get("/games/{game_id}/move")
def move(game_id: int, player_key: str, ficha: int, casilla: int):
    # to do
    return {}

@app.get("/games/{game_id}/get_out_jail")
def get_out_jail(game_id: int, player_key: str):
    # to do
    return {}

@app.get("/games/{game_id}/snitch")
def snitch(game_id: int, player_key: str):
    # to do
    return {}
