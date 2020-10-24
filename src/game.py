import time
import uuid
import random

# import my_firebase
from tablero import Tablero
from jugador import Jugador
from turno import Turno
import constants

class Game():
    """Clase principal del juego"""

    def __init__(self, publico: bool = False):
        self.publico = publico
        self.iniciado = False
        self.finalizado = False
        self.created_at = time.time()
        self.started_at = None
        self.last_turn = None
        self.jugadores = []
        # En el atributo fichas_en_casillas, las llaves son los números de casilla
        # y el valor es un array de fichas de colores, esta variable sirve para no
        # tener que iterar por cada ficha cada vez que quiero verificar si una ficha
        # puede comer
        self.fichas_en_casillas = {}
        # Estos se deben asignar después de crear el juego
        self.id = None
        self.turno = None
        self.tablero = None
    
    def dump_object(self):
        """Retorna el estado actual del objeto"""
        return {
            'id': self.id,
            'tablero': self.tablero.dump_object(),
            'jugadores': [jugador.dump_object() for jugador in self.jugadores],
            'finalizado': self.finalizado,
            'inicio': self.created_at,
            'ultimo_turno': self.last_turn
        }

    def join(self, color: str, nickname: str):
        """Se agrega un jugador a la partida"""
        if not color in constants.COLORES:
            mensaje = f'El color no es válido, debe ser una de estas opciones: {list(constants.COLORES.keys())}'
            return {
                'error': True,
                'mensaje': mensaje
            }

        if len(self.jugadores) >= self.tablero.posiciones:
            return {
                'error': True,
                'mensaje': 'Ya se alcanzó el máximo de jugadores para esta partida'
            }

        if color in self.tablero.colores:
            return {
                'error': True,
                'mensaje': f'El color {color} ya fue escogido, por favor escoja otro'
            }

        if self.iniciado:
            return {
                'error': True,
                'mensaje': 'No se puede unir a esta partida porque ya inició'
            }

        jugador = Jugador(color, nickname)
        jugador.key = str(uuid.uuid4())
        self.jugadores.append(jugador)
        self.tablero.add_color(color)
        return {
            'success': True,
            'key': jugador.key
        }

    def start(self):
        """Se inicia la partida, ya no se pueden unir más jugadores"""
        if len(self.jugadores) < 2:
            return {
                'error': True,
                'mensaje': 'No se puede iniciar la partida porque hay muy pocos jugadores'
            }

        # RANDOMIZACION

        # Orden aleatorio de los turnos de los jugadores
        random.shuffle(self.tablero.colores)

        # Establece el orden de los jugadores
        temp_jugadores = self.jugadores
        self.jugadores = []
        indice = 0
        for color in self.tablero.colores:
            if color is not None:
                # Encuentre el jugador por el color
                for jugador in temp_jugadores:
                    if jugador.color == color:
                        # Asigne las salidas
                        jugador.salida = indice * 17
                        # ponga las fichas en su posicion
                        for ficha in jugador.fichas:
                            ficha.posicion = jugador.salida
                        # Asigne el jugador al arreglo
                        self.jugadores.append(jugador)
                        break
            indice += 1
        # FIN RANDOMIZACION

        # Asigna el primer turno
        self.turno.color = self.jugadores[0].color
        self.turno.intentos = 3

        # Marca el inicio del juego
        self.started_at = time.time()
        self.iniciado = True

        return self.almacenar()

    def lanzar(self, player_key: str):
        """Realiza un lanzamiento de dados"""
        jugador = self.encontrar_jugador(player_key)

        if jugador is None:
            return {
                'error': True,
                'mensaje': 'La llave no coincide con ningún jugador en este juego'
            }

        if self.turno.color != jugador.color:
            return {
                'error': True,
                'mensaje': 'Espere su turno'
            }

        if all([ficha.encarcelada for ficha in jugador.fichas if not ficha.coronada]):
            self.turno.lanzar(2)

            self.turno.intentos -= 1

            if self.turno.intentos == 0 and self.turno.dado1 != self.turno.dado2:
                self.siguiente_turno()
        else:
            if self.turno.dado1 is not None:
                return {
                    'error': True,
                    'mensaje': 'No es momento de lanzar los dados'
                }

            self.turno.lanzar(jugador.cantidad_dados())

            # Verifica las fichas en las casillas: Itera sobre cada ficha de cada
            # jugador que no esté encarcelada ni coronada ni en la carcel para
            # crear un diccionario con las fichas que hay en cada casilla del
            # tablero

            # primero inicializa todo
            self.fichas_en_casillas = {}

            # Itera sobre cada ficha de cada jugador
            for jugador1 in self.jugadores:
                # Excluye las fichas del jugador actual
                if jugador1.color == self.turno.color:
                    continue

                for ficha in range(4):
                    ficha1 = jugador1.fichas[ficha]
                    # que no esté ni coronada ni encarcelada ni en la recta final
                    if any([ficha1.encarcelada, ficha1.coronada, ficha1.recta_final]):
                        continue

                    # Crea una lista de listas por cada casilla ocupada
                    if not ficha1.posicion in self.fichas_en_casillas:
                        self.fichas_en_casillas[ficha1.posicion] = [[jugador1.color, ficha]]
                    else:
                        self.fichas_en_casillas[ficha1.posicion].append([jugador1.color, ficha])

            # Almacene la posición actual de las fichas del jugador actual, esto
            # con el fin de saber si cuando se sople es o no procedente
            self.turno.acciones['posiciones'] = [ficha.posicion for ficha in jugador.fichas]

            # Verifique cuales fichas no se pueden mover
            self.turno.locked = []
            todas_bloqueadas = True
            for ficha in jugador.fichas:
                locked = ficha.encarcelada or ficha.coronada
                if not locked and ficha.recta_final:
                    pasos_restantes = 8 - ficha.posicion
                    if self.turno.dado1 > pasos_restantes and (self.turno.dado2 == 0 or self.turno.dado2 > pasos_restantes):
                        locked = True
                if not locked:
                    todas_bloqueadas = False
                self.turno.locked.append(locked)

            # Si todas las fichas están bloqueadas, es el turno del siguiente jugador
            if todas_bloqueadas:
                if self.turno.pares is None:
                    self.siguiente_turno()
                else:
                    self.turno.siguiente_turno(self.turno.color)

        # Incremente el contador de pares si aplica
        if self.turno.dado1 == self.turno.dado2:
            if self.turno.pares is None:
                self.turno.pares = 1
            else:
                self.turno.pares += 1
        else:
            self.turno.pares = None

        return self.almacenar()

    def mover(self, player_key: str, ficha: int, cantidad: int):
        jugador = self.encontrar_jugador(player_key)

        if jugador is None:
            return {
                'error': True,
                'mensaje': 'La llave no coincide con ningún jugador en este juego'
            }

        if ficha > len(jugador.fichas):
            return {
                'error': True,
                'mensaje': 'Ficha erronea'
            }

        if self.turno.color != jugador.color:
            return {
                'error': True,
                'mensaje': 'Espere su turno'
            }
        
        if self.turno.dado1 is None or self.turno.dado2 is None:
            return {
                'error': True,
                'mensaje': 'Debe lanzar los dados primero'
            }

        esta_ficha = jugador.fichas[ficha]
        cantidad_legal = cantidad == self.turno.dado1 or \
                         cantidad == self.turno.dado2 or \
                         cantidad == self.turno.dado1 + self.turno.dado2
        if esta_ficha.encarcelada or esta_ficha.coronada or \
           not cantidad_legal or cantidad == 0 or self.turno.locked[ficha]:
            return {
                'error': True,
                'mensaje': 'Movimiento ilegal'
            }

        # Este pedazo es complicado, porque toca considerar muchas cosas
        if esta_ficha.recta_final:
            # Si esta en la recta final, revise que la cantidad de pasos que quiere
            # mover sea menor que los que le falten
            if 8 - esta_ficha.posicion < cantidad:
                return {
                    'error': True,
                    'mensaje': 'Movimiento ilegal'
                }

            esta_ficha.posicion += cantidad

            if esta_ficha.posicion == 8:
                esta_ficha.coronada = True
                jugador.finalizado = all([ficha.coronada for ficha in jugador.fichas])


        else:
            # Si no esta en la recta final
            posicion_actual = esta_ficha.posicion
            llegada = (jugador.salida + self.tablero.posiciones * 17 - 5) % (self.tablero.posiciones * 17)

            for movimiento in range(cantidad):
                pasos_restantes = cantidad - movimiento - 1

                # Si llegó a la recta final:
                if posicion_actual + movimiento + 1 == llegada:
                    if pasos_restantes > 8:
                        return {
                            'error': True,
                            'mensaje': 'Movimiento ilegal'
                        }

                    else:
                        esta_ficha.recta_final = True
                        esta_ficha.posicion += pasos_restantes

                        if esta_ficha.posicion == 8:
                            esta_ficha.coronada = True
                            jugador.finalizado = all([ficha.coronada for ficha in jugador.fichas])

                else:
                    esta_ficha.posicion = (posicion_actual + movimiento + 1) % (self.tablero.posiciones * 17)

        # Revise si metió alguna ficha a la carcel
        comio = not self.tablero.seguro(esta_ficha.posicion) and \
                not esta_ficha.recta_final and \
                not self.tablero.salida(esta_ficha.posicion) and \
                esta_ficha.posicion in self.fichas_en_casillas
        ficha_que_se_comio = None
        if comio:
            # Bloquee la ficha para que no la pueda mover
            self.turno.locked[ficha] = True

            # Encuentre la ficha que se comió
            for color_ficha in self.fichas_en_casillas[esta_ficha.posicion]:
                color = color_ficha[0]
                # Encuentre el jugador por el color
                for otro_jugador in self.jugadores:
                    if otro_jugador.color == color:
                        otra_ficha = otro_jugador.fichas[color_ficha[1]]
                        # Lleve la ficha a la carcel
                        otra_ficha.encarcelada = True
                        otra_ficha.posicion = otro_jugador.salida
                        ficha_que_se_comio = [otro_jugador.color, esta_ficha.posicion]
                        break

            # En esta casilla solo deja este color en el mapa, para que si pone otra
            # ficha ahí mismo no cuente como si hubiera comido      
            self.fichas_en_casillas[esta_ficha.posicion] = [[jugador.color, ficha]]

        # Determine cuantos dados usó
        if cantidad == self.turno.dado1:
            self.turno.dado1 = 0
            self.turno.acciones['mover_dado_1'] = ficha
            self.turno.acciones['comio_dado_1'] = ficha_que_se_comio
        elif cantidad == self.turno.dado2:
            self.turno.dado2 = 0
            self.turno.acciones['mover_dado_2'] = ficha
            self.turno.acciones['comio_dado_2'] = ficha_que_se_comio
        else:
            self.turno.dado1 = 0
            self.turno.dado2 = 0
            self.turno.acciones['mover_dado_1'] = ficha
            self.turno.acciones['mover_dado_2'] = ficha
            self.turno.acciones['comio_dado_1'] = ficha_que_se_comio
            self.turno.acciones['comio_dado_2'] = ficha_que_se_comio

        if (self.turno.dado1 == 0 and self.turno.dado2 == 0) or all(self.turno.locked):
            if self.turno.pares is None:
                self.siguiente_turno()
            else:
                self.turno.siguiente_turno(self.turno.color)

        return self.almacenar()

    def sacar_de_la_carcel(self, player_key: str):
        """
        Saca fichas de la carcel, depende del par que sacó y de las fichas que
        estén en la carcel
        """
        jugador = self.encontrar_jugador(player_key)

        if jugador is None:
            return {
                'error': True,
                'mensaje': 'La llave no coincide con ningún jugador en este juego'
            }

        if self.turno.color != jugador.color:
            return {
                'error': True,
                'mensaje': 'Espere su turno'
            }
        
        if self.turno.dado1 is None or self.turno.dado2 is None:
            return {
                'error': True,
                'mensaje': 'Debe lanzar los dados primero'
            }

        if self.turno.dado1 != self.turno.dado2:
            return {
                'error': True,
                'mensaje': 'Necesita sacar pares para salir de la carcel'
            }

        # Si no tiene fichas en la carcel
        if len([0 for ficha in jugador.fichas if ficha.encarcelada]) == 0:
            return {
                'error': True,
                'mensaje': 'No tiene fichas en la carcel'
            }

        contador = 0

        # Almacene cuales fichas libera, para que no se pueda mover si es solo una
        fichas_liberadas = []
        for ficha in range(4):
            esta_ficha = jugador.fichas[ficha]
            if esta_ficha.encarcelada and not esta_ficha.coronada:
                esta_ficha.encarcelada = False
                fichas_liberadas.append(ficha)
                # Si no es par de 6 ni de 1, saque solo 2
                if self.turno.dado1 != 6 and self.turno.dado2 != 1:
                    contador += 1
                    if contador == 2:
                        break

        self.turno.dado2 = 0
        if len(fichas_liberadas) == 1:
            # Si le quedan más fichas, la ficha que sacó queda bloqueada
            cantidad_no_coronadas = len([0 for ficha in jugador.fichas if not ficha.coronada])
            if cantidad_no_coronadas != 1:
                self.turno.locked[fichas_liberadas[0]] = True
            self.turno.dado2 = 0
        else:
            self.turno.siguiente_turno(self.turno.color)

        # Meta a la carcel las fichas que estaban en la salida

        # Itera sobre cada ficha de cada jugador
        for jugador1 in self.jugadores:
            # Excluye las fichas del jugador actual
            if jugador1.color == self.turno.color:
                continue

            for ficha in range(4):
                ficha1 = jugador1.fichas[ficha]
                # que no esté ni coronada ni encarcelada ni en la recta final
                # Crea una lista de listas por cada casilla ocupada
                if not ficha1.posicion == jugador.salida:
                    ficha1.posicion = jugador1.salida
                    ficha1.encarcelada = True

        self.turno.pares = 0

        self.turno.acciones['sacar_de_la_carcel'] = True

        return self.almacenar()

    def coronar(self, player_key: str, ficha: int):
        """Corona una ficha por pares"""
        jugador = self.encontrar_jugador(player_key)

        if jugador is None:
            return {
                'error': True,
                'mensaje': 'La llave no coincide con ningún jugador en este juego'
            }

        if self.turno.pares is None or self.turno.pares < 3:
            return {
                'error': True,
                'mensaje': 'Tiene que sacar tres pares seguidos sin sacar de la carcel'
            }

        jugador.fichas[ficha].coronada = True
        jugador.finalizado = all([ficha.coronada for ficha in jugador.fichas])

        self.siguiente_turno()

        self.turno.acciones['coronar'] = True

        return self.almacenar()

    def soplar(self, player_key: str, ficha: int):
        """Sopla una ficha para enviarla a la carcel"""
        jugador = self.encontrar_jugador(player_key)

        if jugador is None:
            return {
                'error': True,
                'mensaje': 'La llave no coincide con ningún jugador en este juego'
            }

        if not self.turno.color_soplable:
            return {
                'error': True,
                'mensaje': 'No se puede soplar en este momento'
            }

        # Aquí viene la parte más complicada porque hay que considerar cada una de
        # las posibilidades para saber si el soplido procede o no

        ficha_soplable = False

        # Encuentre el jugador por el color
        jugador_soplable = None
        for jugador1 in self.jugadores:
            if jugador1.color == self.turno.color_soplable:
                jugador_soplable = jugador1
                break

        esta_ficha = jugador_soplable.fichas[ficha]

        movio_dado_1 = self.turno.acciones.get('movio_dado_1', None)
        movio_dado_2 = self.turno.acciones.get('movio_dado_2', None)
        comio_dado_1 = self.turno.acciones.get('comio_dado_1', False)
        comio_dado_2 = self.turno.acciones.get('comio_dado_2', False)
        dado1 = self.turno.acciones['dado1']
        dado2 = self.turno.acciones['dado2']
        # La primera bifurcación es si sacó o no pares
        if self.turno.pares is None:
            # Si no sacó pares, no se puede soplar si con cada dado se comió alguna
            # o si con la suma de los dados se comió alguna
            if self.turno.pares is None and comio_dado_1 and comio_dado_2:
                return {
                    'error': True,
                    'mensaje': 'No se puede soplar esa ficha'
                }

            # Si la ficha que están acusando si comió
            if (ficha == movio_dado_1 and comio_dado_1) or (ficha == movio_dado_2 and comio_dado_2):
                return {
                    'error': True,
                    'mensaje': 'No se puede soplar esa ficha'
                }

        else: # Si sacó pares
            # Si no sacó de la carcel y debía sacar de la carcel
            if not self.turno.acciones.get('sacar_de_la_carcel', False) and \
               any([0 for ficha in jugador_soplable.fichas if ficha.encarcelada]):
                if movio_dado_1 == ficha:
                    ficha_soplable = True
                    # Si había comido, tiene que devolver la ficha que se había comido
                    if comio_dado_1:
                        for jugador1 in self.jugadores:
                            if jugador1.color == comio_dado_1[0]:
                                jugador1.fichas[comio_dado_1[1]].encarcelada = False
                                jugador1.fichas[comio_dado_1[1]].posicion = esta_ficha.posicion
                                break

                if movio_dado_2 == ficha:
                    ficha_soplable = True
                    # Si había comido, tiene que devolver la ficha que se había comido
                    if comio_dado_2:
                        for jugador1 in self.jugadores:
                            if jugador1.color == comio_dado_2[0]:
                                jugador1.fichas[comio_dado_2[1]].encarcelada = False
                                jugador1.fichas[comio_dado_2[1]].posicion = esta_ficha.posicion
                                break

        # Si la ficha que están acusando podía comer
        posicion = self.turno.acciones['posiciones'][ficha]
        if (posicion + dado1) in self.fichas_en_casillas or \
            (posicion + dado2) in self.fichas_en_casillas or \
            (posicion + dado1 + dado2) in self.fichas_en_casillas:
            ficha_soplable = True

        if not ficha_soplable:
            return {
                'error': True,
                'mensaje': 'No se puede soplar esa ficha'
            }

        jugador_soplable.encarcelada = True
        jugador_soplable.posicion = jugador_soplable.salida

        # Solo se puede soplar una ficha
        self.turno.color_soplable = False

        return self.almacenar()

    def almacenar(self):
        """Almacena el estado del juego en la base de datos"""
        self.last_turn = time.time()

        # To do

        return self.dump_object()

    def encontrar_jugador(self, key: str):
        """Encuentra un jugador por su llave"""
        for jugador in self.jugadores:
            if jugador.key == key:
                return jugador

        # Si no encuentra ninguno retorna None
        return None

    def siguiente_turno(self, color: str = None):
        """Hace el setup para el siguiente turno"""
        indice_actual = [jugador.color for jugador in self.jugadores].index(self.turno.color)
        siguiente_jugador = self.jugadores[(indice_actual + 1) % len(self.jugadores)]
        self.turno.siguiente_turno(siguiente_jugador.color)
        self.turno.pares = None
        self.turno.intentos = siguiente_jugador.cantidad_lanzamientos()

    @classmethod
    def retrieve_from_database(cls, id: str):
        """Trae una instancia de un juego desde la base de datos"""

        # to do

    @classmethod
    def create(cls, posiciones: int = 4, publico: bool = False):
        if posiciones >= 4 or posiciones <= 8:
            game = cls(publico)
            game.id = str(uuid.uuid4())
            game.turno = Turno()
            game.tablero = Tablero(posiciones)
            game.almacenar()
            return game

        return {
            'error': True,
            'mensaje': f'No se puede crear un juego para {posiciones} jugadores'
        }
