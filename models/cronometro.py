from PyQt6.QtCore import QTimer
import re

class Cronometro:
    def __init__(self, nombre, minutos, segundos, numeracion=None, logo=None, todos_cronometros=None):
        self.nombre = nombre
        self.minutos = minutos
        self.segundos = segundos
        self.numeracion = numeracion
        self.corriendo = False
        self.timer = None
        self.widget = None
        self.logo_path = logo 
        self.minutos_originales = minutos
        self.segundos_originales = segundos
        self.ya_entro_en_exceso = False
        self.todos_cronometros = todos_cronometros  # Lista de todos los cronómetros

    ##################################################################################



   