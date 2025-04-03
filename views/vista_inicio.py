from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter
from PyQt6.QtCore import Qt
import os


class VistaInicio(QWidget):
    def __init__(self, fuente_oficial):
        super().__init__()

        # Configuración básica
        self.setStyleSheet("background: transparent;")

        # Layout principal con elementos elevados
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 20)  # Margen superior reducido para subir contenido
        layout.setSpacing(20)

        # Espacio flexible superior mínimo
        layout.addStretch(1)

        # Logo más grande (400x400)
        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cargar_logo()
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Título en blanco y más grande (36px)
        titulo = QLabel("AYUNTAMIENTO DE ESPARTINAS", self)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Montserrat", 36, QFont.Weight.Bold))
        titulo.setStyleSheet("""
            color: white; 
            background: transparent; 
            margin-top: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        """)
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Subtítulo en blanco y más grande (24px)
        subtitulo = QLabel("Sistema de Gestión de Tiempos", self)
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setFont(QFont("Roboto", 24, QFont.Weight.Normal))
        subtitulo.setStyleSheet("""
            color: white; 
            background: transparent; 
            margin-bottom: 10px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        """)
        layout.addWidget(subtitulo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Espacio flexible inferior reducido para subir el contenido
        layout.addStretch(2)

    def cargar_logo(self):
        logo_path = os.path.join("assets", "logo_espartinas.png")
        if not os.path.exists(logo_path):
            logo_path = "logo_espartinas.png"

        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(400, 400,  # Logo más grande (400x400)
                              Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
            )
            self.logo_label.setFixedSize(400, 400)

    def paintEvent(self, event):
        """Dibuja el fondo con transparencia"""
        fondo_path = os.path.join("assets", "fondo_inicio.jpg")
        if os.path.exists(fondo_path):
            painter = QPainter(self)
            pixmap = QPixmap(fondo_path)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                painter.setOpacity(0.15)
                painter.drawPixmap(0, 0, pixmap)
                painter.end()