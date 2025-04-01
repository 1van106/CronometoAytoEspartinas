from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class VistaInicio(QWidget):
    def __init__(self, fuente_oficial):
        super().__init__()
        self.fuente_oficial = fuente_oficial
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addStretch(1)

        # Título
        titulo = QLabel("AYUNTAMIENTO DE ESPARTINAS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(self.fuente_oficial)
        titulo.setStyleSheet("QLabel { color: blue; margin-bottom: 30px; }")
        layout.addWidget(titulo)

        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cargar_logo()
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(1)

    def cargar_logo(self):
        logo_path = "assets/logo_espartinas.png" if os.path.exists(
            "assets/logo_espartinas.png") else "logo_espartinas.png"
        pixmap = QPixmap(logo_path)

        if not pixmap.isNull():
            pixmap = pixmap.scaled(450, 450,
                                 Qt.AspectRatioMode.KeepAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setFixedSize(pixmap.size())
        else:
            self.logo_label.setText("[LOGO AYUNTAMIENTO]")
            self.logo_label.setStyleSheet("""
                QLabel {
                    color: white; 
                    font-size: 24px;
                    background-color: #cccccc;
                    border: 2px dashed #999999;
                    min-width: 450px;
                    min-height: 450px;
                }
            """)