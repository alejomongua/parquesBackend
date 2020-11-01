# Proyecto  parqués

Este repositorio corresponde al backend para un juego de parqués en línea.

## ¿Qué es el parqués?

Parqués es un juego de mesa popular en Colombia, es una variación del parchís. Tiene las siguientes características/reglas:

* Se puede jugar de a dos o más jugadores, en esta versión se soportan hasta 8 jugadores en una partida.

* El tiempo promedio de una partida depende de la cantidad de jugadores.

* Cada jugador inicia con cuatro fichas, todas ellas en la "carcel".

* Cuando una ficha está en la carcel no puede ser movida.

* En su turno el jugador lanza dos dados de seis caras.

* Cuando un jugador tiene todas las fichas en la carcel (por ejemplo, al principio de la partida), puede lanzar hasta tres veces.

* Si un jugador saca pares debe sacar sus fichas de la carcel so pena de ser soplado.

* Si saca un par de uno o un par de seis puede sacar todas las fichas que tenga en la carcel.

* Si saca un par diferente de uno o seis puede sacar hasta dos fichas de la carcel.

* Si un jugador solo tiene una ficha en la carcel y saca pares, deberá mover otra ficha la cantidad indicada por uno de los dados

* Si un jugador tiene una única ficha y esta ficha está en la carcel y saca pares, la ficha saldrá en la casilla de salida más la cantidad indicada por uno de los dados con una excepción: Si hay una ficha adversaria en la salida, la ficha adveraria irá a la carcel y la ficha que acaba de salir de la carcel se quedará en la salida

* El jugador deberá mover sus fichas la cantidad indicada por los dados de la siguiente manera:

    - Mover la cantidad indicada con cada dado con una ficha diferente ó

    - Mover con una sola ficha la suma de ambos dados

* Si un jugador tiene una sola ficha y con el valor de uno solo de los dados puede comerse una ficha de un adversario, deberá mover solo esa cantidad y perder la cantidad del otro dado so pena de ser soplado

* Cuando se sacan pares el jugador obtiene otro lanzamiento

* Si un jugador obtiene tres pares seguidos en una misma jugada puede coronar una ficha a su elección, en cuyo caso no moverá ninguna ficha y ya no podrá volver a lanzar, será el turno del siguiente jugador

* Los lanzamientos con pares usados para sacar de la carcel no cuentan para la coronación, es decir, si un jugador saca tres pares seguidos, pero en el primer lanzamiento sacó fichas de la carcel, tendrá que lanzar nuevamente. Si saca pares nuevamente puede coronar una ficha

* Cuando una ficha llega a la meta, la ficha será coronada y saldrá del juego, para ello debe llegar justo a la casilla de llegada, no se puede pasar

* Cuando un jugador corona todas sus fichas, la partida finaliza y dicho jugador es el ganador

## Definiciones

* **Carcel:** Posición inicial de las fichas, las fichas en la carcel no pueden ser movidas

* **Pares:** Lanzamiento en el que en los dos dados se obtiene la misma cantidad _(sacar pares)_

* **Soplar:** Es la acción del juego en la que un jugador indica que algún adversario cometió un movimiento ilegal (ver la próxima sección). La ficha soplada va a la carcel

* **Coronar:** Se le llama _coronar una ficha_ al momento en el que una ficha llega a la meta o por sacar tres pares seguidos

* **Seguro:** Casillas en las cuales fichas de varios colores pueden convivir sin ser enviadas a la carcel.

* **Salida:** Posición inicial de las fichas de determinado color después de salir de la carcel. Puede funcionar como una casilla de seguro (casi)

* **Comer:** Es la acción en la cual un jugador envía una ficha de otro jugador a la carcel, en alguna de las siguentes condiciones:

    - Cuando se mueve hasta la ficha de la ficha _víctima_

    - Cuando la ficha _víctima_ se encuentra en la salida del jugador _victimario_ y este último sale de la carcel

_Nota: los términos víctima y victimario no se usan hábitualmente en el parqués, yo los introduje aquí para hacer más clara la explicación_

## Condiciones para soplar

Para que se pueda soplar a un jugador que acabó de hacer su jugada, este último debe haber realizado alguno de los dos movimiento inválido indicados a continuación:

* El jugador tenía alguna ficha en la carcel, sacó pares y en vez de sacar la ficha de la carcel mueve otra ficha. La ficha que movió puede ser soplada. Si movió más de una ficha cualquiera de las dos puede ser soplada.

* El jugador podía comerse una ficha de un adversario y en su lugar movió una ficha diferente, en cuyo caso la ficha que pudo comer y no lo hizo puede ser soplada.

Las dos reglas citadas anteriormente se listaron en orden de prioridad. Si un jugador puede sacar de la carcel pero en su lugar se come una ficha de un adversario podrá ser soplado, el movimiento será inválidado (la ficha comida vuelve al juego)

En esta implementación se tiene lo siguiente:

* Solo podrá soplarse una ficha por turno así haya más de una ficha potencialmente _soplable_

* El momento en el que se puede soplar es únicamente entre el momento en que se termina el turno de jugador y el momento en que el siguiente jugador lanza los dados, esto debe tenerse en cuenta en el frontend para dar un periodo de tiempo para poder soplar las fichas.

Más información acerca del parqués en https://es.wikipedia.org/wiki/Parqu%C3%A9s

## Acerca de este proyecto

El stack de este proyecto es el siguiente:

* Este proyecto está principalmente programado en python, compatible con versión >= 3.6

* unittest para los test automáticos de la aplicación

* Realtime Database de Firebase para la persistencia

* FastApi para la interfaz web

## Instalación

Para instalar este proyecto se recomienda usar un virtual environment, se necesita python3.6 o superior

    # Instalar los requerimientos
    pip install < requirements.txt

[Se necesita ubicar el archivo secretKey.json en la raiz del proyecto para poder conectarse con Firebase] (https://www.appypie.com/faqs/how-to-obtain-your-firebase-data-url-and-secret-key)

## Testing

Para ejecutar los tests, ejecute el siguiente comando en la raiz del proyecto

    python -m tests.test_game

## Correr el webserver

El servidor se ejecuta con uvicorn:

    uvicorn server.main:app --reload

## Demo

Este proyecto está ejecutándose en https://parques-api.herokuapp.com, la documentación del API está en https://parques-api.herokuapp.com/docs
