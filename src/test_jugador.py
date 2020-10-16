import unittest
from jugador import Jugador
import constants

class FichaTest(unittest.TestCase):
  
  def test_dump_object(self):
    # Tome el primer elemento de la lista de colores
    color = constants.COLORES[list(constants.COLORES.keys())[0]]

    # instancie el jugador
    nickname = 'pepitoperez'
    jugador = Jugador(color, nickname, 3)

    # Lláme el método
    resultado = jugador.dump_object()
    
    # Verifique los diferentes componentes
    self.assertEqual(resultado['nickname'], nickname)
    self.assertEqual(resultado['color'], color)
    self.assertIsInstance(resultado['fichas'], list)
    self.assertEqual(len(resultado['fichas']), 4)
    self.assertEqual(resultado['retirado'], False)
    self.assertEqual(resultado['finalizado'], False)
    self.assertEqual(resultado['salida'], 3 * 17)

  def test_cantidad_de_dados(self):
    # Tome el primer elemento de la lista de colores
    color = constants.COLORES[list(constants.COLORES.keys())[0]]

    # instancie el jugador
    nickname = 'pepitoperez'
    jugador = Jugador(color, nickname, 3)

    # Lláme el método
    resultado = jugador.cantidad_dados()
    
    # Verifique que pueda lanzar dos dados
    self.assertEqual(resultado, 2)

    # Saque las fichas de la carcel
    for i in range(4):
      jugador.fichas[i].encarcelada = False

    # Lláme el método
    resultado = jugador.cantidad_dados()
    
    # Verifique que pueda lanzar dos dados
    self.assertEqual(resultado, 2)

    # Corone tres de las cuatro fichas
    for i in range(3):
      jugador.fichas[i].coronada = True

    # La última ficha, pógala faltando 5 casillas para coronar
    jugador.fichas[3].recta_final = True
    jugador.fichas[3].posicion = 3

    # Lláme el método
    resultado = jugador.cantidad_dados()
    
    # Verifique que pueda lanzar un solo dado
    self.assertEqual(resultado, 1)

  def test_cantidad_de_lanzamientos(self):
    # Tome el primer elemento de la lista de colores
    color = constants.COLORES[list(constants.COLORES.keys())[0]]

    # instancie el jugador
    nickname = 'pepitoperez'
    jugador = Jugador(color, nickname, 3)

    # Lláme el método
    resultado = jugador.cantidad_lanzamientos()
    
    # Verifique que pueda lanzar tres veces
    self.assertEqual(resultado, 3)

    # Saque una de las fichas de la carcel
    jugador.fichas[0].encarcelada = False

    # Lláme el método
    resultado = jugador.cantidad_lanzamientos()
    
    # Verifique que pueda lanzar solo una vez
    self.assertEqual(resultado, 1)

    # Corone tres de las dos fichas
    for i in range(2):
      jugador.fichas[i].coronada = True

    # Lláme el método
    resultado = jugador.cantidad_lanzamientos()
    
    # Verifique que pueda lanzar tres veces
    self.assertEqual(resultado, 3)

    # Saque otra de las fichas de la carcel
    jugador.fichas[3].encarcelada = False

    # Lláme el método
    resultado = jugador.cantidad_lanzamientos()
    
    # Verifique que pueda lanzar solo una vez
    self.assertEqual(resultado, 1)

if __name__ == '__main__':
    unittest.main()
