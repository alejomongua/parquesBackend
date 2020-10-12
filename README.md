# Proyecto  parqués

Este repositorio corresponde al backend para un juego de parqués en línea.

Más información acerca del parqués en https://es.wikipedia.org/wiki/Parqu%C3%A9s

## Objetos

El juego se organiza en objetos que describen su estado, los objetos en una partida son los siguientes:

### Tablero

_**Atributos**_

**colores**: _array de strings_ -> Colores en el tablero en el orden de sus turnos, si hay un jugador faltante el color sera null

_**Métodos**_

**cantidad_de_casillas**: _Entradas: ninguna, Salidas: integer_ -> Calcula la cantidad de casillas dependiendo del número de colores

**seguro**: _Entradas: integer, Salidas: boolean_ -> Determina si una casilla determinada corresponde a un seguro

**salida**: _Entradas: integer, Salidas: boolean_ -> Determina si una casilla determinada corresponde a una casilla de salida

### Jugador

_**Atributos**_

**nickname**: _string_ -> Nombre del jugador dentro de una partida

**color**: _string_ -> Color del jugador, también determina el orden de su turno según el array de colores en el tablero

**fichas**: _array de fichas_ -> Array de 4 objetos de tipo ficha (ver más adelante)

**retirado**: _boolean_ -> Indica si el jugador se retiró del juego

**finalizado**: _boolean_ -> Indica si ya coronó todas sus fichas

**salida**: _integer_ -> Indica la casilla inicial en el tablero para dicho jugador

_**Métodos**_

**cantidad_dados**: _Entradas: ninguna, Salidas: integer_ -> Uno si le queda una sola ficha a menos de seis pasos de ganar, dos en otro caso

**cantidad_lanzamientos**: _Entradas: Ninguna, Salidas: integer_ -> tres si tiene todas sus fichas en la carcel, uno en otro caso

### Ficha

**posicion**: _integer_ -> Posición de la ficha en el tablero

**encarcelada**: _boolean_ -> Indica si la ficha está en la carcel

**coronada**: _boolean_ -> Indica si la ficha ya llegó a la meta

**recta_final**: _boolean_ -> Indica si la fecha está en el último tramo de 8 casillas

### Turno

**color**: _srting_ -> indica de quién es el turno

**dado1**: _integer_ -> Indica la cantidad obtenida en el primer dado, si no ha lanzado o ya movió es null

**dado2**: _integer_ -> Indica la cantidad obtenida en el segundo dado, si no ha lanzado o ya movió o solo va a lanzar un dado es null

**lanzado**: _boolean_ -> Indica si ya se lanzaron los dados

**pares**: _integer_ -> Indica cuantos pares consecutivos ha sacado, si no saca pares es null, si sacó pares pero salió de la cárcel es 0

### Juego

**id**: _string_ -> Identificador único de cada juego

**tablero**: _Tablero_ -> Representa el tablero del juego

**jugadores**: _Array de jugadores_ -> Jugadores en orden de sus turnos

**finalizado**: _boolean_ -> Indica si el juego ya finalizó

## Métodos:

### Creación de un juego:

#### newGame:

Crea un objeto de tipo juego, retorna el ID del juego recién creado

#### getGame (idGame)

Retorna el estado del juego

#### joinGame (idGame, nickname)

Registra un jugador dentro de un juego, retorna una llave única para cada jugador y su color correspondiente

#### startGame (idGame)

Inicia el juego con los jugadores que tenga registrados en el momento

### Jugar

#### Lanzar(playerKey)

Si es el turno del jugador, lanza sus dados, retorna el nuevo estado del juego

#### Mover(playerKey, ficha, casilla)

Mueve la ficha a la casilla indicada por el jugador

#### SacarDeLaCarcel(playerKey, cantidad_fichas)

Saca *cantidad_fichas* de la carcel

#### Soplar(playerKey)

Indíca que el último jugador cometió una acción inválida, si es procedente, el jugador que cometió la falta es penalizado, si no, el jugador que acusó en falso es penalizado

