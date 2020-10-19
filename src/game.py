import time
import uuid

# import my_firebase
from tablero import Tablero
from jugador import Jugador
from turno import Turno
import constants

class Game():
  """Clase principal del juego"""

  def __init__(self, publico: bool = False):
    self.publico = publico
    self.iniciado = False
    self.finalizado = False
    self.created_at = time.time()
    self.started_at = None
    self.last_turn = None
    self.jugadores = []
    # Estos se deben asignar después de crear el juego
    self.id = None
    self.turno = None
    self.tablero = None
  
  def dump_object(self):
    """Retorna el estado actual del objeto"""
    return {
      'id': self.id,
      'tablero': self.tablero.dump_object(),
      'jugadores': [jugador.dump_object() for jugador in self.jugadores],
      'finalizado': self.finalizado,
      'inicio': self.created_at,
      'ultimo_turno': self.last_turn
    }

  def join(self, color: str, nickname: str):
    """Se agrega un jugador a la partida"""
    if not color in constants.COLORES:
      return {
        'error': True,
        'mensaje': f'El color no es válido, debe ser una de estas opciones: {list(constants.COLORES.keys())}'
      }

    if len(self.jugadores) >= self.tablero.posiciones:
      return {
        'error': True,
        'mensaje': 'Ya se alcanzó el máximo de jugadores para esta partida'
      }

    if color in self.tablero.colores:
      return {
        'error': True,
        'mensaje': f'El color {color} ya fue escogido, por favor escoja otro'
      }

    if self.iniciado:
      return {
        'error': True,
        'mensaje': 'No se puede unir a esta partida porque ya inició'
      }

    jugador = Jugador(color, nickname)
    jugador.key = uuid.uuid4()
    self.jugadores.append(jugador)
    self.tablero.add_color(color)
    return {
      'success': True,
      'key': jugador.key
    }

  def iniciar(self):
    """Se inicia la partida, ya no se pueden unir más jugadores"""
    if len(self.jugadores) < 2:
      return {
        'error': True,
        'mensaje': 'No se puede iniciar la partida porque hay muy pocos jugadores'
      }

    # Orden aleatorio de los turnos de los jugadores
    # To do

    # Asigna el primer turno
    self.turno.color = self.jugadores[0]

    # Marca el inicio del juego
    self.started_at = time.time()
    self.iniciado = True

    return { 'success': True }

  def lanzar(self, player_key: str):
    """Realiza un lanzamiento de dados"""
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    if False: # To do verificar si es el turno
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }

    # to do

  def mover(self, player_key: str, ficha: int, cantidad: int):
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    if ficha > len(jugador.fichas):
      return {
        'error': True,
        'mensaje': 'Ficha erronea'
      }

    if False: # To do verificar
      return {
        'error': True,
        'mensaje': 'Movimiento ilegal'
      }

    if False: # To do verificar
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }

    # To do

  def sacar_de_la_carcel(self, player_key: str):
    """Saca fichas de la carcel, depende del par que sacó y de las fichas que estén en la carcel"""
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    if not any([not ficha.encarcelada for ficha in jugador.fichas]):
      return {
        'error': True,
        'mensaje': 'No tiene fichas en la carcel'
      }

    if False: # To do verificar si sacó pares
      return {
        'error': True,
        'mensaje': 'Necesita sacar pares para salir de la carcel'
      }

    if False: # To do verificar si es el turno
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }

    # to do

  def start(self):
    """Inicia el juego"""
    # To do
    return {}

  def coronar(self, player_key: str, ficha: int):
    """Corona una ficha por pares"""
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    # to do
    return {}

  def soplar(self, ficha):
    """Sopla una ficha para enviarla a la carcel"""
    # To do
    return {}

  def almacenar(self):
    """Almacena el estado del juego en la base de datos"""

    # To do

  def encontrar_jugador(self, key: str):
    """Encuentra un jugador por su llave"""
    for jugador in self.jugadores:
      if jugador.key == key:
        return jugador

    # Si no encuentra ninguno retorna None
    return None

  @classmethod
  def retrieve_from_database(cls, id: str):
    """Trae una instancia de un juego desde la base de datos"""

    # to do

  @classmethod
  def create(cls, posiciones: int = 4, publico: bool = False):
    if posiciones >= 4 or posiciones <= 8:
      game = cls(publico)
      game.id = uuid.uuid4()
      game.turno = Turno()
      game.tablero = Tablero(posiciones)
      game.almacenar()
      return game

    return {
      'error': True,
      'mensaje': f'No se puede crear un juego para {posiciones} jugadores'
    }
