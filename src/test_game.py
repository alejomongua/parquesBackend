import unittest
from game import Game
from tablero import Tablero
from turno import Turno
from jugador import Jugador

class GameTest(unittest.TestCase):
  
  def test_new_game_default_values(self):
    # Cree un juego de 4 posiciones
    game = Game(4, False)

    # Verifique los valores por defecto
    self.assertIsInstance(game.tablero, Tablero)
    self.assertIsInstance(game.jugadores, list)
    self.assertEqual(len(game.jugadores), 0)
    self.assertEqual(game.publico, False)
    self.assertIsInstance(game.turno, Turno)

  def test_new_game_posiciones(self):
    # Cree un juego de 4 posiciones
    game = Game(4, False)

    # Verifique que si tenga 4 posiciones
    self.assertEqual(game.tablero.posiciones, 4)

    # Cree un juego de 6 posiciones
    game = Game(6, False)

    # Verifique que si tenga 6 posiciones
    self.assertEqual(game.tablero.posiciones, 6)

    # Cree un juego de 8 posiciones
    game = Game(8, False)

    # Verifique que si tenga 8 posiciones
    self.assertEqual(game.tablero.posiciones, 8)

    # No debe dejar crear tableros de 3 posiciones
    with self.assertRaises(ValueError):
      Game(3, False)

    # No debe dejar crear tableros de 10 posiciones
    with self.assertRaises(ValueError):
      Game(10, False)

  def test_new_game_publico(self):
    # Cree un juego público
    game = Game(4, True)

    # Verifique que sea público
    self.assertEqual(game.publico, True)

  def test_dump_object(self):
    game = Game(4, False)

    resultado = game.dump_object()
    self.assertEqual(resultado['id'], game.id)
    self.assertIsInstance(resultado['tablero'], Tablero)
    self.assertIsInstance(resultado['jugadores'], list)
    self.assertEqual(len(resultado['jugadores']), 0)

  def test_get_from_database(self):
    game1 = Game(4, False)
    game2 = Game.retrieve_from_database(game1.id)

    self.assertEqual(game1.dump_object(), game2.dump_object())

  def test_join_game(self):
    game = Game(4, False)

    # Instancie un color
    color = constants.COLORES.keys()[0]

    # Agrega un jugador
    game.join(color, 'pepitoperez')

    # El numero de jugadores incrementa en uno
    self.assertEqual(len(game.jugadores), 1)

    # No deja unirse con el mismo color
    self.assertRaise():
      game.join(color, 'otrojugador')

    # Cree un juego nuevo
    game = Game(4, False)

    # Agregue 4 jugadores
    for counter in range(4):
      game.join(constants.COLORES.keys()[counter], f'jugador{counter}')

    # No deja agregar mas del numero de posiciones
    with self.assertRaise():
      game.join(constans.COLORES.keys()[-1])

  def test_start_game(self):
    game = Game(4, False)

    # No debe dejar iniciar sin jugadores
    with self.assertRaise():
      game.start()

    # Agregue un jugador
    color = constants.COLORES.keys()[0]
    game.join(color, color)

    # No debe dejar iniciar con un solo jugador
    with self.assertRaise():
      game.start()

    # Agregue otro jugador
    color, constants.COLORES.keys()[1]
    game.join(color, color)

    # Inicie el juego
    game.start()

    # Deja iniciar el juego
    self.assertEqual(game.iniciado, True)
    self.assertIsNotNone(game.started_at)

    # No deja unirse a un juego iniciado
    color = constants.COLORES.keys()[2]
    with self.assertRaise():
      game.join(color, color)

  def test_lanzar(self):
    # Instancie un juego
    game = Game(4, False)

    # Agregue los jugadores
    for counter in range(4):
      game.join(constants.COLORES.keys()[0], f'jugador{counter}')

    # Inicie el juego
    game.start()

    # Intente lanzar con un jugador que no sea el primero
    self.assertRaise():
      game.lanzar(game.jugadores[-1])

    # Lance con el primer jugador
    game.lanzar(game.jugadores[0])

    # Verifique que los dados se hayan lanzado
    self.assertIsNotNone(game.turno.dado1)
    self.assertIsNotNone(game.turno.dado2)

    # Verifique que aun es el turno del primer jugador (tiene tres tiros al iniciar)
    self.assertEqual(game.turno.color, game.jugadores[0].color)

  def test_sacar_de_la_carcel(self):
    pass

  def test_mover(self):
    pass

  def test_soplar(self):
    pass

  def test_coronar(self):
    pass

if __name__ == '__main__':
    unittest.main()
