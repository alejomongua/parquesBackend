# coding: utf-8

from ficha import Ficha

class Jugador(object):
  def __init__(self, color: str, nickname: str):
    self.color = color
    self.nickname = nickname
    self.retirado = False
    self.finalizado = False
    self.fichas = [Ficha(), Ficha(), Ficha(), Ficha()]
    # Asociar después de instanciar
    self.salida = 0
    self.key = None

  def cantidad_dados(self):
    """Determina la cantidad de dados que puede lanzar un jugador"""
    fichas_restantes = [ficha for ficha in self.fichas if not ficha.coronada]
    if len(fichas_restantes) == 1 and fichas_restantes[0].recta_final and fichas_restantes[0].posicion >= 2:
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
