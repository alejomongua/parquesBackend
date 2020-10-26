class Tablero(object):
    colores = []

    def __init__(self, posiciones:int):
        self.posiciones = posiciones
        self.colores = [False] * posiciones
    
    def cantidad_de_casillas(self):
        return 17 * self.posiciones
    
    def seguro(self, casilla:int):    
        return casilla % 17 == 12 or casilla % 17 == 7

    def salida(self, casilla:int):
        return casilla % 17 == 0

    def add_color(self, color):
        for i in range(len(self.colores)):
            if not self.colores[i]:
                self.colores.remove(False)
                self.colores.append(color)
                break
        return

    def public_state(self):
        """Retorna el estado actual del objeto"""
        return {
            'colores': self.colores
        }

    @classmethod
    def deserializar(cls, estado: dict):
        """Reconstruye el estado del objeto desde un diccionario"""
        colores = estado.get('colores', [])
        tablero = cls(len(colores))
        tablero.colores = colores
        return tablero

    serializar = public_state
