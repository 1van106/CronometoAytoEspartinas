from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QIcon
from PyQt6.QtCore import Qt
import os


class VistaInicio(QWidget):
    def __init__(self, fuente_oficial):
        super().__init__()
<<<<<<< HEAD
        
        # Configuración básica
=======
        self.setWindowIcon(QIcon("assets/logo_espartinas_copy1.png"))

        # Configuración original
>>>>>>> 93fa8bcf1d65f567fafc9684a8d69ac4834c10db
        self.setStyleSheet("background: transparent;")
        self.setWindowIcon(QIcon("assets/logo_espartinas_copy1.png"))

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(20)

        # --- Elementos de la interfaz ---

        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cargar_logo()
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Título App
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

        # Subtíyulo App
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

        layout.addStretch(2)

########################################################################################################

    def cargar_logo(self):
        logo_path = os.path.join("assets", "logo_espartinas.png")
        if not os.path.exists(logo_path):
            logo_path = "logo_espartinas.png"

        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(400, 400,
                              Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
            )
            self.logo_label.setFixedSize(400, 400)

########################################################################################################

    def paintEvent(self, event):
        """Dibuja el fondo oscuro + imagen semitransparente"""
        painter = QPainter(self)

        # 1. Fondo oscuro forzado
        painter.fillRect(self.rect(), QColor(40, 40, 40))  # Color oscuro neutro

        # 2. Imagen original con transparencia (15%)
        fondo_path = os.path.join("assets", "fondo_inicio.jpg")
        if os.path.exists(fondo_path):
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