from PyQt6.QtCore import QTimer


class Cronometro:
    def __init__(self, nombre, minutos, segundos):
        self.nombre = nombre
        self.minutos = minutos
        self.segundos = segundos
        self.corriendo = False
        self.timer = None
        self.widget = None
        self.minutos_originales = minutos  # Guardar valores originales
        self.segundos_originales = segundos

########################################################################################################

    def iniciar(self, callback_actualizacion, callback_alarma):
        if not self.corriendo:
            self.corriendo = True
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self._actualizar(callback_actualizacion, callback_alarma))
            self.timer.start(1000)

########################################################################################################

    def detener(self):
        if self.corriendo:
            self.corriendo = False
            if self.timer:
                self.timer.stop()
                self.timer = None

########################################################################################################

    def resetear(self, minutos=None, segundos=None):
        self.detener()
        if minutos is not None:
            self.minutos = minutos
        if segundos is not None:
            self.segundos = segundos
        else:
            # Si no se especifican valores, usar los originales
            self.minutos = self.minutos_originales
            self.segundos = self.segundos_originales

########################################################################################################

    def _actualizar(self, callback_actualizacion, callback_alarma):
        if self.segundos > 0:
            self.segundos -= 1
        elif self.minutos > 0:
            self.minutos -= 1
            self.segundos = 59
        else:
            self.detener()
            callback_alarma()
            return

        callback_actualizacion()