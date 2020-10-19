# coding: utf-8

class Ficha(object):
  def __init__(self):
    self.encarcelada = True
    self.coronada = False
    self.recta_final = False
    # Asignar después de instanciar
    self.posicion = 0

  def dump_object(self):
    """Retorna el estado actual del objeto"""
    return {
      'posicion': self.posicion,
      'encarcelada': self.encarcelada,
      'coronada': self.coronada,
      'recta_final': self.recta_final
    }
