from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout

class VentanaControles(QMainWindow):
    # Señal para notificar la actualización del cronómetro
    tiempo_actualizado = pyqtSignal(int, int, int)  # (índice del cronómetro, minutos, segundos)

    def __init__(self, cronometros, tipo_pleno):
        super().__init__()
        self.tipo_pleno = tipo_pleno
        self.setWindowTitle("Controles de Cronómetros")
        self.cronometros = cronometros  # Lista de cronómetros
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        label = QLabel(f"Visualización del pleno: {self.tipo_pleno}", self)
        layout.addWidget(label)
        self.lista_temporizadores = QListWidget()
        layout.addWidget(self.lista_temporizadores)

        # Agregar los cronómetros a la lista de controles
        for i, cronometro in enumerate(self.cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)

            # Nombre del cronómetro
            nombre_label = QLabel(cronometro['nombre'], alignment=Qt.AlignmentFlag.AlignCenter)
            contenedor_layout.addWidget(nombre_label)

            # Mostrar tiempo
            tiempo_label = QLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}", alignment=Qt.AlignmentFlag.AlignCenter)
            contenedor_layout.addWidget(tiempo_label)

            # Controles
            botones_layout = QHBoxLayout()

            # Botón Play
            btn_play = QPushButton("Play")
            btn_play.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
            btn_play.clicked.connect(lambda _, cronometro=cronometro, tiempo_label=tiempo_label, index=i: self.iniciar_cronometro(cronometro, tiempo_label, index))

            # Botón Stop
            btn_stop = QPushButton("Stop")
            btn_stop.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; border-radius: 5px;")
            btn_stop.clicked.connect(lambda _, cronometro=cronometro, index=i: self.detener_cronometro(cronometro, index))

            # Botón Reset
            btn_reset = QPushButton("Reset")
            btn_reset.setStyleSheet("background-color: #f39c12; color: white; padding: 10px; border-radius: 5px;")
            btn_reset.clicked.connect(lambda _, cronometro=cronometro, tiempo_label=tiempo_label, index=i: self.reset_cronometro(cronometro, tiempo_label, index))

            botones_layout.addWidget(btn_play)
            botones_layout.addWidget(btn_stop)
            botones_layout.addWidget(btn_reset)

            contenedor_layout.addLayout(botones_layout)

            # Agregar el cronómetro al widget de la lista
            item = QListWidgetItem()
            item.setSizeHint(contenedor.sizeHint())
            self.lista_temporizadores.addItem(item)
            self.lista_temporizadores.setItemWidget(item, contenedor)

        self.setCentralWidget(central_widget)

    def iniciar_cronometro(self, cronometro, tiempo_label, index):
        if 'corriendo' not in cronometro:
            cronometro['corriendo'] = False

        if 'minutos_originales' not in cronometro or 'segundos_originales' not in cronometro:
            cronometro['minutos_originales'] = cronometro['minutos']
            cronometro['segundos_originales'] = cronometro['segundos']

        if not cronometro["corriendo"]:
            cronometro["corriendo"] = True
            cronometro["timer"] = QTimer(self)
            cronometro["timer"].timeout.connect(lambda: self.actualizar_tiempo(cronometro, tiempo_label, index))
            cronometro["timer"].start(1000)

    def detener_cronometro(self, cronometro, index):
        if cronometro["corriendo"]:
            cronometro["corriendo"] = False
            cronometro["timer"].stop()

    def reset_cronometro(self, cronometro, tiempo_label, index):
        cronometro["minutos"] = cronometro["minutos_originales"]
        cronometro["segundos"] = cronometro["segundos_originales"]

        if cronometro["corriendo"]:
            cronometro["corriendo"] = False
            cronometro["timer"].stop()

        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])

    def actualizar_tiempo(self, cronometro, tiempo_label, index):
        if cronometro["segundos"] > 0:
            cronometro["segundos"] -= 1
        elif cronometro["minutos"] > 0:
            cronometro["minutos"] -= 1
            cronometro["segundos"] = 59
        else:
            self.detener_cronometro(cronometro, index)

        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])
