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
    jugador.key = str(uuid.uuid4())
    self.jugadores.append(jugador)
    self.tablero.add_color(color)
    return {
      'success': True,
      'key': jugador.key
    }

  def start(self):
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
    self.turno.intentos = 3

    # Marca el inicio del juego
    self.started_at = time.time()
    self.iniciado = True

    return self.almacenar()

  def lanzar(self, player_key: str):
    """Realiza un lanzamiento de dados"""
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    if self.turno.color != jugador.color:
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }

    if all([ficha.encarcelada for ficha in jugador.fichas if not ficha.coronada]):
      self.turno.lanzar(2)

      self.turno.intentos -= 1

      if self.turno.intentos == 0 and self.turno.dado1 != self.turno.dado2:
        self.siguiente_turno()
    else:
      if self.turno.dado1 is not None:
        return {
          'error': True,
          'mensaje': 'No es momento de lanzar los dados'
        }

      self.turno.lanzar(jugador.cantidad_dados())

    # Incremente el contador de pares si aplica
    if self.turno.dado1 == self.turno.dado2:
      if self.turno.pares is None:
        self.turno.pares = 1
      else:
        self.turno.pares += 1
    else:
      self.turno.pares = None

    return self.almacenar()

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

    if self.turno.color != jugador.color:
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
    if esta_ficha.encarcelada or esta_ficha.coronada or not cantidad_legal or cantidad == 0 or self.turno.locked[ficha]:
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

      esta_ficha.posicion += cantidad

      if esta_ficha.posicion == 8:
        esta_ficha.coronada = True

    else:
      # Si no esta en la recta final
      posicion_actual = esta_ficha.posicion
      llegada = (jugador.salida + self.tablero.posiciones * 17 - 5) % self.tablero.posiciones * 17

      for movimiento in range(cantidad):
        pasos_restantes = cantidad - movimiento - 1

        # Si llegó a la recta final:
        if posicion_actual + movimiento + 1 == llegada:
          if pasos_restantes > 8:
            return {
              'error': True,
              'mensaje': 'Movimiento ilegal'
            }

          else:
            esta_ficha.recta_final = True
            esta_ficha.posicion += pasos_restantes

            if esta_ficha.posicion == 8:
              esta_ficha.coronada = True

        else:
          esta_ficha.posicion = (posicion_actual + movimiento + 1) % self.tablero.posiciones * 17

    comio = False
    # Revise si metió alguna ficha a la carcel
    if not esta_ficha.recta_final and not self.tablero.seguro(esta_ficha.posicion) and not self.tablero.salida(esta_ficha.posicion):
      for otro_jugador in self.jugadores:
        if jugador.color == otro_jugador.color:
          continue

        for otra_ficha in otro_jugador.fichas:
          if otra_ficha.encarcelada or otra_ficha.coronada or otra_ficha.recta_final:
            continue

          if otra_ficha.posicion == esta_ficha.posicion:
            comio = True
            otra_ficha.encarcelada = True
            otra_ficha.posicion = otro_jugador.salida

    # Verifique si se puede soplar alguna ficha, este proceso es largo y complicado, la lógica es la siguiente:
    # Se puede soplar en cualquiera de los siguientes casos
    # Si tiene fichas en la carcel y sacó pares
    # Si movió con la suma de los dados y no comió y alguna ficha podía comer
    # Si movió con uno de los dados y no comió y podía comer con la suma de las fichas
    # Si movió con uno de los dados y no comió y podía comer con ese valor y el otro dado tiene un valor diferente

    # Si tiene fichas en la carcel y sacó pares
    if len([0 for ficha in jugador.fichas if ficha.encarcelada]) > 0 and self.turno.dado1 == self.turno.dado2:
      self.turno.color_soplable = jugador.color
      self.turno.soplable[ficha] = True

    if not comio:
      # Si movió con la suma de los dados y no comió y alguna ficha podía comer
      if self.turno.dado1 + self.turno.dado2 == cantidad:
        for contador in range(4):
          ficha1 = jugador.fichas[contador]
          if ficha1.encarcelada or ficha1.coronada or ficha1.recta_final or contador == ficha:
            continue
    
          for otro_jugador in self.jugadores:
            if jugador.color == otro_jugador.color:
              continue
    
            for otra_ficha in otro_jugador.fichas:
              if otra_ficha.encarcelada or otra_ficha.coronada or otra_ficha.recta_final:
                continue
    
              casilla = ficha1.posicion + self.turno.dado1
              if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
                self.turno.color_soplable = jugador.color
                self.turno.soplable[ficha] = True
                continue
    
              casilla = ficha1.posicion + self.turno.dado2
              if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
                self.turno.color_soplable = jugador.color
                self.turno.soplable[ficha] = True
                continue
    
              casilla = ficha1.posicion + self.turno.dado1 + self.turno.dado2
              if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
                self.turno.color_soplable = jugador.color
                self.turno.soplable[ficha] = True
                continue

      else:
        for contador in range(4):
          ficha1 = jugador.fichas[contador]
          if ficha1.encarcelada or ficha1.coronada or ficha1.recta_final or contador == ficha:
            continue
    
          for otro_jugador in self.jugadores:
            if jugador.color == otro_jugador.color:
              continue
    
            for otra_ficha in otro_jugador.fichas:
              if otra_ficha.encarcelada or otra_ficha.coronada or otra_ficha.recta_final:
                continue
    
              # Si movió con uno de los dados y no comió y podía comer con la suma de las fichas
              casilla = ficha1.posicion + self.turno.dado1 + self.turno.dado2
              if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
                self.turno.color_soplable = jugador.color
                self.turno.soplable[ficha] = True
                continue
              
              # Si movió con uno de los dados y no comió y podía comer con ese valor y el otro dado tiene un valor diferente
              if self.turno.dado1 != self.turno.dado2:
                casilla = ficha1.posicion + cantidad
                if otra_ficha.posicion == casilla and not self.tablero.seguro(casilla) and not self.tablero.salida(casilla):
                  self.turno.color_soplable = jugador.color
                  self.turno.soplable[ficha] = True
                  continue

    # Determine cuantos dados usó
    if cantidad == self.turno.dado1:
      self.turno.dado1 = 0
    elif cantidad == self.turno.dado2:
      self.turno.dado2 = 0
    else:
      self.turno.dado1 = 0
      self.turno.dado2 = 0

    if self.turno.dado1 == 0 and self.turno.dado2 == 0:
      if self.turno.pares is None:
        self.siguiente_turno()
      else:
        self.turno.siguiente_turno(self.turno.color)

    return self.almacenar()

  def sacar_de_la_carcel(self, player_key: str):
    """Saca fichas de la carcel, depende del par que sacó y de las fichas que estén en la carcel"""
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    if self.turno.color != jugador.color:
      return {
        'error': True,
        'mensaje': 'Espere su turno'
      }
    
    if self.turno.dado1 is None or self.turno.dado2 is None:
      return {
        'error': True,
        'mensaje': 'Debe lanzar los dados primero'
      }

    if self.turno.dado1 != self.turno.dado2:
      return {
        'error': True,
        'mensaje': 'Necesita sacar pares para salir de la carcel'
      }

    # Si no tiene fichas en la carcel
    if len([0 for ficha in jugador.fichas if ficha.encarcelada]) == 0:
      return {
        'error': True,
        'mensaje': 'No tiene fichas en la carcel'
      }

    contador = 0

    # Almacene cuales fichas libera, para que no se pueda mover si es solo una
    fichas_liberadas = []
    for ficha in range(4):
      esta_ficha = jugador.fichas[ficha]
      if esta_ficha.encarcelada and not esta_ficha.coronada:
        esta_ficha.encarcelada = False
        fichas_liberadas.append(ficha)
        # Si no es par de 6 ni de 1, saque solo 2
        if self.turno.dado1 != 6 and self.turno.dado2 != 1:
          contador += 1
          if contador == 2:
            break

    self.turno.dado2 = 0
    if len(fichas_liberadas) == 1:
      # Si le quedan más fichas, la ficha que sacó queda bloqueada
      cantidad_no_coronadas = len([0 for ficha in jugador.fichas if not ficha.coronada])
      if cantidad_no_coronadas != 1:
        self.turno.locked[fichas_liberadas[0]] = True
      self.turno.dado2 = 0
    else:
      self.turno.siguiente_turno(self.turno.color)
    self.turno.pares = 0

    return self.almacenar()

  def coronar(self, player_key: str, ficha: int):
    """Corona una ficha por pares"""
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    if self.turno.pares is None or self.turno.pares < 3:
      return {
        'error': True,
        'mensaje': 'Tiene que sacar tres pares seguidos sin sacar de la carcel'
      }

    jugador.fichas[ficha].coronada = True
    self.siguiente_turno()
    return self.almacenar()

  def soplar(self, player_key: str, ficha: int):
    """Sopla una ficha para enviarla a la carcel"""
    jugador = self.encontrar_jugador(player_key)

    if jugador is None:
      return {
        'error': True,
        'mensaje': 'La llave no coincide con ningún jugador en este juego'
      }

    if not self.turno.soplable[ficha]:
      return {
        'error': True,
        'mensaje': 'No se puede soplar esa ficha'
      }

    # Encuentre el jugador por el color
    for jugador1 in self.jugadores:
      if jugador1.color == self.turno.color_soplable:
        jugador1.fichas[ficha].encarcelada = True
        break

    return self.almacenar()

  def almacenar(self):
    """Almacena el estado del juego en la base de datos"""
    return self.dump_object()
    # To do

  def encontrar_jugador(self, key: str):
    """Encuentra un jugador por su llave"""
    for jugador in self.jugadores:
      if jugador.key == key:
        return jugador

    # Si no encuentra ninguno retorna None
    return None

  def siguiente_turno(self):
    """Hace el setup para el siguiente turno"""
    indice_actual = [jugador.color for jugador in self.jugadores].index(self.turno.color)
    siguiente_jugador = self.jugadores[(indice_actual + 1) % len(self.jugadores)]
    self.turno.siguiente_turno(siguiente_jugador.color)
    self.turno.pares = None
    self.turno.intentos = siguiente_jugador.cantidad_lanzamientos()

  @classmethod
  def retrieve_from_database(cls, id: str):
    """Trae una instancia de un juego desde la base de datos"""

    # to do

  @classmethod
  def create(cls, posiciones: int = 4, publico: bool = False):
    if posiciones >= 4 or posiciones <= 8:
      game = cls(publico)
      game.id = str(uuid.uuid4())
      game.turno = Turno()
      game.tablero = Tablero(posiciones)
      game.almacenar()
      return game

    return {
      'error': True,
      'mensaje': f'No se puede crear un juego para {posiciones} jugadores'
    }
