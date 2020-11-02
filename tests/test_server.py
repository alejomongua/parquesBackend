import unittest
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
    "created_at" : 1.6043444810811784E9,
    "finalizado" : False,
    "id" : "-ML9NVMSoCEMg750atw4",
    "iniciado" : False,
    "last_turn" : 1.6043444810811965E9,
    "publico" : True,
    "tablero" : {
        "colores" : [ False, False, False, False ]
    },
    "turno" : {
        "intentos" : 3,
        "lanzado" : False,
        "locked" : [ False, False, False, False ]
    }
}

DEFAULT_PLAYERS = [ {
    "color" : "Naranja",
    "fichas" : [ {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 17,
        "recta_final" : False
    }, {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 17,
        "recta_final" : False
    }, {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 17,
        "recta_final" : False
    }, {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 17,
        "recta_final" : False
    } ],
    "finalizado" : False,
    "key" : "e58b050d-2c40-40b6-b491-eccecada7df0",
    "nickname" : "Matías",
    "retirado" : False,
    "salida" : 17
    }, {
    "color" : "Azul oscuro",
    "fichas" : [ {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 85,
        "recta_final" : False
    }, {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 85,
        "recta_final" : False
    }, {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 85,
        "recta_final" : False
    }, {
        "coronada" : False,
        "encarcelada" : True,
        "posicion" : 85,
        "recta_final" : False
    } ],
    "finalizado" : False,
    "key" : "b696ca1e-d369-4483-a81c-78472f1eafa0",
    "nickname" : "Alejo",
    "retirado" : False,
    "salida" : 85
} ]

DEFAULT_TABLERO = { 'colores': ['Azul oscuro', 'Naranja', False, False] }

my_firebase.register_game = Mock(side_effect=side_effect)
my_firebase.public_registry_delete = Mock()
my_firebase.public_registry_update = Mock()
my_firebase.list_public = Mock(return_value=PUBLIC_GAMES_LIST_SAMPLE)
my_firebase.get_game = Mock(return_value=SAMPLE_GAME)

class ServerTest(unittest.TestCase):
    def test_lista_de_juegos_publicos(self):
        response = client.get('/juegos')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
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
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['tablero']['colores'], [False, False, False, False])
        self.assertEqual(respuesta['jugadores'], [])
        self.assertIsInstance(respuesta['id'], str)

    def test_estado_del_juego(self):
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['id'], SAMPLE_GAME['id'])

    def test_unirse(self):
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/unirse', params={ 'color': 'Azul', 'nickname': 'Alejandro' })
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['success'], True)
        self.assertIsInstance(respuesta['key'], str)

    def test_iniciar(self):
        mocked_response = SAMPLE_GAME.copy()
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        mocked_response['tablero'] = DEFAULT_TABLERO
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/iniciar')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        with self.assertRaises(KeyError):
            respuesta['error']
        self.assertEqual(respuesta['id'], SAMPLE_GAME['id'])

    def test_lanzar_dado(self):
        mocked_response = SAMPLE_GAME.copy()
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            "acciones" : None,
            "color" : "Naranja",
            "color_soplable" : False,
            "dado1" : None,
            "dado2" : None,
            "intentos" : 3,
            "lanzado" : False,
            "locked" : [ False, False, False, False ],
            "pares" : None
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/lanzar_dado', params={})
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        with self.assertRaises(KeyError):
            respuesta['error']
        # to do

    def test_mover_ficha(self):
        mocked_response = SAMPLE_GAME.copy()
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            # to do
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/mover_ficha')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        with self.assertRaises(KeyError):
            respuesta['error']
        # to do

    def test_sacar_de_la_carcel(self):
        mocked_response = SAMPLE_GAME.copy()
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            # to do
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/sacar_de_la_carcel')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        with self.assertRaises(KeyError):
            respuesta['error']
        # to do

    def test_soplar(self):
        mocked_response = SAMPLE_GAME.copy()
        mocked_response['jugadores'] = DEFAULT_PLAYERS
        mocked_response['tablero'] = DEFAULT_TABLERO
        mocked_response['iniciado'] = True
        mocked_response['turno'] = {
            # to do
        }
        my_firebase.get_game = Mock(return_value=mocked_response)
        response = client.get('/juegos/-ML3-HtshKPcKrME5Jk6/soplar')
        respuesta = response.json()
        self.assertIsInstance(respuesta, dict)
        with self.assertRaises(KeyError):
            respuesta['error']
        # to do

if __name__ == '__main__':
    unittest.main()
