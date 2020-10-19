import time
import uuid
import random

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

    # RANDOMIZACION

    # Orden aleatorio de los turnos de los jugadores
    random.shuffle(self.tablero.colores)

    # Establece el orden de los jugadores
    temp_jugadores = self.jugadores
    self.jugadores = []
    indice = 0
    for color in self.tablero.colores:
      if color is not None:
        # Encuentre el jugador por el color
        for jugador in temp_jugadores:
          if jugador.color == color:
            # Asigne las salidas
            jugador.salida = indice * 17
            # ponga las fichas en su posicion
            for ficha in jugador.fichas:
              ficha.posicion = jugador.salida
            # Asigne el jugador al arreglo
            self.jugadores.append(jugador)
            break
      indice += 1
    # FIN RANDOMIZACION

    # Asigna el primer turno
    self.turno.color = self.jugadores[0].color

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

    if self.turno.color == jugador.color:
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }

    if self.turno.dado1 is not None:
      return {
        'error': True,
        'mensaje': 'No es momento de lanzar los dados'
      }

    self.turno.lanzar(jugador.cantidad_dados())

    # Incremente el contador de pares si aplica
    if self.turno.dado1 == self.turno.dado2:
      self.turno.pares += 1
      if any([ficha.encarcelada for ficha in jugador.fichas]):
        jugador.puede_sacar_de_la_carcel = True
    else:
      self.turno.pares = None

    # Verifique si puede comer
    for ficha in jugador.fichas:
      if ficha.encarcelada or ficha.coronada or ficha.recta_final:
        continue

      for otro_jugador in self.jugadores:
        if jugador.color == otro_jugador.color:
          continue

        for otra_ficha in otro_jugador.fichas:
          if otra_ficha.encarcelada or otra_ficha.coronada or otra_ficha.recta_final:
            continue

          casilla = ficha.posicion + self.turno.dado1
          if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
            jugador.puede_comer = True

          casilla = ficha.posicion + self.turno.dado2
          if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
            jugador.puede_comer = True

          casilla = ficha.posicion + self.turno.dado1 + self.turno.dado2
          if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
            jugador.puede_comer = True

    return self.dump_object()

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

    if self.turno.color == jugador.color:
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }
    
    if self.turno.dado1 is None or self.turno.dado2 is None:
      return {
        'error': True,
        'mensaje': 'Debe lanzar los dados primero'
      }

    esta_ficha = jugador.fichas[ficha]
    cantidad_legal = cantidad == self.turno.dado1 or cantidad == self.turno.dado2 or cantidad == self.turno.dado1 + self.turno.dado2
    if esta_ficha.encarcelada or esta_ficha.coronada or not cantidad_legal:
      return {
        'error': True,
        'mensaje': 'Movimiento ilegal'
      }

    # Este pedazo es complicado, porque toca considerar muchas cosas
    if esta_ficha.recta_final:
      # Si esta en la recta final, revise que la cantidad de pasos que quiere
      # mover sea menor que los que le falten
      if 8 - esta_ficha.posicion <= cantidad:
        return {
          'error': True,
          'mensaje': 'Movimiento ilegal'
        }

    else:
      posicion_actual = esta_ficha.posicion
      llegada = (jugador.salida + self.tablero.posiciones * 17 - 5) % self.tablero.posiciones * 17

      for movimiento in range(cantidad):
        pasos_restantes = 
        if posicion_actual + movimiento == llegada:
          pass

    # Determine cuantos dados usó
    if cantidad == self.turno.dado1:
      self.turno.dado1 == 0
    elif cantidad == self.turno.dado2:
      self.turno.dado2 == 0
    else:
      self.turno.dado1 == 0
      self.turno.dado2 == 0

    return self.dump_object()

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

    if self.turno.color == jugador.color:
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
