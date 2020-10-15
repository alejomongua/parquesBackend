# coding: utf-8

from ficha import Ficha

class Jugador(object):
  def __init__(self, color: str, nickname: str, orden: int, estado = None):
    if estado is None:
      self.color = color
      self.nickname = nickname
      self.salida = orden * 17
      self.retirado = False
      self.finalizado = False
      self.fichas = [Ficha(self), Ficha(self), Ficha(self), Ficha(self)]
    else:
      self.color = estado['color']
      self.nickname = estado['nickname']
      self.salida = estado['salida']
      self.retirado = estado['retirado']
      self.finalizado = estado['finalizado']
      self.fichas = []
      for ficha in estado['fichas']:
        Ficha(self, ficha)

  def cantidad_dados(self):
    """Determina la cantidad de dados que puede lanzar un jugador"""
    if len([ficha for ficha in self.fichas if ficha.encarcelada and not ficha.coronada]) == 1:
      return 1

    return 2

  def cantidad_lanzamientos(self):
    """Determina la cantidad lanzamientos que tiene un jugador"""
    if all([ficha.encarcelada for ficha in self.fichas if not ficha.coronada]):
      return 3

    return 1

  def dump_object(self):
    """Retorna el estado actual del objeto"""
    return {
      'nickname': self.nickname,
      'color': self.color,
      'fichas': [ficha.dump_object() for ficha in self.fichas],
      'retirado': self.retirado,
      'finalizado': self.finalizado,
      'salida': self.salida
    }
