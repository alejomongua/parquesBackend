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

* Cuando una ficha da la vuelta al tablero, llega a lo que llamo la _recta final_, que es un tramo de 8 casillas antes de llegar a la meta que es diferente para cada jugador. En este tramo las fichas no pueden ser comidas.

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

## Documentación del API

El API responde a peticiones tipo GET únicamente. La documentación de los parámetros y las URL se pueden acceder en https://parques-api.herokuapp.com/docs

### /juegos

Lista todos los juegos públicos abiertos, retorna un objeto json con la siguiente estructura: Cada llave corresponde al ID del juego y  contiene los siguientes parámetros:

#### Respuesta

    - *created_at*: Timestamp de creación del juego

    - _jugadores_: Cantidad de jugadores inscritos actualmente en el juego

    - _posiciones_: Posiciones disponibles en el juego

#### Ejemplo de respuesta:

    {
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

### /juegos/crear_partida

Crea un juego nuevo.

#### Parámetros

* _posiciones_: cantidad de posiciones en el tablero, este número corresponde a la cantidad máxima de jugadores en esta partida, debe estar entre 4 y 8. Si no se ingresa, el valor por defecto es 4 posiciones

* _publico_: valor booleano que indica si la partida es pública o es privada. Por defecto es _true_, es decir, que la partida se listará en el índice de partidas públicas para que cualquiera se pueda unir

#### Ejemplo de petición:

    curl -X GET "https://parques-api.herokuapp.com/juegos/crear_partida?posiciones=6&publico=true" -H  "accept: application/json"

#### Respuesta

La petición responde con el objeto que describe el estado del juego (vease objeto estado)

#### Ejemplo de respuesta

    {
        "publico": true,
        "iniciado": false,
        "finalizado": false,
        "created_at": 1604283752.3218622,
        "started_at": null,
        "last_turn": 1604283752.3218877,
        "jugadores": [],
        "fichas_en_casillas": {},
        "id": "-ML5kq0kGcV7rtLUZZdE",
        "turno": {
            "color": "Naranja",
            "dado1": null,
            "dado2": null,
            "pares": null,
            "lanzado": false,
            "valor_original_dado1": null,
            "valor_original_dado2": null,
            "intentos": 3
        }
        "tablero": {
            "colores": [
                false,
                false,
                false,
                false,
                false,
                false
            ]
        }
    }

### /juegos/{id_juego}

Trae el estado actual del juego

#### Parámetros

* *id_juego*: (argumento en la URL) String correspondiente al identificador único del juego

#### Ejemplo de petición

    curl -X GET "https://parques-api.herokuapp.com/juegos/-MKqg1mhOxA48c-fYrkl" -H  "accept: application/json"

#### Respuesta

La petición responde con el objeto que describe el estado del juego (vease objeto estado)

#### Ejemplo de respuesta

    {
        "publico": true,
        "iniciado": true,
        "finalizado": false,
        "created_at": 1604014058.3548338,
        "started_at": 1604014165.213741,
        "last_turn": 1604014338.2837567,
        "jugadores": [
            {
                "color": "Azul",
                "nickname": "Alejo",
                "retirado": false,
                "finalizado": false,
                "fichas": [
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 0
                    },
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 0
                    },
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 0
                    },
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 0
                    }
                ],
                "salida": 0
            },
            {
                "color": "Naranja",
                "nickname": "Matías",
                "retirado": false,
                "finalizado": false,
                "fichas": [
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 17
                    },
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 17
                    },
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 17
                    },
                    {
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false,
                        "posicion": 17
                    }
                ],
                "salida": 17
            }
        ],
        "fichas_en_casillas": {},
        "id": "-MKqg1mhOxA48c-fYrkl",
        "turno": {
            "color": "Naranja",
            "dado1": 6,
            "dado2": 4,
            "pares": null,
            "lanzado": false,
            "valor_original_dado1": null,
            "valor_original_dado2": null,
            "intentos": 3
        },
        "tablero": {
            "colores": [
                "Azul",
                "Naranja",
                false,
                false
            ]
        }
    }

### /juegos/{id_juego}/unirse

Se une a un juego si aún no ha iniciado y tiene puestos disponibles

#### Parámetros

* *id_juego*: (argumento en la URL) String correspondiente al identificador único del juego

* _color_: (obligatorio), color que usará el jugador en la partida y servirá como identificador único de dicho jugador durante la partida, debe ser una de las llaves en el siguiente diccionario:

```
{
    "Amarillo": "#ffe119",
    "Azul": "#4363d8",
    "Naranja": "#f58231",
    "Lavanda": "#dcbeff",
    "Marrón": "#800000",
    "Azul oscuro": "#000075",
    "Gris": "#a9a9a9",
    "Negro": "#ffffff"
}
```

* _nickname_: (obligatorio) nombre a mostrar del jugador durante la partida

#### Ejemplo de petición

    curl -X GET "https://parques-api.herokuapp.com/juegos/-ML5kq0kGcV7rtLUZZdE/unirse?color=Azul%20oscuro&nickname=Alejo" -H  "accept: application/json"

#### Respuesta

La respuesta entrega una llave que es única para cada jugador y que será necesaria al realizar cualquier jugada en nombre de dicho jugador. Esta llave sirve para asegurarse que el jugador es quien dice ser

#### Ejemplo de respuesta

    {
        "success": true,
        "key": "b696ca1e-d369-4483-a81c-78472f1eafa0"
    }

### /juegos/{id_juego}/iniciar

Inicia la partida, debe haber al menos dos jugadores

#### Parámetros

* *id_juego*: (argumento en la URL) String correspondiente al identificador único del juego

#### Ejemplo de petición

    curl -X GET "https://parques-api.herokuapp.com/juegos/-ML5kq0kGcV7rtLUZZdE/iniciar" -H  "accept: application/json"

#### Respuesta

La petición responde con el objeto que describe el estado del juego (vease objeto estado)

#### Ejemplo de respuesta

    {
        "id": "-ML5kq0kGcV7rtLUZZdE",
        "tablero": {
            "colores": [
                false,
                "Naranja",
                false,
                false,
                false,
                "Azul oscuro"
            ]
        },
        "jugadores": [
            {
                "nickname": "Matías",
                "color": "Naranja",
                "fichas": [
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    }
                ],
                "retirado": false,
                "finalizado": false,
                "salida": 17
            },
            {
                "nickname": "Alejo",
                "color": "Azul oscuro",
                "fichas": [
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    }
                ],
                "retirado": false,
                "finalizado": false,
                "salida": 85
            }
        ],
        "finalizado": false,
        "inicio": 1604283752.3218622,
        "turno": {
            "color": "Naranja",
            "dado1": null,
            "dado2": null,
            "pares": null,
            "lanzado": false,
            "valor_original_dado1": null,
            "valor_original_dado2": null,
            "intentos": 3
        },
        "ultimo_turno": 1604285299.0205038
    }

### /juegos/{id_juego}/lanzar_dado

Lanza el dado si es el turno del jugador y es momento de lanzar. Para saber de quien es el turno se debe revisar el valor `color` en el campo `turno` en el objeto del juego. Es momento de lanzar los dados cuando el campo `lanzado` es `false`

#### Parámetros

* *id_juego*: (argumento en la URL) String correspondiente al identificador único del juego

* *player_key*: (argumento en el HEADER) llave que se entregó al jugador al momento del registro. ESTE PARÁMETRO DEBE IR EN LA CABECERA COMO _player-key_

#### Ejemplo de petición

    curl -X GET "http://localhost:8000/juegos/-ML5kq0kGcV7rtLUZZdE/lanzar_dado" -H  "accept: application/json" -H  "player-key: e58b050d-2c40-40b6-b491-eccecada7df3"

#### Respuesta

La petición responde con el objeto que describe el estado del juego (vease objeto estado)

#### Ejemplo de respuesta

    {
        "id": "-ML5kq0kGcV7rtLUZZdE",
        "tablero": {
            "colores": [
                false,
                "Naranja",
                false,
                false,
                false,
                "Azul oscuro"
            ]
        },
        "jugadores": [
            {
                "nickname": "Matías",
                "color": "Naranja",
                "fichas": [
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 17,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    }
                ],
                "retirado": false,
                "finalizado": false,
                "salida": 17
            },
            {
                "nickname": "Alejo",
                "color": "Azul oscuro",
                "fichas": [
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    },
                    {
                        "posicion": 85,
                        "encarcelada": true,
                        "coronada": false,
                        "recta_final": false
                    }
                ],
                "retirado": false,
                "finalizado": false,
                "salida": 85
            }
        ],
        "finalizado": false,
        "inicio": 1604283752.3218622,
        "turno": {
            "color": "Naranja",
            "dado1": 5,
            "dado2": 5,
            "pares": 1,
            "lanzado": false,
            "valor_original_dado1": null,
            "valor_original_dado2": null,
            "intentos": 2
        },
        "ultimo_turno": 1604285546.1196947
    }

### /juegos/{id_juego}/mover_ficha

Mueve la una ficha una cantidad determinada de casillas siempre y cuando el movimiento sea legal

#### Parámetros

* *id_juego*: (argumento en la URL) String correspondiente al identificador único del juego

* *player_key*: (argumento en el HEADER) llave que se entregó al jugador al momento del registro. ESTE PARÁMETRO DEBE IR EN LA CABECERA COMO _player-key_

* _ficha_: valor entre 0 y 3 que representa la ficha que se va a mover

* _casillas_: cantidad de casillas que va a mover la ficha, puede ser el valor de uno de los dados o la suma de los dos

#### Ejemplo de petición

    curl -X GET "http://localhost:8000/juegos/-ML5kq0kGcV7rtLUZZdE/mover_ficha?ficha=0&casillas=6" -H  "accept: application/json" -H  "player-key: e58b050d-2c40-40b6-b491-eccecada7df3"

#### Respuesta

La petición responde con el objeto que describe el estado del juego (vease objeto estado)

### /juegos/{id_juego}/sacar_de_la_carcel

Si sacó pares y tiene fichas en la carcel, con esta petición saca de la carcel.

#### Parámetros

* *id_juego*: (argumento en la URL) String correspondiente al identificador único del juego

* *player_key*: (argumento en el HEADER) llave que se entregó al jugador al momento del registro. ESTE PARÁMETRO DEBE IR EN LA CABECERA COMO _player-key_

#### Ejemplo de petición

    curl -X GET "http://localhost:8000/juegos/-ML5kq0kGcV7rtLUZZdE/sacar_de_la_carcel" -H  "accept: application/json" -H  "player-key: b696ca1e-d369-4483-a81c-78472f1eafa0"

#### Respuesta

La petición responde con el objeto que describe el estado del juego (vease objeto estado)

### /juegos/{id_juego}/soplar

Declara que un movimiento del jugador interior es ilegal y debe enviarse una ficha a la carcel.

#### Parámetros

* *id_juego*: (argumento en la URL) String correspondiente al identificador único del juego

* *player_key*: (argumento en el HEADER) llave que se entregó al jugador al momento del registro. ESTE PARÁMETRO DEBE IR EN LA CABECERA COMO _player-key_

* _ficha_: valor entre 0 y 3 que representa la ficha que se va a mover

#### Ejemplo de petición

    curl -X GET "http://localhost:8000/juegos/-ML5kq0kGcV7rtLUZZdE/soplar?ficha=2" -H  "accept: application/json" -H  "player-key: b696ca1e-d369-4483-a81c-78472f1eafa0"

#### Respuesta

La petición responde con el objeto que describe el estado del juego (vease objeto estado)

## Objeto estado del juego

La mayoría de las peticiones responden con un objeto que repersenta el estado del juego para poderlo renderizar en un tablero, dicho objeto tiene los siguientes atributos

### id

* _Tipo_: String

* _Descripción_: Es el identificador único del juego

* _Ejemplo_: "-ML5kq0kGcV7rtLUZZdE"

### tablero

* _Tipo_: Objeto

* _Descripción_: Objeto que representa el tablero del juego.

* _Componentes_:

    - _Colores_: (Array de strings) Corresponde a un array que representa las diferentes posiciones del tablero. Si el valor es null es porque en esa posición no hay ningún jugador

* _Ejemplo_:

    {
        "colores": [
            false,
            "Naranja",
            false,
            false,
            false,
            "Azul oscuro"
        ]
    }

### Jugador

* _Tipo_: Objeto

* _Descripción_: Objeto que representa el estado de un jugador, en el juego hay un arreglo de objetos tipo jugador

* _Componentes_:

    - _color_: (String) Color del jugador

    - _nickname_: (String) Nombre o apodo del jugador durante la partida

    * _retirado_: (Boolean) Indica si el jugador se rindió o retiró de la partida

    * _finalizado_: (Boolean) Indica si el jugador la coronó todas sus fichas

    * _fichas_: (Array) Arreglo de objetos tipo ficha

    * _salida_: (Integer) Casilla de salida, en esta casilla iniciarán las fichas al salir de la carcel

* _Ejemplo_:

    {
        "color": "Naranja",
        "nickname": "Matías",
        "retirado": false,
        "finalizado": false,
        "fichas": [
            {
                "encarcelada": true,
                "coronada": false,
                "recta_final": false,
                "posicion": 17
            },
            {
                "encarcelada": true,
                "coronada": false,
                "recta_final": false,
                "posicion": 17
            },
            {
                "encarcelada": true,
                "coronada": false,
                "recta_final": false,
                "posicion": 17
            },
            {
                "encarcelada": true,
                "coronada": false,
                "recta_final": false,
                "posicion": 17
            }
        ],
        "salida": 17
    }

### Ficha

* _Tipo_: Objeto

* _Descripción_: Estado de una ficha determinada

* _Componentes_:

    - _encarcelada_: (Boolean) Indica si la ficha está en la carcel

    - _coronada_: (Boolean) Indica si la ficha finalizó ya la partida

    - *recta_final*: (Boolean) Indica si la ficha ya llegó al tramo final. Cuando una ficha llega a la recta final su posición pasa a 0 y cuando llega a 8 la ficha es coronada

    - *posicion*: (Integer) Posición de la ficha en el tablero.

* _Ejemplo_:

    {
        "encarcelada": true,
        "coronada": false,
        "recta_final": false,
        "posicion": 17
    }

### finalizado

* _Ejemplo_: false,

### inicio

* _Ejemplo_: 1604283752.3218622,

### turno

* _Tipo_: Objeto

* _Descripción_: Estado actual del turno en el juego

* _Componentes_:

    - _color_: (String) Indica de quien es el turno actual

    - _dado1_: (Integer) Indica el valor sacado en el dado 1 que está pendiente por mover, cuando se mueve se vuelve 0

    - _dado2_: (Integer) Indica el valor sacado en el dado 2 que está pendiente por mover, cuando se mueve se vuelve 0

    - _pares_: (Integer) Indica la cantidad de pares seguidos en este turno. Si sacó pares pero los usó para sacar de la carcel es 0, si no sacó pares es null

    - _lanzado_: (Boolean) Indica si ya se lanzaron los dados, si es _false_ es momento de lanzar los dados

    - _intentos_: Cantidad de intentos restantes en caso de que tenga todas las fichas en la carcel

    - *valor_original_dado1*: (Integer) Indica el valor sacado en el dado 1 durante el último lanzamiento, sirve para poder mostrarlo en el frontend ya que el valor dado1 se vuelve 0 al mover

    - *valor_original_dado2*: (Integer) Indica el valor sacado en el dado 2 durante el último lanzamiento, sirve para poder mostrarlo en el frontend ya que el valor dado2 se vuelve 0 al mover

* _Ejemplo_:

    {
        "color": "Naranja",
        "dado1": 5,
        "dado2": 5,
        "pares": 1,
        "lanzado": false,
        "valor_original_dado1": 5,
        "valor_original_dado2": 5,
        "intentos": 2
    }

### ultimo_turno

_Ejemplo_: 1604285546.1196947

## Mensajes de error

Cuando una petición no es exitosa por alguna razón contemplada, el codigo de error será 400 y la respuesta tendrá la siguiente estructura:

    {
        "error": true,
        "mensaje": "Espere su turno"
    }

Donde el mensaje será la causa de la falla en la petición y deberá mostrarse al usuario final

## Acerca de este proyecto

El stack de este proyecto es el siguiente:

* Este proyecto está principalmente programado en python, compatible con versión >= 3.6

* unittest para los test automáticos de la aplicación

* Realtime Database de Firebase para la persistencia

* FastApi para la interfaz web

## Instalación

Para instalar este proyecto se recomienda usar un virtual environment, se necesita python3.6 o superior

    pip install -r requirements.txt

Se necesita ubicar el archivo secretKey.json en la raiz del proyecto para poder conectarse con Firebase https://www.appypie.com/faqs/how-to-obtain-your-firebase-data-url-and-secret-key

## Testing

Para ejecutar los tests, ejecute el siguiente comando en la raiz del proyecto

    python -m pytest

## Correr el webserver

El servidor se ejecuta con uvicorn:

    uvicorn server.main:app --host=0.0.0.0 --port=${PORT:-5000}

## Demo

Este proyecto está ejecutándose en https://parques-api.herokuapp.com, la documentación del API está en https://parques-api.herokuapp.com/docs
