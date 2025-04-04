import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QFrame,QGraphicsDropShadowEffect,
                             QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFontDatabase, QFont, QColor


class VistaDividida(QWidget):
    def __init__(self):
        super().__init__()
        # Paleta de colores con gris anaranjado
        self.COLOR_FONDO = "#332211"  # Gris oscuro con tono anaranjado
        self.COLOR_PRIMARIO = "#FF8C42"  # Naranja cálido
        self.COLOR_SECUNDARIO = "#FF9F5E"  # Naranja más claro
        self.COLOR_TEXTO = "#F5F5F5"  # Blanco ligeramente cálido
        self.COLOR_TEXTO_OSCURO = "#1A120B"  # Para texto sobre naranja
        self.COLOR_BORDE = "#FF9F5E"  # Borde naranja

        font_id = QFontDatabase.addApplicationFont("assets/DS-DIGI.TTF")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
          self.fuente_led = QFont(font_families[0], 90)
        else:
          self.fuente_led = QFont("Arial", 90)

        self.init_ui()

########################################################################################################

    def init_ui(self):
        self.setStyleSheet("background: #2B2D31")
        self.resize(400, 800)
        self.show()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Frame izquierdo (editor de cronómetro)
        self.left_frame = QFrame()
        self.left_frame.setStyleSheet(f"""
          background: #2B2D31;
          border-right: 1px solid {self.COLOR_BORDE};
        """)
        left_layout = QVBoxLayout(self.left_frame)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)

        # Título
        self.titulo = QLineEdit("")
        self.titulo.setPlaceholderText("Nombre de la Intervencion")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_titulo()
        left_layout.addWidget(self.titulo)

        # Contenedor del tiempo
        tiempo_layout = QHBoxLayout()  # Aquí mantenemos el layout horizontal
        left_layout.addLayout(tiempo_layout)

        # Contenedor para "Min"
        contenedor_min = QVBoxLayout()
        
    
        # Etiqueta de "Min" arriba del contenedor
        min_label = QLabel("MIN")
        min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        min_label.setStyleSheet(f"""
          font: bold 40px '{self.fuente_led.family()}';
          color: white;
          background: none;
          border: none;
        """)
        contenedor_min.addWidget(min_label)

        self.min_display = QLabel("00")
        self.min_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_display(self.min_display)
        contenedor_min.addWidget(self.min_display)

        # Botones de control para Min
        botones_min_layout = QHBoxLayout()
        self.btn_min_down = QPushButton("-")
        self.btn_min_up = QPushButton("+")
        self.configurar_boton_control(self.btn_min_down)
        self.configurar_boton_control(self.btn_min_up)
        botones_min_layout.addWidget(self.btn_min_down)
        botones_min_layout.addWidget(self.btn_min_up)
        contenedor_min.addLayout(botones_min_layout)

        tiempo_layout.addLayout(contenedor_min)

        # Contenedor para "Seg"
        contenedor_seg = QVBoxLayout()
        
    
        # Etiqueta de "Seg" arriba del contenedor
        seg_label = QLabel("SEG")
        seg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        seg_label.setStyleSheet(f"""
          font: bold 40px '{self.fuente_led.family()}';
          color: white;
          background: none;
          border: none;
        """)
        contenedor_seg.addWidget(seg_label)

        self.seg_display = QLabel("00")
        self.seg_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_display(self.seg_display)
        contenedor_seg.addWidget(self.seg_display)

        # Botones de control para Seg
        botones_seg_layout = QHBoxLayout()
        self.btn_seg_down = QPushButton("-")
        self.btn_seg_up = QPushButton("+")
        self.configurar_boton_control(self.btn_seg_down)
        self.configurar_boton_control(self.btn_seg_up)
        botones_seg_layout.addWidget(self.btn_seg_down)
        botones_seg_layout.addWidget(self.btn_seg_up)
        contenedor_seg.addLayout(botones_seg_layout)

        tiempo_layout.addLayout(contenedor_seg)

        # Botón principal
        self.btn_agregar = QPushButton("AGREGAR")
        self.configurar_boton_principal(self.btn_agregar)
        left_layout.addWidget(self.btn_agregar, alignment=Qt.AlignmentFlag.AlignCenter)

        left_layout.addStretch()

        # Frame derecho (lista de temporizadores)
        self.right_frame = QFrame()
        self.right_frame.setStyleSheet(f"""
          background:#2B2D31;
          border-left: 1px solid {self.COLOR_BORDE};
        """)

        self.right_layout = QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(10, 10, 10, 10)

        self.lista_temporizadores = QListWidget()
        self.lista_temporizadores.setStyleSheet("""
          QListWidget {
            background: transparent;
            border: none;
            outline: none;
          }
          QListWidget::item {
            margin-bottom: 8px;
          }
          QListWidget::item:selected {
            background: transparent;
          }
        """)
        self.right_layout.addWidget(self.lista_temporizadores)

        layout.addWidget(self.left_frame, stretch=1)
        layout.addWidget(self.right_frame, stretch=1)

########################################################################################################

    def configurar_estilo_titulo(self):
        self.titulo.setStyleSheet(f"""
            QLineEdit {{
                font: bold 40px '{self.fuente_led.family()}';
                color: white;
                padding: 12px;
                border: 2px solid {self.COLOR_PRIMARIO};
                border-radius: 6px;
                background: transparent;
            }}
            QLineEdit:focus {{
                border: 2px solid {self.COLOR_SECUNDARIO};
                background: transparent;
            }}
        """)

########################################################################################################

    def configurar_estilo_display(self, label):
        label.setFont(self.fuente_led)
        label.setStyleSheet(f"""
            QLabel {{
                color: {self.COLOR_PRIMARIO};
                padding: 10px 10px;
                background:trasparent;
                border-radius: 10px;
                border: 3px dashed {self.COLOR_PRIMARIO};
            }}
        """)

########################################################################################################

    def configurar_botones_control(self, layout):
        contenedor_controles = QWidget()
        contenedor_controles.setStyleSheet("background: transparent;")
        controles_layout = QHBoxLayout(contenedor_controles)
        controles_layout.setContentsMargins(0, 0, 0, 0)
        controles_layout.setSpacing(10)

        for btn in [self.btn_min_down, self.btn_seg_down, self.btn_min_up, self.btn_seg_up]:
            self.configurar_boton_control(btn)
            controles_layout.addWidget(btn)

        layout.addWidget(contenedor_controles, alignment=Qt.AlignmentFlag.AlignCenter)

########################################################################################################

    def configurar_boton_control(self, boton):
        boton.setStyleSheet(f"""
            QPushButton {{
                font: bold 40px '{self.fuente_led.family()}';
                color: {self.COLOR_TEXTO};
                background: {self.COLOR_PRIMARIO};
                padding: 8px 12px;
                border: none;
                border-radius: 5px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {self.COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                background:  {self.COLOR_SECUNDARIO};
            }}
        """)

########################################################################################################

    def configurar_boton_principal(self, boton):
        boton.setStyleSheet(f"""
            QPushButton {{
                font: bold 40px '{self.fuente_led.family()}';
                color: {self.COLOR_TEXTO};
                background: {self.COLOR_PRIMARIO};
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                min-width: 200px;
                text-transform: uppercase;
            }}
            QPushButton:hover {{
                background: {self.COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                background: #E67329;
            }}
        """)

########################################################################################################

    def agregar_temporizador_ui(self, cronometro, controlador):
        """Agrega un temporizador a la interfaz con estilo moderno"""
        item = QListWidgetItem()
        widget = self.crear_widget_temporizador(cronometro, controlador)
        item.setSizeHint(widget.sizeHint())
        self.lista_temporizadores.addItem(item)
        self.lista_temporizadores.setItemWidget(item, widget)
        cronometro.widget = widget

########################################################################################################

    def crear_widget_temporizador(self, cronometro, controlador):
        """Crea un widget de temporizador con diseño moderno"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            background: transparent;
            border: 2px solid {self.COLOR_PRIMARIO};
            border-radius: 8px;
            padding: 12px;
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Título del temporizador
        nombre_label = QLabel(cronometro.nombre)
        nombre_label.setStyleSheet(f"""
            font: bold 40px '{self.fuente_led.family()}';
            color:{self.COLOR_TEXTO};
            padding-bottom: 5px;
            border: 2px solid {self.COLOR_PRIMARIO};
        """)
        nombre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nombre_label)

        # Tiempo del temporizador
        tiempo_label = QLabel(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")
        tiempo_label.setFont(self.fuente_led)
        tiempo_label.setStyleSheet(f"""
            color: {self.COLOR_PRIMARIO};
            padding: 0px;
            margin:0;
            border: 2px dashed {self.COLOR_PRIMARIO};
        """)
        tiempo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tiempo_label)

        # Botones de acción
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(0, 0, 10, 0)
        botones_layout.setSpacing(10)

        # Botón Editar
        btn_editar = QPushButton()
        if os.path.exists("assets/lapiz.png"):
            btn_editar.setIcon(QIcon("assets/lapiz.png"))
            btn_editar.setToolTip("Editar")
        else:
            btn_editar.setText("Editar")
        btn_editar.setStyleSheet(f"""
            QPushButton {{
                background: {self.COLOR_PRIMARIO};
                border: none;
                border-radius: 4px;
                padding: 6px;
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
            }}
            QPushButton:hover {{
                background: {self.COLOR_SECUNDARIO};
            }}
        """)
        btn_editar.clicked.connect(lambda: controlador.editar_temporizador(cronometro))

        # Botón Eliminar
        btn_eliminar = QPushButton()
        if os.path.exists("assets/papelera.png"):
            btn_eliminar.setIcon(QIcon("assets/papelera.png"))
            btn_eliminar.setToolTip("Eliminar")
        else:
            btn_eliminar.setText("X")
        btn_eliminar.setStyleSheet(f"""
            QPushButton {{
                background:  {self.COLOR_PRIMARIO};
                border: none;
                border-radius: 4px;
                padding: 6px;
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
                
            }}
            QPushButton:hover {{
                background: #FF6B5B;
            }}
        """)
        btn_eliminar.clicked.connect(lambda: controlador.eliminar_temporizador(cronometro))

        botones_layout.addStretch()
        botones_layout.addWidget(btn_editar)
        botones_layout.addWidget(btn_eliminar)
        

        layout.addLayout(botones_layout)

        return widget

########################################################################################################

    def actualizar_temporizador_ui(self, cronometro):
        """Actualiza la UI de un temporizador existente"""
        if cronometro.widget:
            labels = cronometro.widget.findChildren(QLabel)
            if len(labels) >= 2:
                labels[0].setText(cronometro.nombre)
                labels[1].setText(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")