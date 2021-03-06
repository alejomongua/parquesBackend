import random

class Turno():
    """
    Lleva el control del estado del turno actual

    ...

    Attributes
    ----------
    color : string
            Jugador que tomará el primer turno
    dado1 : int
            Valor lanzado en el primer dado, es None si
            no se ha lanzado o 0 si ya se movió
    dado2 : int
            Valor lanzado en el segundo dado, es None si
            no se ha lanzado o 0 si ya se movió o si se
            lanza un solo dado
    pares : int
            Indica cuantos pares consecutivos ha sacado,
            si no saca pares es None, si sacó pares pero
            salió de la cárcel es 0

    Methods
    -------
    public_state()
            Retorna el estado actual del objeto

    """

    def __init__(self):
        """
        Constructor: Se puede pasar el estado para no
        iniciar con los valores por defecto cuando se
        traiga desde la base de datos
        """
        self.color = None
        self.dado1 = None
        self.dado2 = None
        self.pares = None
        self.lanzado = False
        self.locked = [False, False, False, False]
        self.color_soplable = None
        self.intentos = 3
        # En la variable acciones se almacenan los movimientos realizados en el último turno
        self.acciones = {}

    def public_state(self):
        """Retorna el estado actual del objeto"""

        valor_original_dado1 = None
        valor_original_dado2 = None
        if isinstance(self.acciones, dict):
            valor_original_dado1 = self.acciones.get('dado1', None)
            valor_original_dado2 = self.acciones.get('dado2', None)

        return {
            'color': self.color,
            'dado1': self.dado1,
            'dado2': self.dado2,
            'pares': self.pares,
            'lanzado': self.lanzado,
            'valor_original_dado1': valor_original_dado1,
            'valor_original_dado2': valor_original_dado2,
            'intentos': self.intentos
        }

    def serializar(self):
        otros_atributos = {
            'locked': self.locked,
            'color_soplable': self.color_soplable,
        }

        return { **self.public_state(), **otros_atributos }

    def lanzar(self, dados: int = 2):
        """Lanza los dados"""
        self.color_soplable = False
        self.lanzado = True
        self.intentos -= 1

        if dados == 2:
            self.dado2 = random.randint(1, 6)
        else:
            self.dado2 = 0

        self.dado1 = random.randint(1, 6)

        self.acciones = {
            'dado1': self.dado1,
            'dado2': self.dado2,
        }

        if self.dado1 == self.dado2:
            if self.pares is None:
                self.pares = 1
            else:
                self.pares = self.pares + 1
        else:
            self.pares = None

    def siguiente_turno(self, color: str = None):
        self.color_soplable = self.color
        self.lanzado = False
        self.locked = [False, False, False, False]
        if color is not None:
            self.color = color

    @classmethod
    def deserializar(cls, estado: dict):
        """Reconstruye el estado del objeto desde un diccionario"""
        turno = cls()
        turno.color = estado.get('color')
        turno.dado1 = estado.get('dado1')
        turno.dado2 = estado.get('dado2')
        turno.pares = estado.get('pares')
        turno.lanzado = estado.get('lanzado')
        turno.acciones = estado.get('acciones')
        turno.intentos = estado.get('intentos')
        turno.locked = estado.get('locked')
        turno.color_soplable = estado.get('color_soplable')
        return turno
