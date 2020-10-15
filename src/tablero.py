
class Tablero(object):

    def __init__(self, posiciones:int):
        self.posiciones = posiciones
    
    def cantidad_de_casillas(self):
        cant_casillas = 17*self.posiciones
        return cant_casillas
    
    def seguro(self, casilla:int):
        x = False
        for i in range(self.posiciones+1):
            if casilla == (7+17*(i-1)) or casilla == (12+17*(i-1)):
                x = True
                break
            
        return x

    def salida(self, casilla:int):
        x = False
        for i in range(self.posiciones+1):
            if casilla == (17*(i-1)):
                x = True
                break
            
        return x

""" PRUEBA
tab = Tablero(6)
c = tab.cantidad_de_casillas()
print(c,"Casillas")
print("Son Seguros:")
for i in range(c):
    if tab.seguro(i):
        print(i)
print("Son Salidas:")
for i in range(c):
    if tab.salida(i):
        print(i)
"""