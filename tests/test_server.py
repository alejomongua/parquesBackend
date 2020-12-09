import unittest
import json
import copy
from unittest.mock import Mock
from fastapi.testclient import TestClient

from juego import my_firebase
import server.main as server

app = server.app

client = TestClient(app)

increment = 0


def side_effect(game):
    global increment
    if game.id is None:
        game.id = str(increment)
        increment += 1
    return game.public_state()


PUBLIC_GAMES_LIST_SAMPLE = {
    "-MKlw6VSTSf-FPBaTxfB": {
        "created_at": 1603934385.9833121,
        "jugadores": 0,
        "posiciones": 4
    },
    "-MKlxam1Zjtz14wZgMNp": {
        "created_at": 1603934776.2540152,
        "jugadores": 0,
        "posiciones": 4
    },
    "-MKm6cJ_TwMAEaTpBiQn": {
        "created_at": 1603937403.9798372,
        "jugadores": 0,
        "posiciones": 4
    },
    "-MKm8JvbKJmMAumJbmoU": {
        "created_at": 1603937848.809657,
        "jugadores": 0,
        "posiciones": 4
    },
    "-ML3-HtshKPcKrME5Jk6": {
        "created_at": 1604237470.857504,
        "jugadores": 0,
        "posiciones": 4
    }
}

SAMPLE_GAME = {
    "created_at": 1.6043444810811784E9,
    "finalizado": False,
    "id": "-ML9NVMSoCEMg750atw4",
    "iniciado": False,
    "last_turn": 1.6043444810811965E9,
    "publico": True,
    "tablero": {
        "colores": [False, False, False, False]
    },
    "turno": {
        "intentos": 3,
        "lanzado": False,
        "locked": [False, False, False, False]
    }
}

DEFAULT_PLAYERS = [{
    "color": "Naranja",
    "fichas": [{
        "coronada": False,
        "encarcelada": True,
        "posicion": 17,
        "recta_final": False
    }, {
        "coronada": False,
        "encarcelada": True,
        "posicion": 17,
        "recta_final": False
    }, {
        "coronada": False,
        "encarcelada": True,
        "posicion": 17,
        "recta_final": False
    }, {
        "coronada": False,
        "encarcelada": True,
        "posicion": 17,
        "recta_final": False
    }],
    "finalizado": False,
    "key": "e58b050d-2c40-40b6-b491-eccecada7df0",
    "nickname": "Matías",
    "retirado": False,
    "salida": 17
}, {
    "color": "Azul oscuro",
    "fichas": [{
        "coronada": False,
        "encarcelada": True,
        "posicion": 85,
        "recta_final": False
    }, {
        "coronada": False,
        "encarcelada": True,
        "posicion": 85,
        "recta_final": False
    }, {
        "coronada": False,
        "encarcelada": True,
        "posicion": 85,
        "recta_final": False
    }, {
        "coronada": False,
        "encarcelada": True,
        "posicion": 85,
        "recta_final": False
    }],
    "finalizado": False,
    "key": "b696ca1e-d369-4483-a81c-78472f1eafa0",
    "nickname": "Alejo",
    "retirado": False,
    "salida": 85
}]

DEFAULT_TABLERO = {'colores': ['Azul oscuro', 'Naranja', False, False]}

my_firebase.register_game = Mock(side_effect=side_effect)
my_firebase.public_registry_delete = Mock()
my_firebase.public_registry_update = Mock()
my_firebase.list_public = Mock(return_value=PUBLIC_GAMES_LIST_SAMPLE)


class ServerTest(unittest.TestCase):
    def test_lista_de_juegos_publicos(self):
        response = client.get('/juegos')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        primera_llave = list(respuesta.keys())[0]
        self.assertIsInstance(respuesta[primera_llave], dict)
        self.assertIsInstance(respuesta[primera_llave]['created_at'], float)
        self.assertIsInstance(respuesta[primera_llave]['jugadores'], int)
        self.assertIsInstance(respuesta[primera_llave]['posiciones'], int)

    def test_crear_partida(self):
        response = client.get('/juegos/crear_partida')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['tablero']['colores'], [
                         False, False, False, False])
        self.assertEqual(respuesta['jugadores'], [])
        self.assertIsInstance(respuesta['id'], str)

    def test_estado_del_juego(self):
        my_firebase.get_game = Mock(return_value=SAMPLE_GAME)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['id'], SAMPLE_GAME['id'])

    def test_unirse(self):
        my_firebase.get_game = Mock(return_value=SAMPLE_GAME)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/unirse',
                              params={'color': 'Azul', 'nickname': 'Alejandro'})
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['success'], True)
        self.assertIsInstance(respuesta['key'], str)

    def test_iniciar(self):
        mocked_response = copy.deepcopy(SAMPLE_GAME)
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        mocked_response['tablero'] = DEFAULT_TABLERO
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/iniciar')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['id'], SAMPLE_GAME['id'])

    def test_lanzar_dado(self):
        mocked_response = copy.deepcopy(SAMPLE_GAME)
        jugador = copy.deepcopy(DEFAULT_PLAYERS[0])
        # Saque una ficha de la carcel para que no lance tres veces
        jugador['fichas'][0]['encarcelada'] = False
        mocked_response['jugadores'] = [jugador, DEFAULT_PLAYERS[1]]
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            "acciones": None,
            "color": jugador['color'],
            "color_soplable": False,
            "dado1": None,
            "dado2": None,
            "intentos": 1,
            "lanzado": False,
            "locked": [False, False, False, False],
            "pares": None
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get(
            '/juegos/-ML3-HtshKPcKrME5Jk6/lanzar_dado', headers={'player-key': jugador['key']})
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertTrue(respuesta['turno']['lanzado'])
        self.assertTrue(respuesta['turno']['dado1'] is not None)
        self.assertTrue(respuesta['turno']['dado2'] is not None)

    def test_mover_ficha(self):
        mocked_response = copy.deepcopy(SAMPLE_GAME)
        jugador = copy.deepcopy(DEFAULT_PLAYERS[0])
        # Saque una ficha de la carcel
        jugador['fichas'][0]['encarcelada'] = False
        mocked_response['jugadores'] = [jugador, DEFAULT_PLAYERS[1]]
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            "acciones": {
                "dado1": 4,
                "dado2": 5
            },
            "color": jugador['color'],
            "color_soplable": False,
            "dado1": 4,
            "dado2": 5,
            "intentos": 1,
            "lanzado": True,
            "locked": [False, False, False, False],
            "pares": None
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        params = {
            'ficha': 0,
            'casillas': 9
        }
        headers = {
            'player-key': jugador['key']
        }
        response = client.get(
            '/juegos/-ML3-HtshKPcKrME5Jk6/mover_ficha', params=params, headers=headers)
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['jugadores'][0]['fichas']
                         [0]['posicion'], jugador['salida'] + 9)

    def test_sacar_de_la_carcel(self):
        mocked_response = copy.deepcopy(SAMPLE_GAME)
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            "acciones": {
                "dado1": 5,
                "dado2": 5
            },
            "color": DEFAULT_PLAYERS[0]['color'],
            "color_soplable": False,
            "dado1": 5,
            "dado2": 5,
            "intentos": 1,
            "lanzado": True,
            "locked": [False, False, False, False],
            "pares": 1
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/sacar_de_la_carcel',
                              headers={'player-key': DEFAULT_PLAYERS[0]['key']})
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        # Debería sacar dos fichas de la carcel
        self.assertFalse(respuesta['jugadores'][0]['fichas'][0]['encarcelada'])
        self.assertFalse(respuesta['jugadores'][0]['fichas'][1]['encarcelada'])
        self.assertTrue(respuesta['jugadores'][0]['fichas'][2]['encarcelada'])
        self.assertTrue(respuesta['jugadores'][0]['fichas'][3]['encarcelada'])

    def test_soplar(self):
        mocked_response = copy.deepcopy(SAMPLE_GAME)
        jugador = copy.deepcopy(DEFAULT_PLAYERS[0])
        # Saque una ficha de la carcel
        jugador['fichas'][0]['encarcelada'] = False
        jugador['fichas'][1]['encarcelada'] = False
        mocked_response['jugadores'] = [jugador, DEFAULT_PLAYERS[1]]
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            "acciones": {
                "dado1": 5,
                "dado2": 5,
                "movio_dado_1": 0,
                "comio_dado_1": False,
                "posiciones": [27, 17, 17, 17]
            },
            "color": DEFAULT_PLAYERS[1]['color'],
            "color_soplable": DEFAULT_PLAYERS[0]['color'],
            "dado1": None,
            "dado2": None,
            "intentos": 3,
            "lanzado": False,
            "locked": [False, False, False, False],
            "pares": 1
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        params = {
            'ficha': 0
        }
        headers = {
            'player-key': jugador['key'],
        }
        response = client.get(
            '/juegos/-ML3-HtshKPcKrME5Jk6/soplar', params=params, headers=headers)
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertTrue(respuesta['jugadores'][0]['fichas'][0]['encarcelada'])
        self.assertFalse(respuesta['jugadores'][0]['fichas'][1]['encarcelada'])

    def test_mi_color(self):
        mocked_response = copy.deepcopy(SAMPLE_GAME)
        jugador = copy.deepcopy(DEFAULT_PLAYERS[0])
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        # Saque una ficha de la carcel

        my_firebase.get_game = Mock(return_value=mocked_response)
        headers = {
            'player-key': jugador['key'],
        }
        response = client.get(
            '/juegos/-ML3-HtshKPcKrME5Jk6/mi_color', headers=headers)
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        self.assertLess(response.status_code, 300)
        self.assertGreaterEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertTrue(respuesta['color'] == jugador['color'])


if __name__ == '__main__':
    unittest.main()
