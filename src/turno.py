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

  def __init__(self, estado: dict = None):
    """
    Constructor: Se puede pasar el estado para no
    iniciar con los valores por defecto cuando se
    traiga desde la base de datos
    """
    if estado is None:
      self.color = None
      self.dado1 = None
      self.dado2 = None
      self.pares = None
    else:
      self.color = estado['color']
      self.dado1 = estado['dado1']
      self.dado2 = estado['dado2']
      self.pares = estado['pares']

  def dump_object(self):
    """Retorna el estado actual del objeto"""
    return {
      'color': self.color,
      'dado1': self.dado1,
      'dado2': self.dado2,
      'pares': self.pares
    }

  def lanzar(self, dados: int = 2):
    """Lanza los dados"""
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

  def movio(self, dado1 = False, dado2 = False):
    if dado1:
      self.dado1 = 0
    if dado2:
      self.dado2 = 0

  def siguiente_turno(self, color: str):
    self.color = color,
    self.dado1 = None
    self.dado2 = None