from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import os


class VistaInicio(QWidget):
    def __init__(self, fuente_oficial):
        super().__init__()
        # Paleta de colores más anaranjada
        self.COLOR_FONDO = "#FF6B35"  # Naranja intenso
        self.COLOR_TEXTO = "#FFFFFF"  # Blanco puro
        self.COLOR_TITULO = "#292F36"  # Azul oscuro para contraste
        self.SOMBRA_TITULO = "#FF9B71"  # Naranja claro para sombra

        self.fuente_oficial = fuente_oficial
        self.init_ui()

    def init_ui(self):
        # Fondo anaranjado con degradado
        self.setStyleSheet(f"""
            background: qlineargradient(
                x1:0, y1:0, x2:0.5, y2:0.5,
                stop:0 {self.COLOR_FONDO},
                stop:1 #FF914D
            );
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        # Espacio flexible superior
        layout.addStretch(1)

        # Título con efecto destacado
        titulo = QLabel("AYUNTAMIENTO DE ESPARTINAS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Fuente más grande y con peso
        fuente_titulo = QFont(self.fuente_oficial)
        fuente_titulo.setPointSize(36)
        fuente_titulo.setWeight(QFont.Weight.Bold)
        titulo.setFont(fuente_titulo)

        titulo.setStyleSheet(f"""
            QLabel {{
                color: {self.COLOR_TITULO};
                margin-bottom: 30px;
                padding: 10px;
                text-shadow: 3px 3px 6px {self.SOMBRA_TITULO};
            }}
        """)
        layout.addWidget(titulo)

        # Logo sin marco ni fondo
        self.logo_label = QLabel()
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
            # Logo más grande y centrado sin marco
            pixmap = pixmap.scaled(500, 500,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setFixedSize(pixmap.size())
            self.logo_label.setStyleSheet("background: transparent; border: none;")
        else:
            # Texto alternativo estilizado
            self.logo_label.setText("AYTO.\nESPARTINAS")
            self.logo_label.setStyleSheet(f"""
                QLabel {{
                    font: bold 48px 'Segoe UI';
                    color: {self.COLOR_TITULO};
                    background: transparent;
                    border: none;
                    text-shadow: 2px 2px 4px {self.SOMBRA_TITULO};
                }}
            """)
            self.logo_label.setFixedSize(500, 500)