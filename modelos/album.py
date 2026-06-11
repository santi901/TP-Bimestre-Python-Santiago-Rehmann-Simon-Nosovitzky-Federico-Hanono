# -*- coding: utf-8 -*-
"""Clase que representa a un Álbum lanzado por un artista."""

from datetime import date


class Album:

    def __init__(self, id, titulo, anio, artista_id):
        self.id = id
        self.titulo = titulo
        self.anio = anio
        self.artista_id = artista_id

    def mostrar_info(self):
        """Devuelve la ficha técnica del álbum."""
        return f"{self.titulo} ({self.anio})"

    def calcular_antiguedad(self):
        """Calcula los años de antigüedad del álbum respecto al año actual."""
        anio_actual = date.today().year
        return anio_actual - self.anio

    def es_antiguo(self):
        """True si el álbum fue lanzado antes de 2010."""
        return self.anio < 2010
