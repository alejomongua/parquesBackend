# coding: utf-8

class Ficha(object):
  def __init__(self, jugador, estado = None):
    if estado is None:
      self.posicion = jugador.salida
      self.encarcelada = True
      self.coronada = False
      self.recta_final = False
    else:
      self.posicion = estado['posicion']
      self.encarcelada = estado['encarcelada']
      self.coronada = estado['coronada']
      self.recta_final = estado['recta_final']

  def dump_object(self):
    """Retorna el estado actual del objeto"""
    return {
      'posicion': self.posicion,
      'encarcelada': self.encarcelada,
      'coronada': self.coronada,
      'recta_final': self.recta_final
    }
