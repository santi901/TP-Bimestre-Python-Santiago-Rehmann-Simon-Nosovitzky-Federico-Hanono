# -*- coding: utf-8 -*-
"""Clase que representa a un Artista de la productora."""


class Artista:

    def __init__(self, id, nombre, genero, pais):
        self.id = id
        self.nombre = nombre
        self.genero = genero
        self.pais = pais

    def mostrar_info(self):
        """Devuelve la ficha técnica del artista en una línea."""
        return f"{self.nombre} - {self.genero} - {self.pais}"

    def es_internacional(self):
        """True si el artista no es de Argentina."""
        return self.pais.lower() != "argentina"
