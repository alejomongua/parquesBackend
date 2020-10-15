# coding: utf-8

class Ficha(object):
  def __init__(self, jugador):
    self.posicion = jugador.salida
    self.encarcelada = True
    self.coronada = False
    self.recta_final = False

  def dump_object(self):
    """Retorna el estado actual del objeto"""
    return {
      'posicion': self.posicion,
      'encarcelada': self.encarcelada,
      'coronada': self.coronada,
      'recta_final': self.recta_final
    }