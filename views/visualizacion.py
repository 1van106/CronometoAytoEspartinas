from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class VentanaVisualizacion(QWidget):
    def __init__(self, cronometros, tipo_pleno):
        super().__init__()
        self.setWindowTitle(f"Pleno {tipo_pleno.capitalize()}")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: blue;")

        layout = QGridLayout(self)

        for i, cronometro in enumerate(cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)

            nombre_label = QLabel(cronometro["nombre"])
            nombre_label.setStyleSheet("font: bold 24px Arial; color: black; background-color: #f0f0f0; border: none;")
            contenedor_layout.addWidget(nombre_label)

            tiempo_label = QLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}", alignment=Qt.AlignmentFlag.AlignCenter)
            tiempo_label.setStyleSheet("font: 60px Arial; color: black; padding: 10px;")
            contenedor_layout.addWidget(tiempo_label)

            contenedor.setStyleSheet("border: 2px solid black; padding: 10px; background-color: #f0f0f0;")
            contenedor.setLayout(contenedor_layout)

            fila = i // 2
            columna = i % 2
            layout.addWidget(contenedor, fila, columna)

        self.setLayout(layout)
