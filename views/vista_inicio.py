from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import os


class VistaInicio(QWidget):
    def __init__(self, fuente_oficial):
        super().__init__()

        # Paleta de colores
        self.COLOR_FONDO = QColor(58, 46, 38)  # Naranja terroso oscuro
        self.COLOR_TITULO = QColor(255, 140, 66)  # Naranja vibrante
        self.SOMBRA_TITULO = "rgba(0, 0, 0, 0.3)"

        self.fuente_oficial = fuente_oficial
        self.init_ui()

    def init_ui(self):
        # Método probado que funciona - QPalette con autoFillBackground
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, self.COLOR_FONDO)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        # Configuración del layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Espacio flexible superior
        layout.addStretch(1)

        # Configuración del título
        titulo = QLabel("AYUNTAMIENTO DE ESPARTINAS", self)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fuente_titulo = QFont(self.fuente_oficial)
        fuente_titulo.setPointSize(36)
        fuente_titulo.setWeight(QFont.Weight.Bold)
        titulo.setFont(fuente_titulo)

        titulo.setStyleSheet(f"""
            QLabel {{
                color: {self.COLOR_TITULO.name()};
                margin-bottom: 30px;
                padding: 10px;
                text-shadow: 2px 2px 4px {self.SOMBRA_TITULO};
                background: transparent;
            }}
        """)
        layout.addWidget(titulo)

        # Configuración del logo
        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cargar_logo()
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Espacio flexible inferior
        layout.addStretch(1)

    def cargar_logo(self):
        logo_path = "assets/logo_espartinas.png" if os.path.exists(
            "assets/logo_espartinas.png") else "logo_espartinas.png"
        pixmap = QPixmap(logo_path)

        if not pixmap.isNull():
            pixmap = pixmap.scaled(500, 500,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setFixedSize(pixmap.size())
            self.logo_label.setStyleSheet("background: transparent; border: none;")
        else:
            self.logo_label.setText("AYTO.\nESPARTINAS")
            self.logo_label.setStyleSheet(f"""
                QLabel {{
                    font: bold 48px 'Segoe UI';
                    color: {self.COLOR_TITULO.name()};
                    background: transparent;
                    border: none;
                    text-shadow: 2px 2px 4px {self.SOMBRA_TITULO};
                }}
            """)
            self.logo_label.setFixedSize(500, 500)