
class Tablero(object):
    colores=[]

    def __init__(self, posiciones:int):
        self.posiciones = posiciones
        self.colores = [None]*posiciones
    
    def cantidad_de_casillas(self):
        cant_casillas = 17*self.posiciones
        return cant_casillas
    
    def seguro(self, casilla:int):
        x = False
        for i in range(self.posiciones):
            if casilla == (7+17*(i)) or casilla == (12+17*(i)):
                x = True
                break
            
        return x

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
        'colores': self.colores,
        }
