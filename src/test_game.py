import unittest
from game import Game
from tablero import Tablero
from turno import Turno
from jugador import Jugador
import constants

def iniciar_juego(jugadores: int):
  # Instancie un juego
  game = Game(4, False)

  # Agregue los jugadores
  for counter in range(4):
    game.join(constants.COLORES.keys()[0], f'jugador{counter}')

  # Inicie el juego
  game.start()

  return game

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
    with self.assertRaises(Exception):
      Game(3, False)

    # No debe dejar crear tableros de 10 posiciones
    with self.assertRaises(Exception):
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
    resultado = game.join(color, 'otrojugador')

    self.assertDictContainsSubset(resultado, { 'error', True })
    self.assertEqual(len(game.jugadores), 1)

    # Cree un juego nuevo
    game = Game(4, False)

    # Agregue 4 jugadores
    for counter in range(4):
      game.join(constants.COLORES.keys()[counter], f'jugador{counter}')

    # No deja agregar mas del numero de posiciones
    resultado = game.join(constants.COLORES.keys()[-1], constants.COLORES.keys()[-1])

    self.assertDictContainsSubset(resultado, { 'error', True })
    self.assertEqual(len(game.jugadores), 4)

  def test_start_game(self):
    game = Game(4, False)

    # No debe dejar iniciar sin jugadores
    resultado = game.start()

    self.assertDictContainsSubset(resultado, { 'error', True })
    self.assertFalse(game.iniciado)

    # Agregue un jugador
    color = constants.COLORES.keys()[0]
    game.join(color, color)

    # No debe dejar iniciar con un solo jugador
    resultado = game.start()

    self.assertDictContainsSubset(resultado, { 'error', True })
    self.assertFalse(game.iniciado)

    # Agregue otro jugador
    color, constants.COLORES.keys()[1]
    game.join(color, color)

    # Inicie el juego
    game.start()

    # Deja iniciar el juego
    self.assertTrue(game.iniciado)
    self.assertIsNotNone(game.started_at)
    self.assertIsNotNone(game.turno.color)

    # No deja unirse a un juego iniciado
    color = constants.COLORES.keys()[2]
    resultado = game.join(color, color)

    self.assertDictContainsSubset(resultado, { 'error', True })
    self.assertEqual(len(game.jugadores), 2)

  def test_lanzar(self):
    # Inicie un juego de 4 jugadores
    game = iniciar_juego(4)

    # Intente lanzar con un jugador que no sea el primero
    resultado = game.lanzar(game.jugadores[-1])

    self.assertDictContainsSubset(resultado, { 'error', True })
    self.assertIsNone(game.turno.dado1)
    self.assertIsNone(game.turno.dado2)

    # Lance con el primer jugador
    game.lanzar(game.jugadores[0])

    # Verifique que los dados se hayan lanzado
    self.assertIsNotNone(game.turno.dado1)
    self.assertIsNotNone(game.turno.dado2)

    # Verifique que aun es el turno del primer jugador (tiene tres tiros al iniciar)
    self.assertEqual(game.turno.color, game.jugadores[0].color)

  def test_no_deja_lanzar_cuando_ya_lanzo(self):
    # Inicie un juego de 4 jugadores
    game = iniciar_juego(4)

    # Saca las fichas de la carcel
    for ficha in game.jugadores[0].fichas:
      ficha.encarcelada = True

    # Lance los dados
    resultado = game.lanzar(game.jugadores[0])

    # No debe haber error
    with self.assertRaises(KeyError):
      resultado['error']

    # Intente volver a lanzar los dados sin haber movido
    resultado = game.lanzar(game.jugadores[0])

    # Debe generar un error
    self.assertDictContainsSubset(resultado, { 'error', True })

  def test_sacar_de_la_carcel(self):
    game = iniciar_juego(4)

    # Repita los turnos hasta que saque pares
    while True:
      # Encuentre cual es jugador que sigue
      for jugador in game.jugadores:
        if jugador.color == game.turno.color:
          jugador_actual = jugador
          break
      # El jugador que corresponda lance los dados
      game.lanzar(jugador_actual)

      # Si saca pares
      if game.turno.dado1 == game.turno.dado2:
        # Saque las fichas de la carcel
        game.sacar_de_la_carcel(jugador_actual)

        # Si es par de unos o par de seises
        if game.turno.dado1 == 1 or game.turno.dado1 == 6:
          # Si es par de unos o par de seis, saque todas las fichas
          self.assertTrue(all([not ficha.encarcelada for ficha in jugador_actual.fichas]))
        else:
          # Si es otro par saque solo dos fichas
          self.assertEqual(len([True for ficha in jugador_actual.fichas if not ficha.encarcelada]), 2)
        break

      # Si no saca pares no deja sacar de la carcel
      resultado = game.sacar_de_la_carcel(jugador_actual)

      self.assertDictContainsSubset(resultado, { 'error', True })
      self.assertTrue(all([ficha.encarcelada for ficha in jugador_actual.fichas]))

  def test_mover(self):
    # Inicia el juego
    game = iniciar_juego(4)

    # Saca las fichas de la carcel
    for jugador in game.jugadores:
      for ficha in jugador.fichas:
        ficha.encarcelada = True

    # Lance los dados
    game.lanzar(game.jugadores[0])

    # Intente mover con otro jugador
    resultado = game.mover(game.jugadores[-1], 0)

    # Debe generar error
    self.assertDictContainsSubset(resultado, { 'error', True })
    self.assertEqual(game.jugadores[-1].fichas[0].posicion, game.jugadores[-1].salida)

    # Intente mover con el jugador correcto
    resultado = game.mover(game.jugadores[0], 0)

  def test_soplar(self):
    pass

  def test_coronar(self):
    pass

if __name__ == '__main__':
    unittest.main()
