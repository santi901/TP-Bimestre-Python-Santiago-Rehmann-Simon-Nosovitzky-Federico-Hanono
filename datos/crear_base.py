# -*- coding: utf-8 -*-
"""Script de creación de la base de datos de Live Music Pro.

Sigue el mismo estilo del script provisto por la cátedra: una función dedicada
que crea las tablas con CREATE TABLE IF NOT EXISTS, carga datos de ejemplo
iniciales y se ejecuta desde el bloque if __name__ == "__main__".

Para crear la base, ejecutar desde la raíz del proyecto:
    python -m datos.crear_base
"""

from datos.conexion import conectar, NOMBRE_DB


def crear_base_datos():
    # Conexión (si no existe, se crea el archivo)
    conexion = conectar()
    cursor = conexion.cursor()

    # 1. Tabla de ARTISTAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            genero TEXT NOT NULL,
            pais TEXT NOT NULL
        )
    ''')

    # 2. Tabla de ÁLBUMES (relacionada con Artistas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS albumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            anio INTEGER NOT NULL,
            artista_id INTEGER,
            FOREIGN KEY (artista_id) REFERENCES artistas (id)
        )
    ''')

    # 3. Tabla de CONCIERTOS (relacionada con Artistas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conciertos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciudad TEXT NOT NULL,
            fecha TEXT NOT NULL,
            artista_id INTEGER,
            FOREIGN KEY (artista_id) REFERENCES artistas (id)
        )
    ''')

    # Solo cargamos datos de ejemplo si la tabla de artistas está vacía,
    # para no duplicar los registros cada vez que se ejecuta el script.
    cursor.execute('SELECT COUNT(*) FROM artistas')
    hay_datos = cursor.fetchone()[0]

    if hay_datos == 0:

        # Datos de ejemplo iniciales: ARTISTAS
        artistas_iniciales = [
            ('Soda Stereo', 'Rock', 'Argentina'),
            ('Dua Lipa', 'Pop', 'Reino Unido'),
            ('Bad Bunny', 'Reggaeton', 'Puerto Rico')
        ]
        cursor.executemany(
            'INSERT INTO artistas (nombre, genero, pais) VALUES (?, ?, ?)',
            artistas_iniciales
        )

        # Datos de ejemplo iniciales: ÁLBUMES (vinculados a los artistas 1, 2 y 3)
        albumes_iniciales = [
            ('Canción Animal', 1990, 1),
            ('Future Nostalgia', 2020, 2),
            ('Un Verano Sin Ti', 2022, 3)
        ]
        cursor.executemany(
            'INSERT INTO albumes (titulo, anio, artista_id) VALUES (?, ?, ?)',
            albumes_iniciales
        )

        # Datos de ejemplo iniciales: CONCIERTOS
        conciertos_iniciales = [
            ('Buenos Aires', '2026-09-15', 1),
            ('Córdoba', '2026-10-02', 2),
            ('Rosario', '2026-11-20', 3)
        ]
        cursor.executemany(
            'INSERT INTO conciertos (ciudad, fecha, artista_id) VALUES (?, ?, ?)',
            conciertos_iniciales
        )

    conexion.commit()
    conexion.close()
    print(f"Base de datos '{NOMBRE_DB}' creada exitosamente.")


if __name__ == "__main__":
    crear_base_datos()
