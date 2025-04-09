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

    def iniciar(self, callback_actualizacion, callback_alarma):
        if not self.corriendo:
            self.corriendo = True
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self._actualizar(callback_actualizacion, callback_alarma))
            self.timer.start(1000)

    ##################################################################################

    def detener(self):
        if self.corriendo:
            self.corriendo = False
            if self.timer:
                self.timer.stop()
                self.timer = None

    ##################################################################################

    def resetear(self, minutos=None, segundos=None):
        self.detener()
        if minutos is not None:
            self.minutos = minutos
        if segundos is not None:
            self.segundos = segundos
        else:
            self.minutos = self.minutos_originales
            self.segundos = self.segundos_originales
        self.ya_entro_en_exceso = False

########################################################################################

    def _actualizar(self, callback_actualizacion, callback_alarma):
        if self.segundos > 0:
            self.segundos -= 1
        elif self.minutos > 0:
            self.minutos -= 1
            self.segundos = 59
        else:
            self.detener()  # Detener el cronómetro cuando llegue a 00:00
            callback_alarma()  # Llamar al callback de alarma
            if not self.ya_entro_en_exceso:
                self.ya_entro_en_exceso = True
                self._sincronizar_cronometros()  # Sincronizar los cronómetros cuando se pase de tiempo
            return

        callback_actualizacion()  # Actualizar la interfaz

        # Si el tiempo se ha agotado y no se ha sincronizado aún, se hace ahora
        if self.minutos == 0 and self.segundos == 0 and not self.ya_entro_en_exceso:
            self.ya_entro_en_exceso = True
            self._sincronizar_cronometros()

########################################################################################

    def _sincronizar_cronometros(self):
        if not self.todos_cronometros:
            return

        nombre_base = self._obtener_nombre_base(self.nombre)

        # Buscar cronómetros con el mismo nombre base (excluyendo este cronómetro)
        similares = [
            c for c in self.todos_cronometros
            if c != self and self._obtener_nombre_base(c.nombre) == nombre_base
        ]

        if not similares:
            return

        # Este cronómetro ya está en exceso. Ver cuál tiene menor duración
        self_duracion = self.minutos_originales * 60 + self.segundos_originales
        menores = [c for c in similares if (c.minutos_originales * 60 + c.segundos_originales) < self_duracion]

        for menor in menores:
            if not menor.corriendo:
                # Si el cronómetro más corto aún no ha empezado, forzamos su inicio
                menor.resetear(minutos=menor.minutos_originales, segundos=menor.segundos_originales)
                menor.iniciar(lambda: None, lambda: None)  # Forzamos el inicio del cronómetro