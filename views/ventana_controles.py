from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt6.QtGui import  QFontDatabase, QFont
from views.visualizacion import VentanaVisualizacion

class VentanaControles(QMainWindow):
    # Señal para sincronizar los cronómetros entre ventanas
    tiempo_actualizado = pyqtSignal(int, int, int)  

    def __init__(self, cronometros, tipo_pleno, sound_alarm):
        super().__init__()
        self.tipo_pleno = tipo_pleno
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.sound_alarm = sound_alarm
        self.cronometros = cronometros 
        self.resize(270, 820)

        font_id = QFontDatabase.addApplicationFont("assets/DS-DIGI.TTF")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
          self.fuente_led = QFont(font_families[0], 90)
        else:
          self.fuente_led = QFont("Arial", 90) 

        self.init_ui()

########################################################################################################

    def init_ui(self):
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        central_widget.setStyleSheet("background-color: #2B2D31;border:3px solid #FF9F5E;")
        label = QLabel(f"Pleno {self.tipo_pleno}", self)
        label.setStyleSheet(f"""
            font: bold 20px '{self.fuente_led.family()}'; 
            color: #FF9F5E;
            background-color:#2B2D31;
            text-align: center;
            padding: 10px;
        """)
        layout.addWidget(label)
        self.lista_temporizadores = QListWidget()
        layout.addWidget(self.lista_temporizadores)

        for i, cronometro in enumerate(self.cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)

            contenedor.setStyleSheet(f"""
                background-color: #2B2D31;
                color:#FF9F5E;
                font: bold 40px '{self.fuente_led.family()}';
                border: 1.5px solid black;                     
                padding: 3px;
                margin: 0;                     
            """)

            nombre_label = QLabel(cronometro['nombre'])
            nombre_label.setStyleSheet(f"""
                font: bold 20px '{self.fuente_led.family()}';color: #FF9F5E; background-color:  #2B2D31; border: none;
                """)
            contenedor_layout.addWidget(nombre_label)

            tiempo_label = QLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}", alignment=Qt.AlignmentFlag.AlignCenter)

            botones_layout = QHBoxLayout()
            btn_play = QPushButton("Play")
            self.aplicar_estilo_boton(btn_play)
            btn_play.clicked.connect(lambda _, c=cronometro, t=tiempo_label, index=i: self.iniciar_cronometro(c, t, index))

            btn_stop = QPushButton("Stop")
            self.aplicar_estilo_boton(btn_stop)
            btn_stop.clicked.connect(lambda _, c=cronometro, index=i: self.detener_cronometro(c, index))

            btn_reset = QPushButton("Reset")
            self.aplicar_estilo_boton(btn_reset)
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

########################################################################################################

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

########################################################################################################

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

########################################################################################################

    def aplicar_estilo_boton(self, boton):
        """Aplica estilos a los botones de Play, Stop y Reset."""
        boton.setStyleSheet(f"""
            QPushButton {{
                background-color: #FF9F5E;
                color:  #2B2D31;
                font: bold 20px '{self.fuente_led.family()}';
                padding: 5px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #E07A00;
            }}
            QPushButton:pressed {{
                background-color: #C96900;
            }}
        """)

########################################################################################################

    def iniciar_cronometro(self, cronometro, tiempo_label, index):
        if 'corriendo' not in cronometro:
            cronometro['corriendo'] = False

        if not cronometro["corriendo"]:
            cronometro["corriendo"] = True
            cronometro["timer"] = QTimer(self)
            cronometro["timer"].timeout.connect(lambda: self.actualizar_tiempo(cronometro, tiempo_label, index))
            cronometro["timer"].start(1000)

            self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])

            # Cambiar el color a blanco
            cronometro["contenedor"].setStyleSheet("background-color: #FFFFFF; border: 2px solid black;")

########################################################################################################

    def detener_cronometro(self, cronometro, index):
        if cronometro["corriendo"]:
          cronometro["corriendo"] = False
          cronometro["timer"].stop()

          self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])

          cronometro["contenedor"].setStyleSheet("background-color:  #f0f0f0; border: 2px solid black;")

########################################################################################################

    def reset_cronometro(self, cronometro, tiempo_label, index):
        # Usamos los valores originales para restaurar el tiempo
        cronometro["minutos"] = cronometro.get("minutos_originales", 0)
        cronometro["segundos"] = cronometro.get("segundos_originales", 0)
 
        if cronometro["corriendo"]:
          cronometro["corriendo"] = False
          cronometro["timer"].stop()

        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])  # Emitir señal

########################################################################################################

    def sonar_alarma(self):
        if self.sound_alarm:
          self.sound_alarm.play()

########################################################################################################

    def actualizar_tiempo(self, cronometro, tiempo_label, index):
        if cronometro["segundos"] > 0:
            cronometro["segundos"] -= 1
        elif cronometro["minutos"] > 0:
            cronometro["minutos"] -= 1
            cronometro["segundos"] = 59
        else:
            if "alarma_sonada" not in cronometro:
              cronometro["alarma_sonada"] = True
              self.sonar_alarma()
              cronometro["contenedor"].setStyleSheet("background-color: rgba(255, 0, 0, 0.6); border: 2px solid black;")

            # Continúa en tiempo negativo
            cronometro["segundos"] -= 1
            if cronometro["segundos"] < 0:
              cronometro["segundos"] = 59
              cronometro["minutos"] -= 1

        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])