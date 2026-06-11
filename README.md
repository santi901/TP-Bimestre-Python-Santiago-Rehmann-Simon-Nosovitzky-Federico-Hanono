# 🎵 Live Music Pro

Sistema de gestión para la productora musical **ORT Sounds**: permite administrar
artistas, los álbumes que lanzan y la agenda de conciertos, con persistencia en
SQLite e interfaz web en Streamlit.

## Estructura del proyecto

```
Proyecto Python/
├── app.py                  # Interfaz gráfica (Streamlit) — Objetivo 3
├── requirements.txt        # Dependencias
├── README.md
│
├── modelos/                # Clases POO (entidades) — Objetivo 1
│   ├── __init__.py
│   ├── artista.py
│   ├── album.py
│   └── concierto.py
│
└── datos/                  # Capa de persistencia SQLite — Objetivo 2
    ├── __init__.py
    ├── conexion.py         # Conexión centralizada a la base
    ├── crear_base.py       # Creación de tablas + datos de ejemplo
    └── crud.py             # CRUD completo (Crear, Leer, Actualizar, Borrar)
```

La lógica de SQL vive únicamente en `datos/`; la interfaz nunca habla con la
base directamente (Objetivo 4: código modularizado).

## Cómo ejecutarlo

1. Instalar dependencias:

   ```
   pip install -r requirements.txt
   ```

2. (Opcional) Crear la base con datos de ejemplo. La app también la crea sola
   al iniciar, pero se puede correr a mano:

   ```
   python -m datos.crear_base
   ```

3. Levantar la aplicación:

   ```
   streamlit run app.py
   ```

## Cómo cumple la consigna

- **Arquitectura de Datos (POO):** clases `Artista`, `Album` y `Concierto`, cada
  una con `__init__` y al menos dos métodos de instancia
  (`mostrar_info`, `es_internacional`, `calcular_antiguedad`, etc.).
- **Persistencia con SQLite:** capa de datos con conexión propia y CRUD completo
  por ID para las tres tablas principales.
- **Interfaz Streamlit:** menú de navegación, formularios de alta, listados con
  filtros (por género, por artista, por ciudad).
- **Lógica de programación:** validaciones con condicionales (campos vacíos,
  años inválidos), bucles que transforman filas en objetos, y funciones que
  separan la lógica SQL de la interfaz.
```
