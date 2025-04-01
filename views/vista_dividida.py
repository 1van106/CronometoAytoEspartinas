import os

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QFrame,
                             QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class VistaDividida(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Frame izquierdo (cronómetro)
        self.left_frame = QFrame()
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout(self.left_frame)
        left_layout.addStretch(1)

        # Componentes del cronómetro
        self.titulo = QLineEdit("")
        self.titulo.setPlaceholderText("Título de la Intervención")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_titulo()
        left_layout.addWidget(self.titulo)

        self.display = QLabel("00:00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_display()
        left_layout.addWidget(self.display)

        # Botones de control
        self.btn_min_down = QPushButton("◄ Min")
        self.btn_seg_down = QPushButton("◄ Seg")
        self.btn_min_up = QPushButton("Min ►")
        self.btn_seg_up = QPushButton("Seg ►")

        self.configurar_botones_controles(left_layout)

        # Botón agregar/actualizar
        self.btn_agregar = QPushButton("Agregar")
        self.configurar_boton(self.btn_agregar, "#2ecc71")
        left_layout.addWidget(self.btn_agregar, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addStretch(1)

        # Frame derecho (lista)
        self.right_frame = QFrame()
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setStyleSheet("background-color: #f8f9fa;")

        self.right_layout = QVBoxLayout(self.right_frame)
        self.lista_temporizadores = QListWidget()
        self.right_layout.addWidget(self.lista_temporizadores)

        layout.addWidget(self.left_frame, stretch=1)
        layout.addWidget(self.right_frame, stretch=1)

    def configurar_estilo_titulo(self):
        self.titulo.setStyleSheet("""
            QLineEdit {
                font: bold 18px 'Arial';
                color: #2c3e50;
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin: 10px 50px;
                background: #ecf0f1;
            }
        """)

    def configurar_estilo_display(self):
        self.display.setStyleSheet("""
            QLabel {
                font: bold 60px 'Arial';
                color: #3498db;
                margin: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 12px;
                border: 3px solid #bdc3c7;
            }
        """)

    def configurar_botones_controles(self, layout):
        controles_layout = QHBoxLayout()

        controles_layout.addStretch()

        self.configurar_boton(self.btn_min_down)
        controles_layout.addWidget(self.btn_min_down)

        self.configurar_boton(self.btn_seg_down)
        controles_layout.addWidget(self.btn_seg_down)

        controles_layout.addSpacing(20)

        self.configurar_boton(self.btn_min_up)
        controles_layout.addWidget(self.btn_min_up)

        self.configurar_boton(self.btn_seg_up)
        controles_layout.addWidget(self.btn_seg_up)

        controles_layout.addStretch()

        layout.addLayout(controles_layout)

    def configurar_boton(self, boton, color="#3498db"):
        boton.setStyleSheet(f"""
            QPushButton {{
                font: bold 14px 'Arial';
                color: white;
                background: {color};
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                min-width: 100px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background: #2980b9;
            }}
        """)

    def agregar_temporizador_ui(self, cronometro, controlador):
        """Agrega un temporizador a la interfaz"""
        item = QListWidgetItem()
        widget = self.crear_widget_temporizador(cronometro, controlador)
        item.setSizeHint(widget.sizeHint())
        self.lista_temporizadores.addItem(item)
        self.lista_temporizadores.setItemWidget(item, widget)
        cronometro.widget = widget

    def crear_widget_temporizador(self, cronometro, controlador):
        """Crea el widget UI para un temporizador"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Título
        nombre_label = QLabel(cronometro.nombre)
        nombre_label.setStyleSheet("font: bold 24px Arial; color: black;")
        nombre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nombre_label)

        # Tiempo
        tiempo_label = QLabel(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")
        tiempo_label.setStyleSheet("""
            font: 36px Arial; 
            color: black; 
            border: 3px solid black;
            padding: 10px;
            margin: 10px;
        """)
        tiempo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tiempo_label)

        # Botones
        botones_layout = QHBoxLayout()

        btn_play = QPushButton("Play")
        btn_play.setStyleSheet("""
            QPushButton {
                font: bold 14px Arial;
                background-color: #2ecc71;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
        """)
        btn_play.clicked.connect(lambda: controlador.toggle_cronometro(cronometro))

        btn_reset = QPushButton("Reset")
        btn_reset.setStyleSheet("""
            QPushButton {
                font: bold 14px Arial;
                background-color: #3498db;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
        """)
        btn_reset.clicked.connect(lambda: cronometro.resetear(cronometro.minutos, cronometro.segundos))

        # Agregar icono de editar (lápiz)
        btn_editar = QPushButton()
        btn_editar.setIcon(QIcon("assets/lapiz.png")) \
            if os.path.exists("assets/lapiz.png") else btn_editar.setText("Editar")
        btn_editar.clicked.connect(lambda: controlador.editar_temporizador(cronometro))

        # Agregar icono de eliminar (papelera)
        btn_eliminar = QPushButton()
        btn_eliminar.setIcon(QIcon("assets/papelera.png")) \
            if os.path.exists("assets/papelera.png") else btn_eliminar.setText("Eliminar")
        btn_eliminar.clicked.connect(lambda: controlador.eliminar_temporizador(cronometro))

        botones_layout.addWidget(btn_play)
        botones_layout.addWidget(btn_reset)
        botones_layout.addWidget(btn_editar)
        botones_layout.addWidget(btn_eliminar)
        layout.addLayout(botones_layout)

        widget.setStyleSheet("""
            border: 2px solid black;
            padding: 10px;
            margin: 5px;
            background-color: #f0f0f0;
        """)

        return widget

    def actualizar_temporizador_ui(self, cronometro):
        """Actualiza la UI de un temporizador existente"""
        if cronometro.widget:
            labels = cronometro.widget.findChildren(QLabel)
            if len(labels) >= 2:
                labels[0].setText(cronometro.nombre)
                labels[1].setText(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")