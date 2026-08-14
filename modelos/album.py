# -*- coding: utf-8 -*-
"""Clase que representa a un Álbum lanzado por un artista."""

from datetime import date


class Album:

    def __init__(self, id, titulo, anio, artista_id):
        self.id = id
        self.titulo = titulo
        self.año = año
        self.artista_id = artista_id

    def mostrar_info(self):
        """Devuelve la ficha técnica del álbum."""
        return f"{self.titulo} ({self.año})"

    def calcular_antiguedad(self):
        """Calcula los años de antigüedad del álbum respecto al año actual."""
        año_actual = date.today().year
        return año_actual - self.año

    def es_antiguo(self):
        """True si el álbum fue lanzado antes de 2010."""
        return self.año < 2010
