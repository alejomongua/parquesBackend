import time

import my_firebase
import tablero
import jugador

class Game():
  """Clase principal del juego"""

  COLORES = {
    'Amarillo': '#ffe119',
    'Azul': '#4363d8',
    'Naranja': '#f58231',
    'Lavanda': '#dcbeff', 
    'Marrón': '#800000', 
    'Azul oscuro': '#000075',
    'Gris': '#a9a9a9',
    'Negro': '#ffffff'
  }

  def __init__(self, posiciones: int, publico: bool):
    self.tablero = tablero.Tablero(posiciones)
    self.publico = publico
    self.jugadores = []
    self.id = my_firebase.register_game(self.tablero, publico)
    self.finalizado = False
    self.created_at = time.time()
    self.last_turn = None
  
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
    if not color in Game.COLORES:
      return {
        'error': True,
        'message': f'El color no es válido, debe ser una de estas opciones: {list(Game.COLORES.keys())}'
      }
    if len(self.jugadores) < self.tablero.posiciones:
      self.jugadores.append(jugador.Jugador(color, nickname, len(self.jugadores)))
      self.tablero.add_color(color)
      return {
        'success': True
      }

  @classmethod
  def retrieve_from_database(cls, id: str):
    """Trae una instancia de un juego desde la base de datos"""
    # to do
    pass
