import time
import uuid

# import my_firebase
import tablero
import jugador
from turno import Turno
import constants

class Game():
  """Clase principal del juego"""

  def __init__(self, posiciones: int, publico: bool, estado = None):
    self.jugadores = []
    if estado is None:
      self.tablero = tablero.Tablero(posiciones)
      self.publico = publico
      self.iniciado = False
      self.id = uuid.uuid4()
      self.finalizado = False
      self.created_at = time.time()
      self.started_at = None
      self.last_turn = None
      self.turno = Turno()
    else:
      self.tablero = tablero.Tablero(None, estado['tablero'])
      self.publico = estado['publico']
      self.iniciado = estado['iniciado']
      for jugador in estado['jugadores']:
        self.jugadores.append(jugador.Jugador(None, None, None, estado['jugador']))
      self.id = estado['id']
      self.finalizado = estado['finalizado']
      self.created_at = estado['created_at']
      self.started_at = estado['started_at']
      self.last_turn = estado['last_turn']
  
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

    self.jugadores.append(jugador.Jugador(color, nickname, len(self.jugadores)))
    self.tablero.add_color(color)
    return {
      'success': True
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

  def lanzar(self, jugador: jugador.Jugador):
    """Realiza un lanzamiento de dados"""
    if False: # To do verificar si es el turno
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }

    # to do

  def mover(self, jugador: jugador.Jugador, ficha: int):
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

  def sacar_de_la_carcel(self, jugador: jugador.Jugador):
    """Saca fichas de la carcel, depende del par que sacó y de las fichas que estén en la carcel"""
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

  def coronar(self, ficha):
    """Corona una ficha por pares"""
    # to do
    return {}

  def soplar(self, ficha):
    """Sopla una ficha para enviarla a la carcel"""
    # To do
    return {}

  @classmethod
  def retrieve_from_database(cls, id: str):
    """Trae una instancia de un juego desde la base de datos"""
    # to do
    pass

  @classmethod
  def create(cls, posiciones: int = 4, publico: bool = False):
    if posiciones >= 4 or posiciones <= 8:
      return cls(posiciones, publico)

    return {
      'error': True,
      'mensaje': f'No se puede crear un juego para {posiciones} jugadores'
    }
