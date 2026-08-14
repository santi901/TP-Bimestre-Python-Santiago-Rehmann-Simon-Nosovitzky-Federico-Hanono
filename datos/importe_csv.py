# -*- coding: utf-8 -*-
"""Ampliación del Integrador — Parte 2: importar el CSV propio a la base.

Lee `albumes.csv` (Parte 1) con pandas y carga cada fila usando las mismas
funciones de alta que ya existen en `datos.crud` (`crear_artista` y
`crear_album`), recorriendo el DataFrame con un for. No hace falta insert
masivo: alcanza con el bucle simple.

Como el CSV trae el nombre del artista (no su id, que es autogenerado),
para cada fila buscamos si ese artista ya existe en la base; si no existe,
lo damos de alta con `crear_artista` antes de crear el álbum.

Para ejecutar de forma independiente desde la raíz del proyecto:
    python -m datos.importar_csv
"""

import os

import pandas as pd

from datos.crud import crear_artista, obtener_artistas, crear_album, obtener_albumes

# Ruta por defecto: albumes.csv en la raíz del proyecto (un nivel arriba de /datos)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_CSV_DEFAULT = os.path.join(RAIZ, "albumes.csv")


def obtener_o_crear_artista(nombre, genero, pais):
    """Busca un artista por nombre; si no existe, lo da de alta y devuelve su id."""

    artistas = obtener_artistas()

    for artista in artistas:
        if artista.nombre.lower() == nombre.lower():
            return artista.id

    # No existía todavía: lo creamos con el mismo alta que ya usa la app
    crear_artista(nombre, genero, pais)

    # Lo volvemos a buscar para conseguir el id que le asignó SQLite
    artistas = obtener_artistas()
    for artista in artistas:
        if artista.nombre.lower() == nombre.lower():
            return artista.id


def importar_csv_albumes(ruta=RUTA_CSV_DEFAULT):
    """Lee el CSV de álbumes con Pandas y carga cada fila con el alta existente."""

    df = pd.read_csv(ruta)

    for indice, fila in df.iterrows():
        artista_id = obtener_o_crear_artista(fila["artista"], fila["genero"], fila["pais"])
        crear_album(fila["titulo"], int(fila["anio"]), artista_id)

    print(f"Se importaron {len(df)} álbumes desde '{ruta}'.")


if __name__ == "__main__":
    importar_csv_albumes()

    # Verificamos en la propia vista de listado que los registros se cargaron bien
    print("Álbumes actuales en la base:")
    for album in obtener_albumes():
        print(" -", album.mostrar_info())
