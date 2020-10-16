import unittest
from turno import Turno

class TurnoTest(unittest.TestCase):
  
  def test_dump_object(self):
    # instancie el turno
    turno = Turno()

    # Lláme el método
    resultado = turno.dump_object()
    
    # Estado por defecto
    default = {
      'color': None,
      'dado1': None,
      'dado2': None,
      'pares': None
    }

    self.assertEqual(resultado, default)

  def test_lanzar(self):
    # instancie el turno
    turno = Turno()

    # Lláme el método
    turno.lanzar(2)

    self.assertIsNotNone(turno.dado1)
    self.assertIsNotNone(turno.dado2)

    turno.lanzar(1)

    self.assertIsNotNone(turno.dado1)
    self.assertEqual(turno.dado2, 0)

  def test_pares(self):
    # instancie el turno
    turno = Turno()

    # Lance hasta que saque pares
    while True:
      turno.lanzar(2)
      if turno.dado1 == turno.dado2:
        break

    # Se debe incrementar el contador de pares
    self.assertEqual(turno.pares, 1)
    # En el juego, cuando saque de la carcel se debe decrementar
    # pero esto se hará desde el juego

    # Lance hasta que NO saque pares
    while True:
      turno.lanzar(2)
      if turno.dado1 != turno.dado2:
        break

    # El contador de pares debe volver a None
    self.assertIsNone(turno.pares)

  def test_siguiente_turno(self):
    # instancie el turno
    turno = Turno()

    # Lance hasta que NO saque pares
    while True:
      turno.lanzar(2)
      if turno.dado1 != turno.dado2:
        break

    # Nuevo turno
    turno.siguiente_turno('color')

    self.assertIsNone(turno.dado1)
    self.assertIsNone(turno.dado2)

if __name__ == '__main__':
    unittest.main()
