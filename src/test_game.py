import unittest
from game import Game
from tablero import Tablero
from turno import Turno
from jugador import Jugador
import constants

def iniciar_juego(jugadores: int):
  # Instancie un juego
  game = Game.create(4, False)

  # Agregue los jugadores
  for counter in range(4):
    game.join(constants.COLORES.keys()[0], f'jugador{counter}')

  # Inicie el juego
  game.start()

  return game

def sacar_de_la_carcel(game: Game, cantidad: int = 4):
  for jugador in game.jugadores:
    for contador in range(cantidad):
      ficha = jugador.fichas[contador]
      ficha.encarcelada = False

class GameTest(unittest.TestCase):

  def test_new_game_default_values(self):
    # Cree un juego de 4 posiciones
    game = Game.create(4, False)

    # Verifique los valores por defecto
    self.assertIsInstance(game.tablero, Tablero)
    self.assertIsInstance(game.jugadores, list)
    self.assertEqual(len(game.jugadores), 0)
    self.assertEqual(game.publico, False)
    self.assertIsInstance(game.turno, Turno)

  def test_new_game_posiciones(self):
    # Cree un juego de 4 posiciones
    game = Game.create(4, False)

    # Verifique que si tenga 4 posiciones
    self.assertEqual(game.tablero.posiciones, 4)

    # Cree un juego de 6 posiciones
    game = Game.create(6, False)

    # Verifique que si tenga 6 posiciones
    self.assertEqual(game.tablero.posiciones, 6)

    # Cree un juego de 8 posiciones
    game = Game.create(8, False)

    # Verifique que si tenga 8 posiciones
    self.assertEqual(game.tablero.posiciones, 8)

    # No debe dejar crear tableros de 3 posiciones
    game = Game.create(3, False)
    self.assertIsNotInstance(game, Game)

    # No debe dejar crear tableros de 10 posiciones
    game = Game.create(10, False)
    self.assertIsNotInstance(game, Game)

  def test_new_game_publico(self):
    # Cree un juego público
    game = Game.create(4, True)

    # Verifique que sea público
    self.assertEqual(game.publico, True)

  def test_dump_object(self):
    game = Game.create(4, False)

    resultado = game.dump_object()
    self.assertEqual(resultado['id'], game.id)
    self.assertIsInstance(resultado['tablero'], Tablero)
    self.assertIsInstance(resultado['jugadores'], list)
    self.assertEqual(len(resultado['jugadores']), 0)

  def test_get_from_database(self):
    game1 = Game.create(4, False)
    game2 = Game.retrieve_from_database(game1.id)

    self.assertEqual(game1.dump_object(), game2.dump_object())

  def test_join_game(self):
    game = Game.create(4, False)

    # Instancie un color
    color = constants.COLORES.keys()[0]

    # Agrega un jugador
    game.join(color, 'pepitoperez')

    # El numero de jugadores incrementa en uno
    self.assertEqual(len(game.jugadores), 1)

    # No deja unirse con el mismo color
    resultado = game.join(color, 'otrojugador')

    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(len(game.jugadores), 1)

    # Cree un juego nuevo
    game = Game.create(4, False)

    # Agregue 4 jugadores
    for counter in range(4):
      game.join(constants.COLORES.keys()[counter], f'jugador{counter}')

    # No deja agregar mas del numero de posiciones
    resultado = game.join(constants.COLORES.keys()[-1], constants.COLORES.keys()[-1])

    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(len(game.jugadores), 4)

  def test_start_game(self):
    game = Game.create([5~]4, False)

    # No debe dejar iniciar sin jugadores
    resultado = game.start()

    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertFalse(game.iniciado)

    # Agregue un jugador
    color = constants.COLORES.keys()[0]
    game.join(color, color)

    # No debe dejar iniciar con un solo jugador
    resultado = game.start()

    self.assertDictContainsSubset(resultado, { 'error': True })
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

    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(len(game.jugadores), 2)

  def test_lanzar(self):
    # Inicie un juego de 4 jugadores
    game = iniciar_juego(4)

    # Intente lanzar con un jugador que no sea el primero
    resultado = game.lanzar(game.jugadores[-1])

    self.assertDictContainsSubset(resultado, { 'error': True })
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
    sacar_de_la_carcel(game)

    # Lance los dados
    resultado = game.lanzar(game.jugadores[0])

    # No debe haber error
    with self.assertRaises(KeyError):
      resultado['error']

    # Intente volver a lanzar los dados sin haber movido
    resultado = game.lanzar(game.jugadores[0])

    # Debe generar un error
    self.assertDictContainsSubset(resultado, { 'error': True })

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

      self.assertDictContainsSubset(resultado, { 'error': True })
      self.assertTrue(all([ficha.encarcelada for ficha in jugador_actual.fichas]))

  def test_movimientos_ilegales(self):
    # Inicia el juego
    game = iniciar_juego(4)

    # Saca las fichas de la carcel
    sacar_de_la_carcel(game)

    # Lance los dados
    game.lanzar(game.jugadores[0])

    # Intente mover con otro jugador
    resultado = game.mover(game.jugadores[-1].fichas[0], game.turno.dado1)

    # Debe generar error
    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(game.jugadores[-1].fichas[0].posicion, game.jugadores[-1].salida)

    # Intente mover con el jugador correcto un numero incorrecto de casillas
    resultado = game.mover(game.jugadores[0].fichas[0], game.turno.dado1 + game.turno.dado2 - 1)
    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(game.jugadores[0].fichas[0].posicion, game.jugadores[0].salida)

    # Intente mover una ficha encarcelada
    game.jugadores[0].fichas[0].encarcelada = True
    resultado = game.mover(game.jugadores[0].fichas[0], game.turno.dado1)
    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(game.jugadores[0].fichas[0].posicion, game.jugadores[0].salida)

    # Intente mover una ficha coronada
    game.jugadores[0].fichas[0].encarcelada = False
    game.jugadores[0].fichas[0].coronada = True
    resultado = game.mover(game.jugadores[0].fichas[0], game.turno.dado1)
    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(game.jugadores[0].fichas[0].posicion, game.jugadores[0].salida)

    # Ponga una ficha en la recta final a 2 pasos de coronar
    game.jugadores[0].fichas[1].recta_final = True
    game.jugadores[0].fichas[1].posicion = 6

    # Cambie el lanzamiento
    game.turno.dado1 = 6

    # Intente mover mas pasos de los que puede mover
    resultado = game.mover(game.jugadores[0].fichas[1], game.turno.dado1)
    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(game.jugadores[0].fichas[1].posicion, 6)

  def test_movimientos_legales(self):
    game = iniciar_juego(4)

    # Saca las fichas de la carcel
    sacar_de_la_carcel(game)

    # Lance los dados
    game.lanzar(game.jugadores[0])

    # Mueva el jugador correcto la cantidad de fichas de un dado
    resultado = game.mover(game.jugadores[0].fichas[0], game.turno.dado1)
    with self.assertRaises(KeyError):
      resultado['error']
    self.assertEqual(game.jugadores[0].fichas[0].posicion, game.jugadores[0].salida + game.turno.dado1)

    # Mueva lo del segundo dado con otra ficha
    resultado = game.mover(game.jugadores[0].fichas[1], game.turno.dado2)
    with self.assertRaises(KeyError):
      resultado['error']
    self.assertEqual(game.jugadores[0].fichas[1].posicion, game.jugadores[0].salida + game.turno.dado2)

    siguiente_jugador = game.jugadores[1]

    # Verifique si saco pares
    if game.turno.dado1 == game.turno.dado2:
      siguiente_jugador = game.jugadores[0]

    game.lanzar(siguiente_jugador)

    # Mueva la suma de ambos dados
    resultado = game.mover(siguiente_jugador.fichas[2], game.turno.dado1 + game.turno.dado2)
    with self.assertRaises(KeyError):
      resultado['error']
    self.assertEqual(siguiente_jugador.fichas[2].posicion, siguiente_jugador.salida + game.turno.dado1 + game.turno.dado2)

  def test_sacar_de_la_carcel_y_mover(self):
    # Inicie un juego nuevo
    game = iniciar_juego(4)

    # Saque tres fichas de la carcel de cada jugador
    sacar_de_la_carcel(game, 3)

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
        resultado = game.sacar_de_la_carcel(jugador_actual)
        with self.assertRaises(KeyError):
          resultado['error']

        # No debe tener ninguna ficha en la carcel
        self.assertTrue(all([not ficha.encarcelada for ficha in jugador_actual.fichas]))

        # Intente mover la ficha que salio de la carcel
        resultado = game.mover(jugador.fichas[3], game.turno.dado1)
        self.assertDictContainsSubset(resultado, { 'error': True })
        self.assertEqual(game.jugadores[0].fichas[3].posicion, game.jugadores[0].salida)

        # Intente mover la suma de los dos dados
        posicion_ficha0 = jugador.fichas[0].posicion
        resultado = game.mover(jugador.fichas[0], game.turno.dado1 + game.turno.dado2)
        self.assertDictContainsSubset(resultado, { 'error': True })
        self.assertEqual(game.jugadores[0].fichas[0].posicion, posicion_ficha0)

        # Mueva el resultado de un dado
        resultado = game.mover(jugador.fichas[0], game.turno.dado1)
        with self.assertRaises(KeyError):
          resultado['error']
        self.assertEqual(game.jugadores[0].fichas[0].posicion, posicion_ficha0 + game.turno.dado1)

        # El contador de pares debe ser 0 porque salio de la carcel
        self.assertEqual(game.turno.pares, 0)

        # El siguiente turno debe ser del mismo jugador
        self.assertEqual(game.turno.color, jugador_actual.color)
        break

      # Si no saca pares mueva para que sea el turno del siguiente jugador
      game.mover(jugador_actual.fichas[0], game.turno.dado1 + game.turno.dado2)

      # Devuelva la ficha para hacer las pruebas predecibles
      jugador_actual.fichas[0].posicion = jugador_actual.salida

  def test_meter_a_la_carcel(self):
    game = iniciar_juego(4)

    # Saca las fichas de la carcel
    sacar_de_la_carcel(game)

    # Ubique las fichas para la prueba
    game.jugadores[0].fichas[3].posicion = game.jugadores[0].salida + 4
    game.jugadores[2].fichas[0].posicion = game.jugadores[0].salida + 5

    # Lance los dados
    game.lanzar(game.jugadores[0])

    # ubique los dados para la prueba
    game.turno.dado1 = 5
    game.turno.dado2 = 4

    # Meta a la carcel la ficha del jugador 2
    game.mover(game.jugadores[0].fichas[0], 5)

    # Verifique que queda encarcelada
    self.assertTrue(game.jugadores[2].fichas[0].encarcelada)

    # Verifique que la ficha que movio no se vaya para la carcel
    self.assertFalse(game.jugadores[0].fichas[0].encarcelada)

    # Verifique que vuelve a la posicion incial
    self.assertEqual(game.jugadores[2].fichas[0].posicion, game.jugadores[2].salida)

    # Intente mover la misma ficha con la que metio a la carcel con el otro dado
    resultado = game.mover(game.jugadores[0].fichas[0], 4)

    # Verifique que no se puede
    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(game.jugadores[0].fichas[0].posicion, game.jugadores[0].salida + 5)

    # Mueva otra ficha donde ya tenia una el mismo jugador
    game.mover(game.jugadores[0].fichas[1], 4)

    # Verifique que no se va para la carcel ninguna de las dos
    self.assertFalse(game.jugadores[0].ficha[3].encarcelada)
    self.assertFalse(game.jugadores[0].ficha[1].encarcelada)

  def test_primer_seguro(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    # Ubique las fichas para la prueba
    game.jugadores[2].fichas[0].posicion = game.jugadores[0].salida + 7

    # ubique los dados para la prueba
    game.turno.dado1 = 5
    game.turno.dado2 = 2

    # Mueva a la misma casilla
    game.mover(game.jugadores[0].fichas[0], 7)

    # Verifique que no este encarcelada
    self.assertFalse(game.jugadores[2].ficha[0].encarcelada)

  def test_segundo_seguro(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    # Ubique las fichas para la prueba
    game.jugadores[2].fichas[0].posicion = game.jugadores[0].salida + 12

    # ubique los dados para la prueba
    game.turno.dado1 = 6
    game.turno.dado2 = 6

    # Mueva a la misma casilla
    game.mover(game.jugadores[0].fichas[0], 12)

    # Verifique que no este encarcelada
    self.assertFalse(game.jugadores[2].ficha[0].encarcelada)

  def test_salida_como_seguro(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    # Ubique las fichas para la prueba
    game.jugadores[2].fichas[0].posicion = game.jugadores[1].salida
    game.jugadores[0].fichas[0].posicion = game.jugadores[1].salida - 3

    # ubique los dados para la prueba
    game.turno.dado1 = 3

    # Mueva a la misma casilla
    game.mover(game.jugadores[0].fichas[0], 3)

    # Verifique que no este encarcelada
    self.assertFalse(game.jugadores[2].ficha[0].encarcelada)

  def test_meter_a_la_carcel_en_salida(self):
    game = iniciar_juego(4)

    # Repita los turnos hasta que saque pares
    while True:
      # Encuentre cual es jugador que sigue
      for jugador in game.jugadores:
        if jugador.color == game.turno.color:
          jugador_actual = jugador
          break

      # Meta las fichas del jugador actual a la carcel
      for ficha in jugador_actual.fichas:
        ficha.encarcelada = True

      # Otro jugador diferente al actual
      otro_jugador = game.jugadores[0]
      if jugador_actual.color == game.jugadores[0].color:
        otro_jugador = game.jugadores[1]

      # Saque las fichas del otro jugador de la carcel y pongalas todas
      # en la salida del jugador actual (que bruto!)
      for ficha in otro_jugador.fichas:
        ficha.encarcelada = False
        ficha.posicion = jugador_actual.salida

      # El jugador que corresponda lance los dados
      game.lanzar(jugador_actual)

      # Si saca pares
      if game.turno.dado1 == game.turno.dado2:
        # Saque las fichas de la carcel
        game.sacar_de_la_carcel(jugador_actual)

        # Todas las fichas del otro jugador deben estar encarceladas
        self.assertTrue(all([ficha.encarcelada for ficha in otro_jugador.fichas]))

        break

      # Si no saca pares mueva para que sea el turno del siguiente jugador
      game.mover(jugador_actual.fichas[0], game.turno.dado1 + game.turno.dado2)

      # Devuelva la ficha para hacer las pruebas predecibles
      jugador_actual.fichas[0].posicion = jugador_actual.salida

  def test_solo_una_ficha_sale_de_la_carcel_y_mueve(self):
    game = iniciar_juego(4)

    # Corone 3 de 4 fichas de cada jugador
    for jugador in game.jugadores:
      for contador in range(3):
        ficha = jugador.fichas[contador]
        ficha.coronada = True

    # Al salir de la carcel debe permitirle mover con la misma ficha
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

        # Debe poder mover la ficha que acaba de sacar de la carcel
        resultado = game.mover(jugador_actual.fichas[-1], game.turno.dado1)

        with self.assertRaises(KeyError):
          resultado['error']

        self.assertEqual(jugador_actual.fichas[-1].posicion, jugador_actual.salida + game.turno.dado1)
        break

  def test_solo_una_ficha_mueve_solo_un_dado_y_come(self)
    game = iniciar_juego(4)

    # Corone 3 de 4 fichas de cada jugador
    for contador in range(3):
      ficha = game.jugadores[0].fichas[contador]
      ficha.coronada = True

    # La unica ficha que le queda al jugador 1
    ficha = game.jugadores[0].fichas[-1]

    # pone una ficha al alcance de la primera
    game.jugadores[2].ficha[0].posicion = ficha.posicion + 4

    # Lance los dados
    game.lanzar(game.jugadores[0])

    # Organice los dados
    game.turno.dado1 = 4

    # Mueva la ficha
    game.move(ficha, 4)

    # Verifique que la otra ficha este en la carcel
    self.assertTrue(game.jugadores[2].ficha[0].encarcelada)

    # Intente mover el otro dado
    resultado = game.mover(ficha, game.turno.dado2)

    # Verifique que no se puede
    self.assertDictContainsSubset(resultado, { 'error': True })
    self.assertEqual(ficha, game.jugadores[0].salida + 4)

  def test_soplar_cuando_no_come(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    # Ponga una ficha al alcance
    game.jugadores[2].fichas[0].posicion = game.jugadores[0].salida + 4

    # Lance los dados y acomodelos
    game.lanzar(game.jugadores[0])
    game.turno.dado1 = 4

    # Mueva la ficha sin comerse la que podia comerse
    game.mover(game.jugadores[0].fichas[0], 4 + game.turno.dado2)

    # Sople la ficha que no comio
    resultado = game.soplar(game.jugadores[0].fichas[0])

    # Verifique que es procedente
    with self.assertRaises(KeyError):
      resultado['error']

    # Verifique que la ficha vaya a la carcel
    self.assertTrue(game.jugadores[0].fichas[0].encarcelada)

  def test_cuando_no_saca_de_la_carcel(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game, 2)

    # intentelo hasta que saque pares
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

        # Mueva una ficha en vez de sacar de la carcel
        game.mover(game.jugadores[0].fichas[0], game.turno.dado1 + game.turno.dado2)

        # Sople la ficha que movio
        resultado = game.soplar(game.jugadores[0].fichas[0])

        # Verifique que es procedente
        with self.assertRaises(KeyError):
          resultado['error']

        # Verifique que la ficha vaya a la carcel
        self.assertTrue(game.jugadores[0].fichas[0].encarcelada)

        break

      # Si no saca pares mueva para que sea el turno del siguiente jugador
      game.mover(jugador_actual.fichas[0], game.turno.dado1 + game.turno.dado2)

      # Devuelva la ficha para hacer las pruebas predecibles
      jugador_actual.fichas[0].posicion = jugador_actual.salida

  def test_soplar_cuando_no_procede(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    game.lanzar(game.jugadores[0])

    # Ponga una ficha en un seguro
    game.jugadores[2].fichas[0].posicion = game.jugadores[0].salida + 7

    # Lance los dados y acomodelos
    game.lanzar(game.jugadores[0])
    game.turno.dado1 = 4
    game.turno.dado2 = 3

    # Mueva la ficha sin comerse la que podia comerse
    game.mover(game.jugadores[0].fichas[0], 7)

    # Sople la ficha que movio
    resultado = game.soplar(game.jugadores[0].fichas[0])

    # Verifique que es procedente
    self.assertDictContainsSubset(resultado, { 'error': True })

    # Verifique que la ficha no vaya a la carcel
    self.assertFalse(game.jugadores[0].fichas[0].encarcelada)

  def test_coronar(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    # Ponga a una ficha a tres de ganar
    ficha = game.jugadores[0].fichas[0]
    ficha.recta_final = True
    ficha.posicion = 5 # Se gana en 8

    # Lance y acomode los dados
    game.lanzar(game.jugadores[0])
    game.turno.dado1 = 3

    # Corone la ficha
    game.mover(ficha, 3)

    # Verifique que la ficha queda coronada
    self.assertTrue(ficha.coronada)

  def test_coronar_con_pares(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    # Repita los turnos hasta que saque pares
    while True:
      # Encuentre cual es jugador que sigue
      for jugador in game.jugadores:
        if jugador.color == game.turno.color:
          jugador_actual = jugador
          break

      # El jugador tiene dos pares seguidos
      game.turno.pares = 2

      # El jugador que corresponda lance los dados
      game.lanzar(jugador_actual)

      # Si saca pares
      if game.turno.dado1 == game.turno.dado2:
        resultado = game.coronar(game.jugadores[0].fichas[0])

        # Verifique que no hay error
        with self.assertRaises(KeyError):
          resultado['error']

        # Verifique que la ficha si fue coronada
        self.assertTrue(game.jugadores.fichas[0].coronada)

        break

      # else (si no saco pares)
      # Intente coronar sin haber sacado pares
      resultado = game.coronar(game.jugadores[0].fichas[0])

      # Verifique que no es procedente
      self.assertDictContainsSubset(resultado, { 'error': True })

      # Verifique que la ficha no este coronada
      self.assertFalse(game.jugadores[0].fichas[0].coronada)

      # Si no saca pares mueva para que sea el turno del siguiente jugador
      game.mover(jugador_actual.fichas[0], game.turno.dado1 + game.turno.dado2)

      # Devuelva la ficha para hacer las pruebas predecibles
      jugador_actual.fichas[0].posicion = jugador_actual.salida

  def test_ganar(self):
    game = iniciar_juego(4)

    sacar_de_la_carcel(game)

    # Corone todas las fichas del jugador 1 salvo 1
    for contador in range(3):
      ficha = game.jugadores[0].fichas[contador]
      ficha.coronada = True

    # Ponga la ultima ficha a tres de ganar
    ficha = game.jugadores[0].fichas[3]
    ficha.recta_final = 4
    ficha.posicion = 5 # gana cuando llega al 8

    # Lance y acomode los dados
    game.lanzar(game.jugadores[0])
    game.turno.dado1 = 3

    # Corone la ficha
    game.mover(ficha, 3)

    # Verifique que el jugador 1 haya ganado
    self.assertTrue(game.jugadores[0].finalizado)

if __name__ == '__main__':
    unittest.main()
