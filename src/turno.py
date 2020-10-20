import random

class Turno():
  """
  Lleva el control del estado del turno actual

  ...

  Attributes
  ----------
  color : string
      Jugador que tomará el primer turno
  dado1 : int
      Valor lanzado en el primer dado, es None si
      no se ha lanzado o 0 si ya se movió
  dado2 : int
      Valor lanzado en el segundo dado, es None si
      no se ha lanzado o 0 si ya se movió o si se
      lanza un solo dado
  pares : int
      Indica cuantos pares consecutivos ha sacado,
      si no saca pares es None, si sacó pares pero
      salió de la cárcel es 0

  Methods
  -------
  dump_object()
      Retorna el estado actual del objeto

  """

  def __init__(self):
    """
    Constructor: Se puede pasar el estado para no
    iniciar con los valores por defecto cuando se
    traiga desde la base de datos
    """
    self.color = None
    self.dado1 = None
    self.dado2 = None
    self.pares = None
    self.soplable = [False, False, False, False]
    self.locked = [False, False, False, False]
    self.color_soplable = None
    self.intentos = 3

  def dump_object(self):
    """Retorna el estado actual del objeto"""
    return {
      'color': self.color,
      'dado1': self.dado1,
      'dado2': self.dado2,
      'pares': self.pares,
      'intentos': self.intentos
    }

  def lanzar(self, dados: int = 2):
    """Lanza los dados"""
    self.soplable = [False, False, False, False]

    if dados == 2:
      self.dado2 = random.randint(1, 6)
    else:
      self.dado2 = 0

    self.dado1 = random.randint(1, 6)

    if self.dado1 == self.dado2:
      if self.pares is None:
        self.pares = 1
      else:
        self.pares = self.pares + 1
    else:
      self.pares = None

  def siguiente_turno(self, color: str):
    self.color = color
    self.dado1 = None
    self.dado2 = None
    self.locked = [False, False, False, False]
