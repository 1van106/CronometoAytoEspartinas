from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout

class VentanaControles(QMainWindow):
    # Señal para sincronizar los cronómetros entre ventanas
    tiempo_actualizado = pyqtSignal(int, int, int)  # (índice, minutos, segundos)

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

        for i, cronometro in enumerate(self.cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)

            nombre_label = QLabel(cronometro['nombre'], alignment=Qt.AlignmentFlag.AlignCenter)
            contenedor_layout.addWidget(nombre_label)

            tiempo_label = QLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}", alignment=Qt.AlignmentFlag.AlignCenter)
            contenedor_layout.addWidget(tiempo_label)

            botones_layout = QHBoxLayout()
            btn_play = QPushButton("Play")
            btn_play.clicked.connect(lambda _, c=cronometro, t=tiempo_label, index=i: self.iniciar_cronometro(c, t, index))

            btn_stop = QPushButton("Stop")
            btn_stop.clicked.connect(lambda _, c=cronometro, index=i: self.detener_cronometro(c, index))

            btn_reset = QPushButton("Reset")
            btn_reset.clicked.connect(lambda _, c=cronometro, t=tiempo_label, index=i: self.reset_cronometro(c, t, index))

            botones_layout.addWidget(btn_play)
            botones_layout.addWidget(btn_stop)
            botones_layout.addWidget(btn_reset)

            contenedor_layout.addLayout(botones_layout)

            item = QListWidgetItem()
            item.setSizeHint(contenedor.sizeHint())
            self.lista_temporizadores.addItem(item)
            self.lista_temporizadores.setItemWidget(item, contenedor)

        self.setCentralWidget(central_widget)

    def iniciar_cronometro(self, cronometro, tiempo_label, index):
        if 'corriendo' not in cronometro:
            cronometro['corriendo'] = False

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
        cronometro["minutos"] = cronometro.get("minutos_originales", 0)
        cronometro["segundos"] = cronometro.get("segundos_originales", 0)

        if cronometro["corriendo"]:
            cronometro["corriendo"] = False
            cronometro["timer"].stop()

        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])  # Emitir señal

    def actualizar_tiempo(self, cronometro, tiempo_label, index):
        if cronometro["segundos"] > 0:
            cronometro["segundos"] -= 1
        elif cronometro["minutos"] > 0:
            cronometro["minutos"] -= 1
            cronometro["segundos"] = 59
        else:
            self.detener_cronometro(cronometro, index)

        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])  # Emitir señal
