from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class VentanaVisualizacion(QWidget):
    def __init__(self, cronometros, tipo_pleno):
        super().__init__()
        self.setWindowTitle(f"Pleno {tipo_pleno.capitalize()}")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: black;")
        self.cronometros = cronometros  # Guardar referencia a los cronómetros
        self.labels_tiempos = []  # Guardar referencias a los labels de tiempo

        layout = QGridLayout(self)

        for i, cronometro in enumerate(cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)

            nombre_label = QLabel(cronometro["nombre"])
            nombre_label.setStyleSheet("font: bold 40px Arial; color: black; background-color: #f0f0f0; border: none;")
            contenedor_layout.addWidget(nombre_label)

            tiempo_label = QLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}", alignment=Qt.AlignmentFlag.AlignCenter)
            tiempo_label.setStyleSheet("font: 60px Arial; color: black; padding: 10px;")
            contenedor_layout.addWidget(tiempo_label)

            self.labels_tiempos.append(tiempo_label)  # Guardar referencia al label

            contenedor.setStyleSheet("border: 2px solid black; padding: 10px; background-color: #f0f0f0;")
            contenedor.setLayout(contenedor_layout)

            fila = i // 2
            columna = i % 2
            layout.addWidget(contenedor, fila, columna)

            # Guardar la referencia al contenedor para cambiar el color
            cronometro["contenedor"] = contenedor
            cronometro["tiempo_label"] = tiempo_label

        self.setLayout(layout)

    def actualizar_tiempo(self, index, minutos, segundos):
        """ Método para actualizar los tiempos en la interfaz """
        if 0 <= index < len(self.labels_tiempos):
            self.labels_tiempos[index].setText(f"{minutos:02d}:{segundos:02d}")

    def actualizar_color(self, index, color):
        """ Método para actualizar el color de fondo de un cronómetro """
        cronometro = self.cronometros[index]
        cronometro["contenedor"].setStyleSheet(f"background-color: {color}; border: 2px solid black;")
        
    def cambiar_a_blanco(self, index):
        """ Cambiar el fondo del cronómetro a blanco cuando está en marcha """
        self.actualizar_color(index, "#FFFFFF")  # Blanco cuando está en marcha

    def cambiar_a_rojo_translucido(self, index):
        """ Cambiar el fondo del cronómetro a rojo translúcido cuando termina """
        self.actualizar_color(index, "rgba(255, 0, 0, 0.1)")  # Rojo translúcido cuando el cronómetro termina , y en la otra from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout