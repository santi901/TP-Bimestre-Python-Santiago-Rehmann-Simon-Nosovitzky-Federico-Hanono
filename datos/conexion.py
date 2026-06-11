# -*- coding: utf-8 -*-
"""Conexión centralizada a la base de datos SQLite.

Define una única ruta a la base para que todos los módulos (creación y CRUD)
trabajen siempre sobre el mismo archivo, sin importar desde dónde se ejecute.
"""

import os
import sqlite3

# Carpeta raíz del proyecto (un nivel por encima de /datos)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta absoluta al archivo de la base de datos
NOMBRE_DB = os.path.join(RAIZ, "live_music.db")


def conectar():
    """Devuelve una conexión nueva a la base de datos."""
    return sqlite3.connect(NOMBRE_DB)
