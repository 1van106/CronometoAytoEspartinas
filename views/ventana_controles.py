from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt6.QtGui import  QFontDatabase, QFont, QKeySequence, QShortcut,QIcon
from views.visualizacion import VentanaVisualizacion
from functools import partial
from models import cronometro

class VentanaControles(QMainWindow):
    # Señal para sincronizar los cronómetros entre ventanas
    tiempo_actualizado = pyqtSignal(int, int, int)  

    def __init__(self, cronometros, tipo_pleno, sound_alarm):
        super().__init__()
        
        self.setWindowIcon(QIcon("assets/logo_espartinas_copy1.png"))
        self.tipo_pleno = tipo_pleno
        button_cerrar = QPushButton("Cerrar")
        button_cerrar.clicked.connect(self.cerrar_todo)

        layout = QVBoxLayout()
        layout.addWidget(button_cerrar)
        
        self.setWindowTitle(f"Pleno {self.tipo_pleno}")
        self.sound_alarm = sound_alarm
        self.cronometros = cronometros 
        self.tiempo_labels = [] 
        self.resize(440, 920)

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
        central_widget.setStyleSheet("background-color:white ;border:None;padding:0;margin:0;")
        self.setCentralWidget(central_widget)

      
        self.lista_temporizadores = QListWidget()
        layout.addWidget(self.lista_temporizadores)

        for i, cronometro in enumerate(self.cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)

            contenedor.setStyleSheet(f"""
                background-color: white;
                color:#2B2D31;
                font: bold 40px '{self.fuente_led.family()}';
                border: 1.5px solid #2B2D31;                     
                padding: 5px;
                margin: 0;                     
            """)

            nombre_label = QLabel(f"{i + 1}. {cronometro['nombre']}")
            nombre_label.setStyleSheet(f"""
                font: bold 30px 'Arial';color: #2B2D31; background-color:  white; border: 2px solid #2B2D31;
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

            if i < 9:  # teclas del 1 al 9
                tecla = str(i + 1)
                shortcut = QShortcut(QKeySequence(tecla), self)
                # Conectar atajo de teclas numéricas al cronómetro correspondiente
                shortcut.activated.connect(lambda idx=i: self.toggle_cronometro(idx))

                # **Atajos dinámicos para Ctrl+1, Ctrl+2, ..., Ctrl+9 (Reset)**
                shortcut_reset = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
                # El _ es el evento que es pasado por defecto a los atajos
                shortcut_reset.activated.connect(lambda c=cronometro, t=tiempo_label, index=i: self.reset_cronometro(c, t, index))

        self.setCentralWidget(central_widget)

########################################################################################################

    def cerrar_todo(self):
        
        self.close()

########################################################################################################
    
    def toggle_cronometro(self, index):
        cronometro = self.cronometros[index]
        tiempo_label = cronometro.get('tiempo_label', None)  
    
        if 'corriendo' not in cronometro or not cronometro['corriendo']:
          self.iniciar_cronometro(cronometro, tiempo_label, index)
        else:
          self.detener_cronometro(cronometro, index)


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
                background-color: #2B2D31;
                color:  white;
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

    
    def actualizar_color_display(self, cronometro, estado):
        """Actualiza el color del display de tiempo según el estado."""
        tiempo_label = cronometro['tiempo_label']
        numeracion_label = cronometro['numeracion_label']  # Título/número
        contenedor = cronometro['contenedor']

        if estado == 'inactivo':
            # Cuando el cronómetro está inactivo, se ve apagado (gris)
            tiempo_label.setStyleSheet("""
            
              padding: 10px;
              background-color: #E0E0E0; 
            """)
            numeracion_label.setStyleSheet("""
              font: bold 30px Arial;
              background-color: #E0E0E0;
            """)
            contenedor.setStyleSheet("""
              background-color: #E0E0E0;
          
            """)

        elif estado == 'activo':
            # Cuando el cronómetro está activo, se ve blanco
            tiempo_label.setStyleSheet("""
            color: #2B2D31;  /* Gris oscuro */
            padding: 10px;
            background-color: #F5F5F5;
            
            """)
            numeracion_label.setStyleSheet("""
            color: #2B2D31;  
            background-color: #F5F5F5;
            font: bold 30px Arial;
            """)
            contenedor.setStyleSheet("""
              background-color: #F5F5F5;
            """)
        elif estado == 'pasado':
            # Cuando el cronómetro se pasa, se pone rojo/naranja cálido
            tiempo_label.setStyleSheet("""
              padding: 10px;
              background-color:#FF6B6B;
              
            """)
            numeracion_label.setStyleSheet("""
              font: bold 30px Arial;
              background-color: #FF6B6B;
            """)
            contenedor.setStyleSheet("""
              background-color: #FF6B6B;
            """)



########################################################################################################

    def iniciar_cronometro(self, cronometro, tiempo_label, index):
        """Inicia o reinicia el cronómetro asegurando que todo el estado se maneje correctamente."""
        # Verificamos si el cronómetro está detenido
        if "corriendo" not in cronometro or not cronometro["corriendo"]:
            print(f"Iniciando cronómetro {index} con tiempo {cronometro['minutos']}:{cronometro['segundos']}")
          
            # Marcamos el cronómetro como corriendo
            cronometro["corriendo"] = True
            
        
            # Si ya hay un timer, lo detenemos
            if "timer" in cronometro:
                cronometro["timer"].stop()

            # Creamos y arrancamos el timer
            cronometro["timer"] = QTimer(self)
            cronometro["timer"].timeout.connect(lambda: self.actualizar_tiempo(cronometro, tiempo_label, index))
            cronometro["timer"].start(1000)  # 1 segundo

            # Cambiamos el color de la interfaz a activo
            self.actualizar_color_display(cronometro, 'activo')

            # Actualizamos la interfaz
            self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])

        else:
            print(f"El cronómetro {index} ya está corriendo. No se puede iniciar de nuevo.")


########################################################################################################

    def detener_cronometro(self, cronometro, index):
        if cronometro.get("corriendo", False):
          cronometro["corriendo"] = False
          cronometro["timer"].stop()

          self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])

          # Cambiar el color a apagado (inactivo)
          self.actualizar_color_display(cronometro, 'inactivo')

########################################################################################################

    def reset_cronometro(self, cronometro, tiempo_label, index):
        """Resetea el cronómetro y lo detiene si está corriendo."""
    
        # Restauramos el tiempo original
        cronometro["minutos"] = cronometro.get("minutos_originales", 0)
        cronometro["segundos"] = cronometro.get("segundos_originales", 0)

        # Desactivamos la alarma si ha sonado
        cronometro["alarma_sonada"] = False

        # Restauramos el estado de "corriendo" a False
        cronometro["corriendo"] = False
    
        # Detenemos el cronómetro si está corriendo
        if "timer" in cronometro and cronometro["corriendo"]:  # Verifica si el temporizador está en ejecución
            cronometro["timer"].stop()
            cronometro["corriendo"] = False   # Detener el temporizador

        # Restauramos el color de la interfaz (para indicar que está inactivo)
        self.actualizar_color_display(cronometro, 'inactivo')

        # Actualizamos el texto en la interfaz
        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")

        # Emitir la señal para actualizar la interfaz
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])
    
        print(f"Cronómetro {index} reseteado: {cronometro['minutos']:02d}:{cronometro['segundos']:02d}")




########################################################################################################

    def sonar_alarma(self):
        if self.sound_alarm:
          self.sound_alarm.play()

########################################################################################################

    def actualizar_tiempo(self, cronometro, tiempo_label, index):
        # Reducir el tiempo del cronómetro
        if cronometro["segundos"] > 0:
            cronometro["segundos"] -= 1
        elif cronometro["minutos"] > 0:
            cronometro["minutos"] -= 1
            cronometro["segundos"] = 59
        else:
            # Si el cronómetro llegó a 00:00
            if "alarma_sonada" not in cronometro:
                cronometro["alarma_sonada"] = True
                self.sonar_alarma()  # Suena la alarma
                self.actualizar_color_display(cronometro, 'pasado') 
                self._sincronizar_cronometros(cronometro)

            # Continúa en tiempo negativo
            cronometro["segundos"] -= 1
            if cronometro["segundos"] < 0:
                cronometro["segundos"] = 59
                cronometro["minutos"] -= 1
 
            

        # Actualizar la interfaz con el nuevo tiempo
        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        print(f"Tiempo actualizado: {cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
        self.tiempo_actualizado.emit(index, cronometro['minutos'], cronometro['segundos'])
        

########################################################################################################

    def _sincronizar_cronometros(self, cronometro):
        print(f"Sincronizando cronómetros para {cronometro['nombre']}")

        nombre_base = cronometro["nombre"].split('.')[0]
        print(f"Nombre base del cronómetro: {nombre_base}")

        if 'corriendo' not in cronometro:
            cronometro['corriendo'] = False

        similares = [c for c in self.cronometros if c != cronometro and c["nombre"].split('.')[0] == nombre_base]

        if not similares:
            print(f"No se encontraron cronómetros con el mismo nombre base: {nombre_base}")
            return

        cronometro_duracion = cronometro["minutos_originales"] * 60 + cronometro["segundos_originales"]
        print(f"Duración del cronómetro actual {cronometro['nombre']}: {cronometro_duracion} segundos")

        for index, menor in enumerate(similares):
            if 'corriendo' not in menor:
                menor['corriendo'] = False

            menor_duracion = menor["minutos_originales"] * 60 + menor["segundos_originales"]
            print(f"Duración del cronómetro {menor['nombre']}: {menor_duracion} segundos")

            if menor_duracion < cronometro_duracion and not menor["corriendo"]:
                print(f"Iniciando cronómetro {menor['nombre']} ya que su duración es menor.")
                menor["corriendo"] = True
                menor["timer"] = QTimer(self)

                # Usamos `partial` para pasar los parámetros correctamente a la función
                menor["timer"].timeout.connect(partial(self.actualizar_tiempo, menor, menor['tiempo_label'], index))

                menor["timer"].start(1000)
                self.tiempo_actualizado.emit(index, menor['minutos'], menor['segundos'])
                self.actualizar_color_display(menor, 'activo')




      
########################################################################################################

     
    @staticmethod
    def _obtener_nombre_base(nombre):
        return nombre.split('.')[0]