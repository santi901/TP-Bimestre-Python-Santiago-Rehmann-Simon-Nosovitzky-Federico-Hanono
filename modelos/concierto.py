# -*- coding: utf-8 -*-
"""Clase que representa a un Concierto de la agenda."""


class Concierto:

    def __init__(self, id, ciudad, fecha, artista_id):
        self.id = id
        self.ciudad = ciudad
        self.fecha = fecha
        self.artista_id = artista_id

    def mostrar_info(self):
        """Devuelve la ficha técnica del concierto."""
        return f"{self.ciudad} - {self.fecha}"

    def es_en_buenos_aires(self):
        """True si el concierto es en Buenos Aires."""
        return self.ciudad.lower() == "buenos aires"
