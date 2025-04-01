import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QFrame,
                             QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


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

        self.init_ui()

    def init_ui(self):
        # Configuración del fondo degradado
        self.setStyleSheet(f"""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.COLOR_FONDO}, 
                stop:1 #2A1A0F
            );
        """)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Frame izquierdo (editor de cronómetro)
        self.left_frame = QFrame()
        self.left_frame.setStyleSheet(f"""
            background: rgba(30, 20, 10, 0.6);
            border-right: 1px solid {self.COLOR_BORDE};
        """)
        left_layout = QVBoxLayout(self.left_frame)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)

        # Componentes del cronómetro
        self.titulo = QLineEdit("")
        self.titulo.setPlaceholderText("Nombre de la Intervención")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_titulo()
        left_layout.addWidget(self.titulo)

        self.display = QLabel("00:00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_display()
        left_layout.addWidget(self.display, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botones de control
        self.btn_min_down = QPushButton("◄ Min")
        self.btn_seg_down = QPushButton("◄ Seg")
        self.btn_min_up = QPushButton("Min ►")
        self.btn_seg_up = QPushButton("Seg ►")
        self.configurar_botones_control(left_layout)

        # Botón principal
        self.btn_agregar = QPushButton("AGREGAR")
        self.configurar_boton_principal(self.btn_agregar)
        left_layout.addWidget(self.btn_agregar, alignment=Qt.AlignmentFlag.AlignCenter)

        left_layout.addStretch()

        # Frame derecho (lista de temporizadores)
        self.right_frame = QFrame()
        self.right_frame.setStyleSheet(f"""
            background: rgba(30, 20, 10, 0.6);
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

    def configurar_estilo_titulo(self):
        self.titulo.setStyleSheet(f"""
            QLineEdit {{
                font: bold 16px 'Segoe UI';
                color: {self.COLOR_TEXTO};
                padding: 12px;
                border: 2px solid {self.COLOR_PRIMARIO};
                border-radius: 6px;
                background: rgba(45, 45, 45, 0.7);
            }}
            QLineEdit:focus {{
                border: 2px solid {self.COLOR_SECUNDARIO};
                background: rgba(45, 45, 45, 0.9);
            }}
        """)

    def configurar_estilo_display(self):
        self.display.setStyleSheet(f"""
            QLabel {{
                font: bold 72px 'Segoe UI';
                color: {self.COLOR_PRIMARIO};
                padding: 20px 40px;
                background: rgba(45, 45, 45, 0.7);
                border-radius: 10px;
                border: 3px solid {self.COLOR_PRIMARIO};
            }}
        """)
        self.display.setMinimumWidth(300)

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

    def configurar_boton_control(self, boton):
        boton.setStyleSheet(f"""
            QPushButton {{
                font: bold 12px 'Segoe UI';
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
                background: #E67329;
            }}
        """)

    def configurar_boton_principal(self, boton):
        boton.setStyleSheet(f"""
            QPushButton {{
                font: bold 14px 'Segoe UI';
                color: {self.COLOR_TEXTO_OSCURO};
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

    def agregar_temporizador_ui(self, cronometro, controlador):
        """Agrega un temporizador a la interfaz con estilo moderno"""
        item = QListWidgetItem()
        widget = self.crear_widget_temporizador(cronometro, controlador)
        item.setSizeHint(widget.sizeHint())
        self.lista_temporizadores.addItem(item)
        self.lista_temporizadores.setItemWidget(item, widget)
        cronometro.widget = widget

    def crear_widget_temporizador(self, cronometro, controlador):
        """Crea un widget de temporizador con diseño moderno"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            background: rgba(30, 20, 10, 0.8);
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
            font: bold 18px 'Segoe UI';
            color: {self.COLOR_PRIMARIO};
            padding-bottom: 5px;
            border-bottom: 1px solid {self.COLOR_PRIMARIO};
        """)
        nombre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nombre_label)

        # Tiempo del temporizador
        tiempo_label = QLabel(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")
        tiempo_label.setStyleSheet(f"""
            font: 32px 'Segoe UI';
            color: {self.COLOR_TEXTO};
            padding: 5px;
        """)
        tiempo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tiempo_label)

        # Botones de acción
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(0, 10, 0, 0)
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
                background: #E74C3C;
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
        botones_layout.addStretch()

        layout.addLayout(botones_layout)

        return widget

    def actualizar_temporizador_ui(self, cronometro):
        """Actualiza la UI de un temporizador existente"""
        if cronometro.widget:
            labels = cronometro.widget.findChildren(QLabel)
            if len(labels) >= 2:
                labels[0].setText(cronometro.nombre)
                labels[1].setText(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")