# coding: utf-8

class Ficha():
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

    @classmethod
    def deserializar(cls, estado: dict):
        """Reconstruye el estado del objeto desde un diccionario"""
        ficha = cls()
        ficha.posicion = estado.get('posicion')
        ficha.encarcelada = estado.get('encarcelada')
        ficha.coronada = estado.get('coronada')
        ficha.recta_final = estado.get('recta_final')
        return ficha
