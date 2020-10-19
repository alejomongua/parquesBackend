class Tablero(object):
    colores = []

    def __init__(self, posiciones:int, estado: dict=None):
        self.posiciones = posiciones
        self.colores = [None] * posiciones
    
    def cantidad_de_casillas(self):
        return 17 * self.posiciones
    
    def seguro(self, casilla:int):    
        return casilla % 17 == 12 or casilla % 17 == 7

    def salida(self, casilla:int):
        return casilla % 17 == 0

    def add_color(self, color):
        for i in range(len(self.colores)):
            if self.colores[i] == None:
                self.colores.remove(None)
                self.colores.append(color)
                break
        return


    def dump_object(self):
        """Retorna el estado actual del objeto"""
        return {
            'colores': self.colores
        }
