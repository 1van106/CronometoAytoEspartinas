from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class VentanaInfo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Información de la Aplicación")
        self.setWindowIcon(QIcon("assets/logo_espartinas_copy1.png"))
        self.resize(800, 600)
        self.setStyleSheet("background-color: #f8f9fa;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        self.texto_info = QTextBrowser()
        self.texto_info.setOpenExternalLinks(True)
        self.texto_info.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: none;
                font-size: 16px;  /* Aumento del tamaño de la fuente */
                color: #333;
                padding: 15px;  /* Aumento de padding para dar más espacio */
                margin: 10px;  /* Margen adicional */
                line-height: 1.8;  /* Ajuste de la altura de las líneas */
                min-width: 750px;  /* Aumento del ancho mínimo */
                min-height: 500px;  /* Aumento de la altura mínima */
            }
        """)

        html_info = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                line-height: 1.6;
                color: #333;
                background-color: white;
                padding: 20px;
                margin: 0;
            }

            h1 {
                text-align: center;
                color: #2c3e50;
                font-size: 28px;
                margin-bottom: 20px;
                background-color: #eaf2f8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            }

            .section {
                margin-bottom: 30px;
            }

            p {
                margin: 10px 0;
            }

            .info-label {
                font-weight: bold;
                color: #3498db;
            }

            .footer {
                margin-top: 30px;
                text-align: center;
                font-size: 14px;
                color: #777;
                border-top: 1px solid #ddd;
                padding-top: 15px;
            }
        </style>
        </head>
        <body>

        <h1>Información de la Aplicación</h1>

        <div class="section">
            <p><span class="info-label">Nombre:</span> Cronómetro Municipal</p>
            <p><span class="info-label">Versión:</span> 1.0.0</p>
            <p><span class="info-label">Desarrollado por:</span> Ayuntamiento de Espartinas</p>
            <p><span class="info-label">Entidad:</span> Ayuntamiento de Espartinas</p>
            <p><span class="info-label">Descripción:</span> Aplicación diseñada para gestionar y visualizar los tiempos de intervención durante los plenos municipales.</p>
        </div>

        <div class="footer">
            © 2025 Ayuntamiento de Espartinas · Todos los derechos reservados
        </div>

        </body>
        </html>
        """

        self.texto_info.setHtml(html_info)
        layout.addWidget(self.texto_info, alignment=Qt.AlignmentFlag.AlignTop)
