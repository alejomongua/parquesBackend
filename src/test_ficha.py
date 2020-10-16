import unittest
from ficha import Ficha
from jugador import Jugador
import constants

class FichaTest(unittest.TestCase):
  
  def test_dump_object(self):
    # Tome el primer elemento de la lista de colores
    color = constants.COLORES[list(constants.COLORES.keys())[0]]

    # instancie el jugador
    jugador = Jugador(color, "pepitoperez", 3)

    # Instancie la ficha
    ficha = Ficha(jugador)

    salida_esperada = {
      'posicion': 3 * 17,
      'encarcelada': True,
      'coronada': False,
      'recta_final': False
    }

    self.assertEqual(ficha.dump_object(), salida_esperada)

if __name__ == '__main__':
    unittest.main()
