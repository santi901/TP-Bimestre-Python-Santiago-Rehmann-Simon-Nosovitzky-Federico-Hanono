# -*- coding: utf-8 -*-
"""Capa de acceso a datos (CRUD) de Live Music Pro.

Toda la lógica SQL vive acá. La interfaz (app.py) nunca habla con la base
directamente: siempre lo hace a través de estas funciones.

Las funciones de lectura recuperan las filas y, mediante bucles, las
transforman en objetos de las clases del paquete `modelos`.
"""

from datos.conexion import conectar
from modelos import Artista, Album, Concierto


# ---------------------------------------------------------------------------
# ARTISTAS
# ---------------------------------------------------------------------------

def crear_artista(nombre, genero, pais):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO artistas (nombre, genero, pais) VALUES (?, ?, ?)",
        (nombre, genero, pais)
    )
    conexion.commit()
    conexion.close()


def obtener_artistas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, genero, pais FROM artistas")
    datos = cursor.fetchall()
    conexion.close()

    # Bucle que transforma cada fila en un objeto Artista
    artistas = []
    for fila in datos:
        artistas.append(Artista(*fila))
    return artistas


def actualizar_artista(id, nombre, genero, pais):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE artistas SET nombre=?, genero=?, pais=? WHERE id=?",
        (nombre, genero, pais, id)
    )
    conexion.commit()
    conexion.close()


def borrar_artista(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM artistas WHERE id=?", (id,))
    conexion.commit()
    conexion.close()


# ---------------------------------------------------------------------------
# ÁLBUMES
# ---------------------------------------------------------------------------

def crear_album(titulo, anio, artista_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO albumes (titulo, anio, artista_id) VALUES (?, ?, ?)",
        (titulo, anio, artista_id)
    )
    conexion.commit()
    conexion.close()


def obtener_albumes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, anio, artista_id FROM albumes")
    datos = cursor.fetchall()
    conexion.close()

    albumes = []
    for fila in datos:
        albumes.append(Album(*fila))
    return albumes


def obtener_albumes_con_artista():
    """Devuelve una lista de diccionarios con el álbum y el nombre del artista."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT albumes.id,
               albumes.titulo,
               albumes.anio,
               artistas.nombre
        FROM albumes
        JOIN artistas ON albumes.artista_id = artistas.id
    """)
    datos = cursor.fetchall()
    conexion.close()

    albumes = []
    for fila in datos:
        albumes.append({
            "id": fila[0],
            "titulo": fila[1],
            "anio": fila[2],
            "artista": fila[3]
        })
    return albumes


def actualizar_album(id, titulo, anio, artista_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE albumes SET titulo=?, anio=?, artista_id=? WHERE id=?",
        (titulo, anio, artista_id, id)
    )
    conexion.commit()
    conexion.close()


def borrar_album(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM albumes WHERE id=?", (id,))
    conexion.commit()
    conexion.close()


# ---------------------------------------------------------------------------
# CONCIERTOS
# ---------------------------------------------------------------------------

def crear_concierto(ciudad, fecha, artista_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO conciertos (ciudad, fecha, artista_id) VALUES (?, ?, ?)",
        (ciudad, fecha, artista_id)
    )
    conexion.commit()
    conexion.close()


def obtener_conciertos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, ciudad, fecha, artista_id FROM conciertos")
    datos = cursor.fetchall()
    conexion.close()

    conciertos = []
    for fila in datos:
        conciertos.append(Concierto(*fila))
    return conciertos


def obtener_conciertos_con_artista():
    """Devuelve una lista de diccionarios con el concierto y el nombre del artista."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT conciertos.id,
               conciertos.ciudad,
               conciertos.fecha,
               artistas.nombre
        FROM conciertos
        JOIN artistas ON conciertos.artista_id = artistas.id
    """)
    datos = cursor.fetchall()
    conexion.close()

    conciertos = []
    for fila in datos:
        conciertos.append({
            "id": fila[0],
            "ciudad": fila[1],
            "fecha": fila[2],
            "artista": fila[3]
        })
    return conciertos


def actualizar_concierto(id, ciudad, fecha, artista_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE conciertos SET ciudad=?, fecha=?, artista_id=? WHERE id=?",
        (ciudad, fecha, artista_id, id)
    )
    conexion.commit()
    conexion.close()


def borrar_concierto(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM conciertos WHERE id=?", (id,))
    conexion.commit()
    conexion.close()
