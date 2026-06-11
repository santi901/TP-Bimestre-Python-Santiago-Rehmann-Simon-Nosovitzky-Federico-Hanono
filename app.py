# -*- coding: utf-8 -*-
"""Live Music Pro - Interfaz gráfica (Streamlit).

Esta capa SOLO se ocupa de la presentación y la validación de datos de entrada.
Toda la persistencia se delega en el paquete `datos` (CRUD), y las entidades se
representan con las clases del paquete `modelos`.

Para ejecutar:
    streamlit run app.py
"""

import streamlit as st

from datos.crear_base import crear_base_datos
from datos.crud import (
    crear_artista, obtener_artistas, actualizar_artista, borrar_artista,
    crear_album, obtener_albumes, obtener_albumes_con_artista,
    actualizar_album, borrar_album,
    crear_concierto, obtener_conciertos, obtener_conciertos_con_artista,
    actualizar_concierto, borrar_concierto,
)

# Nos aseguramos de que la base y las tablas existan al iniciar la app.
crear_base_datos()


st.title("Live Music Pro")

menu = st.sidebar.selectbox(
    "Menú de navegación",
    ["Artistas", "Álbumes", "Conciertos"]
)


# ---------------------------------------------------------------------------
# GESTIÓN DE ARTISTAS
# ---------------------------------------------------------------------------
if menu == "Artistas":

    st.header("Gestión de Artistas")

    # --- Formulario de alta ---
    st.subheader("Agregar artista")
    nombre = st.text_input("Nombre")
    genero = st.text_input("Género")
    pais = st.text_input("País")

    if st.button("Agregar artista"):
        # Validación: no se permiten campos vacíos
        if nombre.strip() == "" or genero.strip() == "" or pais.strip() == "":
            st.error("No puede haber campos vacíos.")
        else:
            crear_artista(nombre.strip(), genero.strip(), pais.strip())
            st.success("Artista agregado correctamente.")

    # --- Listado con filtro ---
    st.subheader("Lista de artistas")
    artistas = obtener_artistas()

    if len(artistas) == 0:
        st.info("Todavía no hay artistas cargados.")
    else:
        # Filtro dinámico por género
        generos = sorted({a.genero for a in artistas})
        filtro_genero = st.selectbox("Filtrar por género", ["Todos"] + generos)

        for artista in artistas:
            if filtro_genero == "Todos" or artista.genero == filtro_genero:
                etiqueta = " 🌎" if artista.es_internacional() else ""
                st.write(f"#{artista.id} - {artista.mostrar_info()}{etiqueta}")

        # --- Modificación segura por ID ---
        st.subheader("Editar artista")
        opciones_edit = {f"#{a.id} - {a.nombre}": a for a in artistas}
        sel_edit = st.selectbox("Seleccionar artista a editar", list(opciones_edit.keys()))
        artista_sel = opciones_edit[sel_edit]

        nuevo_nombre = st.text_input("Nuevo nombre", value=artista_sel.nombre, key="edit_art_nombre")
        nuevo_genero = st.text_input("Nuevo género", value=artista_sel.genero, key="edit_art_genero")
        nuevo_pais = st.text_input("Nuevo país", value=artista_sel.pais, key="edit_art_pais")

        if st.button("Guardar cambios del artista"):
            if nuevo_nombre.strip() == "" or nuevo_genero.strip() == "" or nuevo_pais.strip() == "":
                st.error("No puede haber campos vacíos.")
            else:
                actualizar_artista(
                    artista_sel.id,
                    nuevo_nombre.strip(),
                    nuevo_genero.strip(),
                    nuevo_pais.strip()
                )
                st.success("Artista actualizado. Actualizá la página para ver los cambios.")

        # --- Baja segura por ID ---
        st.subheader("Eliminar artista")
        opciones = {f"#{a.id} - {a.nombre}": a.id for a in artistas}
        seleccion = st.selectbox("Seleccionar artista a eliminar", list(opciones.keys()))
        if st.button("Eliminar artista"):
            borrar_artista(opciones[seleccion])
            st.success("Artista eliminado. Actualizá la página para ver los cambios.")


# ---------------------------------------------------------------------------
# GESTIÓN DE ÁLBUMES
# ---------------------------------------------------------------------------
elif menu == "Álbumes":

    st.header("Gestión de Álbumes")

    artistas = obtener_artistas()

    if len(artistas) == 0:
        st.warning("Primero tenés que cargar artistas.")
    else:
        # --- Formulario de alta ---
        st.subheader("Agregar álbum")
        titulo = st.text_input("Título del álbum")
        anio = st.number_input(
            "Año de lanzamiento",
            min_value=1900,
            max_value=2100,
            value=2024,
            step=1
        )

        # Diccionario {nombre: id} para elegir el artista
        opciones_artistas = {a.nombre: a.id for a in artistas}
        artista_nombre = st.selectbox("Artista", list(opciones_artistas.keys()))

        if st.button("Agregar álbum"):
            # Validaciones
            if titulo.strip() == "":
                st.error("El título no puede estar vacío.")
            elif anio <= 0:
                st.error("El año de lanzamiento no puede ser negativo o cero.")
            else:
                crear_album(titulo.strip(), int(anio), opciones_artistas[artista_nombre])
                st.success("Álbum agregado correctamente.")

        # --- Listado con filtro ---
        st.subheader("Lista de álbumes")
        albumes = obtener_albumes_con_artista()

        if len(albumes) == 0:
            st.info("Todavía no hay álbumes cargados.")
        else:
            # Filtro dinámico por artista
            nombres = sorted({al["artista"] for al in albumes})
            filtro_artista = st.selectbox("Filtrar por artista", ["Todos"] + nombres)

            for al in albumes:
                if filtro_artista == "Todos" or al["artista"] == filtro_artista:
                    st.write(f'#{al["id"]} - {al["titulo"]} ({al["anio"]}) - {al["artista"]}')

            # --- Modificación segura por ID ---
            st.subheader("Editar álbum")
            albumes_obj = obtener_albumes()
            opciones_edit = {f"#{al.id} - {al.titulo}": al for al in albumes_obj}
            sel_edit = st.selectbox("Seleccionar álbum a editar", list(opciones_edit.keys()))
            album_sel = opciones_edit[sel_edit]

            nuevo_titulo = st.text_input("Nuevo título", value=album_sel.titulo, key="edit_alb_titulo")
            nuevo_anio = st.number_input(
                "Nuevo año",
                min_value=1900,
                max_value=2100,
                value=int(album_sel.anio),
                step=1,
                key="edit_alb_anio"
            )

            # Artista actual preseleccionado
            nombres_artistas = list(opciones_artistas.keys())
            id_a_nombre = {v: k for k, v in opciones_artistas.items()}
            indice_actual = 0
            if album_sel.artista_id in id_a_nombre:
                indice_actual = nombres_artistas.index(id_a_nombre[album_sel.artista_id])
            nuevo_artista_nombre = st.selectbox(
                "Nuevo artista", nombres_artistas, index=indice_actual, key="edit_alb_artista"
            )

            if st.button("Guardar cambios del álbum"):
                if nuevo_titulo.strip() == "":
                    st.error("El título no puede estar vacío.")
                elif nuevo_anio <= 0:
                    st.error("El año no puede ser negativo o cero.")
                else:
                    actualizar_album(
                        album_sel.id,
                        nuevo_titulo.strip(),
                        int(nuevo_anio),
                        opciones_artistas[nuevo_artista_nombre]
                    )
                    st.success("Álbum actualizado. Actualizá la página para ver los cambios.")

            # --- Baja segura por ID ---
            st.subheader("Eliminar álbum")
            opciones = {f'#{al["id"]} - {al["titulo"]}': al["id"] for al in albumes}
            seleccion = st.selectbox("Seleccionar álbum a eliminar", list(opciones.keys()))
            if st.button("Eliminar álbum"):
                borrar_album(opciones[seleccion])
                st.success("Álbum eliminado. Actualizá la página para ver los cambios.")


# ---------------------------------------------------------------------------
# AGENDA DE CONCIERTOS
# ---------------------------------------------------------------------------
elif menu == "Conciertos":

    st.header("Agenda de Conciertos")

    artistas = obtener_artistas()

    if len(artistas) == 0:
        st.warning("Primero tenés que cargar artistas.")
    else:
        # --- Formulario de alta ---
        st.subheader("Agregar concierto")
        ciudad = st.text_input("Ciudad")
        fecha = st.date_input("Fecha")

        opciones_artistas = {a.nombre: a.id for a in artistas}
        artista_nombre = st.selectbox("Artista", list(opciones_artistas.keys()))

        if st.button("Agregar concierto"):
            if ciudad.strip() == "":
                st.error("La ciudad no puede estar vacía.")
            else:
                crear_concierto(ciudad.strip(), str(fecha), opciones_artistas[artista_nombre])
                st.success("Concierto agregado correctamente.")

        # --- Listado con filtro ---
        st.subheader("Lista de conciertos")
        conciertos = obtener_conciertos_con_artista()

        if len(conciertos) == 0:
            st.info("Todavía no hay conciertos cargados.")
        else:
            # Filtro dinámico por ciudad
            ciudades = sorted({c["ciudad"] for c in conciertos})
            filtro_ciudad = st.selectbox("Filtrar por ciudad", ["Todas"] + ciudades)

            for c in conciertos:
                if filtro_ciudad == "Todas" or c["ciudad"] == filtro_ciudad:
                    st.write(f'#{c["id"]} - {c["ciudad"]} - {c["fecha"]} - {c["artista"]}')

            # --- Modificación segura por ID ---
            st.subheader("Editar concierto")
            conciertos_obj = obtener_conciertos()
            opciones_edit = {f'#{c.id} - {c.ciudad}': c for c in conciertos_obj}
            sel_edit = st.selectbox("Seleccionar concierto a editar", list(opciones_edit.keys()))
            concierto_sel = opciones_edit[sel_edit]

            nueva_ciudad = st.text_input("Nueva ciudad", value=concierto_sel.ciudad, key="edit_con_ciudad")
            nueva_fecha = st.date_input("Nueva fecha", key="edit_con_fecha")

            nombres_artistas = list(opciones_artistas.keys())
            id_a_nombre = {v: k for k, v in opciones_artistas.items()}
            indice_actual = 0
            if concierto_sel.artista_id in id_a_nombre:
                indice_actual = nombres_artistas.index(id_a_nombre[concierto_sel.artista_id])
            nuevo_artista_nombre = st.selectbox(
                "Nuevo artista", nombres_artistas, index=indice_actual, key="edit_con_artista"
            )

            if st.button("Guardar cambios del concierto"):
                if nueva_ciudad.strip() == "":
                    st.error("La ciudad no puede estar vacía.")
                else:
                    actualizar_concierto(
                        concierto_sel.id,
                        nueva_ciudad.strip(),
                        str(nueva_fecha),
                        opciones_artistas[nuevo_artista_nombre]
                    )
                    st.success("Concierto actualizado. Actualizá la página para ver los cambios.")

            # --- Baja segura por ID ---
            st.subheader("Eliminar concierto")
            opciones = {f'#{c["id"]} - {c["ciudad"]} ({c["fecha"]})': c["id"] for c in conciertos}
            seleccion = st.selectbox("Seleccionar concierto a eliminar", list(opciones.keys()))
            if st.button("Eliminar concierto"):
                borrar_concierto(opciones[seleccion])
                st.success("Concierto eliminado. Actualizá la página para ver los cambios.")
