import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QWidget,
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout,
    QStackedWidget, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QGuiApplication


class CronometroApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de pantalla completa
        self.setWindowTitle("Ayuntamiento de Espartinas")
        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.showFullScreen()

        # Variables de estado
        self.minutos = 0
        self.segundos = 0
        self.corriendo = False

        # Fuentes
        self.fuente_oficial = QFont("Times New Roman", 48, QFont.Weight.Bold)
        self.fuente_secundaria = QFont("Arial", 14)

        # Crear interfaz
        self.init_ui()

    def init_ui(self):
        # Widget principal con stacked layout
        self.stacked_main = QStackedWidget()
        self.setCentralWidget(self.stacked_main)

        # 1. PANTALLA INICIAL (completa)
        self.pagina_inicio = self.crear_pagina_inicio()

        # 2. PANTALLA DIVIDIDA (cronómetro + área derecha)
        self.pagina_dividida = self.crear_pagina_dividida()

        self.stacked_main.addWidget(self.pagina_inicio)
        self.stacked_main.addWidget(self.pagina_dividida)
        self.stacked_main.setCurrentIndex(0)

        # Menú
        self.crear_menu()

    def crear_pagina_inicio(self):
        pagina = QWidget()
        layout = QVBoxLayout()
        pagina.setLayout(layout)

        # Añadir espacio flexible arriba para centrar verticalmente
        layout.addStretch(1)  # Esto empujará el contenido hacia el centro

        # Título con menos margen superior
        titulo = QLabel("AYUNTAMIENTO DE ESPARTINAS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(self.fuente_oficial)
        titulo.setStyleSheet("""
            QLabel {
                color: white;
                margin-bottom: 30px;  # Solo margen inferior
            }
        """)
        layout.addWidget(titulo)

        # Logo más grande y centrado
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = ".venv/image/logo_espartinas.png"
        pixmap = QPixmap(logo_path)

        if not pixmap.isNull():
            # Tamaño aumentado (450x450 manteniendo proporciones)
            pixmap = pixmap.scaled(450, 450,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setFixedSize(pixmap.size())
        else:
            logo_label.setText("[LOGO AYUNTAMIENTO]")
            logo_label.setStyleSheet("""
                QLabel {
                    color: white; 
                    font-size: 24px;
                    background-color: #cccccc;
                    border: 2px dashed #999999;
                    min-width: 450px;
                    min-height: 450px;
                }
            """)

        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir espacio flexible abajo para balancear el centrado
        layout.addStretch(1)

        return pagina

    def crear_pagina_dividida(self):
        pagina = QWidget()
        layout = QHBoxLayout()
        pagina.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- MITAD IZQUIERDA: Cronómetro ---
        self.left_frame = QFrame()
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout()
        self.left_frame.setLayout(left_layout)

        # Añadir espacio flexible arriba para centrar verticalmente
        left_layout.addStretch(1)

        # Editor de cronómetro
        self.titulo = QLineEdit("Cronómetro")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        left_layout.addWidget(self.titulo)

        self.display = QLabel("00:00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        left_layout.addWidget(self.display)

        controles_layout = QHBoxLayout()
        btn_min_down = QPushButton("◄ Min")
        btn_min_down.setStyleSheet(self.get_boton_style())
        btn_min_down.clicked.connect(lambda: self.ajustar_tiempo("min", -1))

        btn_seg_down = QPushButton("◄ Seg")
        btn_seg_down.setStyleSheet(self.get_boton_style())
        btn_seg_down.clicked.connect(lambda: self.ajustar_tiempo("seg", -1))

        btn_min_up = QPushButton("Min ►")
        btn_min_up.setStyleSheet(self.get_boton_style())
        btn_min_up.clicked.connect(lambda: self.ajustar_tiempo("min", 1))

        btn_seg_up = QPushButton("Seg ►")
        btn_seg_up.setStyleSheet(self.get_boton_style())
        btn_seg_up.clicked.connect(lambda: self.ajustar_tiempo("seg", 1))

        controles_layout.addStretch()
        controles_layout.addWidget(btn_min_down)
        controles_layout.addWidget(btn_seg_down)
        controles_layout.addSpacing(20)
        controles_layout.addWidget(btn_min_up)
        controles_layout.addWidget(btn_seg_up)
        controles_layout.addStretch()

        left_layout.addLayout(controles_layout)

        # Cambiar botón "Iniciar" por "Confirmar" (sin funcionalidad por ahora)
        self.btn_confirmar = QPushButton("Confirmar")
        self.btn_confirmar.setStyleSheet(self.get_boton_style("#2ecc71"))
        left_layout.addWidget(self.btn_confirmar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir espacio flexible abajo para balancear el centrado
        left_layout.addStretch(1)

        # --- MITAD DERECHA: Mismo color que el izquierdo ---
        self.right_frame = QFrame()
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setStyleSheet("background-color: #f8f9fa;")  # Mismo color que el display

        # Layout para futuros widgets
        self.right_layout = QVBoxLayout()
        self.right_frame.setLayout(self.right_layout)

        # Añadir placeholder (opcional, puedes quitarlo si prefieres)
        placeholder = QLabel("Área para implementaciones futuras")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setFont(self.fuente_secundaria)
        self.right_layout.addWidget(placeholder)

        # Añadir frames al layout principal
        layout.addWidget(self.left_frame, stretch=1)  # 50%
        layout.addWidget(self.right_frame, stretch=1)  # 50%

        # Timer (lo mantenemos por si luego implementamos funcionalidad)
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)

        return pagina

    def get_boton_style(self, color="#3498db"):
        return f"""
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
        """

    def ajustar_tiempo(self, unidad, cambio):
        if self.corriendo:
            return

        if unidad == "min":
            self.minutos = max(0, min(59, self.minutos + cambio))
        else:
            self.segundos = max(0, min(59, self.segundos + cambio))

        self.actualizar_display()

    def actualizar_display(self):
        self.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")

    def actualizar_tiempo(self):
        if self.segundos > 0:
            self.segundos -= 1
        elif self.minutos > 0:
            self.minutos -= 1
            self.segundos = 59
        else:
            self.toggle_cronometro()

        self.actualizar_display()

    def crear_menu(self):
        barra_menu = self.menuBar()

        # Menú Archivo
        archivo_menu = barra_menu.addMenu("Archivo")
        accion_agregar = archivo_menu.addAction("Agregar")
        accion_agregar.triggered.connect(self.mostrar_editor)
        archivo_menu.addAction("Eliminar")

        # Opción Salir que cierra la aplicación directamente
        archivo_menu.addAction("Salir").triggered.connect(QApplication.instance().quit)

        # Menú Editar
        barra_menu.addMenu("Editar")

        # Menú Ayuda
        barra_menu.addMenu("Ayuda").addAction("Acerca de")

    def mostrar_editor(self):
        """Cambia a la vista dividida con el cronómetro"""
        self.stacked_main.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication([])
    ventana = CronometroApp()
    ventana.show()
    app.exec()