# Proyecto  parqués

Este repositorio corresponde al backend para un juego de parqués en línea.

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

## To do:

* Hacer tests para la interfaz web

* Poder crear un websocket para actualizar en tiempo real el juego en los clientes

* Hacer algún cliente con visualización amigable para ver si el juego realmente funciona
