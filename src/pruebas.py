import tablero


tab = tablero.Tablero(6)
tab.add_color("Azul")
c = tab.cantidad_de_casillas()
print(c,"Casillas")
color = tab.colores
print(color)

tab.add_color("Amarillo")
color = tab.colores
print(color)

tab.add_color("Amarillo")
color = tab.colores
print(color)

tab.add_color("Amarillo")
color = tab.colores
print(color)

tab.add_color("Amarillo")
color = tab.colores
print(color)

tab.add_color("Verde")
color = tab.colores
print(color)

"""
print(c,"Casillas")
print("Son Seguros:")
for i in range(c):
    if tab.seguro(i):
        print(i)
print("Son Salidas:")
for i in range(c):
    if tab.salida(i):
        print(i)

lista=[]
for i in range(0, c):
    lista.append({
        i:tab.salida(i)
        })

print(lista)
"""