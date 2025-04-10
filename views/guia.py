from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextBrowser,
                             QPushButton, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor


class VentanaGuia(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guía de Usuario - Cronómetro Municipal")
        self.resize(1000, 750)
        self.setStyleSheet("background-color: #f8f9fa;")

        # Layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Área de scroll principal (única)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("border: none; background-color: #f8f9fa;")

        # Widget contenedor
        contenido_widget = QWidget()
        contenido_widget.setStyleSheet("background-color: white;")
        self.layout_contenido = QVBoxLayout(contenido_widget)
        self.layout_contenido.setContentsMargins(40, 40, 40, 40)
        self.layout_contenido.setSpacing(30)

        # Contenido HTML unificado
        self.texto_guia = QTextBrowser()
        self.texto_guia.setOpenExternalLinks(True)
        self.texto_guia.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: none;
                font-size: 14px;
                color: #333;
                padding: 0;
            }
        """)

        # Configurar el documento HTML
        self.configurar_guia_completa()

        self.layout_contenido.addWidget(self.texto_guia)
        scroll_area.setWidget(contenido_widget)
        layout_principal.addWidget(scroll_area)

        # Botón de cerrar
        btn_cerrar = QPushButton("Cerrar Guía")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 6px;
                margin: 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_cerrar.clicked.connect(self.close)
        layout_principal.addWidget(btn_cerrar, alignment=Qt.AlignmentFlag.AlignCenter)

    def configurar_guia_completa(self):
        """Configura todo el contenido de la guía en un solo documento HTML"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
            }
            .seccion {
                margin-bottom: 40px;
            }
            h1 {
                color: #2c3e50;
                font-size: 24px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-top: 0;
            }
            h2 {
                color: #3498db;
                font-size: 20px;
                margin-top: 30px;
                margin-bottom: 15px;
            }
            h3 {
                color: #2c3e50;
                font-size: 18px;
                margin-top: 25px;
            }
            ul, ol {
                margin-top: 10px;
                margin-bottom: 15px;
                padding-left: 30px;
            }
            li {
                margin-bottom: 8px;
            }
            b, strong {
                color: #e74c3c;
            }
            i {
                color: #7f8c8d;
            }
            .nota {
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 10px 15px;
                margin: 15px 0;
            }
        </style>
        </head>
        <body>
        """

        # Sección de Introducción
        html_content += """
        <div class='seccion'>
            <h1>Guía de Usuario del Cronómetro Municipal</h1>
            <p>Esta aplicación está diseñada para gestionar los tiempos de intervención en los plenos del Ayuntamiento de Espartinas.</p>
        </div>
        """

        # Sección del Menú Principal
        html_content += """
        <div class='seccion'>
            <h2>1. Menú Principal</h2>

            <h3>Estructura del Menú:</h3>
            <ul>
                <li><b>Menú Admin:</b>
                    <ul>
                        <li><i>Pleno Ordinario:</i> Configura los temporizadores para plenos ordinarios</li>
                        <li><i>Pleno Extraordinario:</i> Configura los temporizadores para plenos extraordinarios</li>
                    </ul>
                </li>
                <li><b>Menú Visualización:</b>
                    <ul>
                        <li><i>Ver Pleno Ordinario:</i> Muestra la pantalla de visualización para plenos ordinarios</li>
                        <li><i>Ver Pleno Extraordinario:</i> Muestra la pantalla de visualización para plenos extraordinarios</li>
                    </ul>
                </li>
                <li><b>Ayuda:</b>
                    <ul>
                        <li><i>Guía:</i> Muestra este manual de instrucciones</li>
                        <li><i>Información:</i> Muestra detalles sobre la aplicación</li>
                    </ul>
                </li>
                <li><b>Salir:</b> Cierra la aplicación (icono en la esquina superior derecha)</li>
            </ul>
        </div>
        """

        # Sección de Funcionamiento Básico
        html_content += """
        <div class='seccion'>
            <h2>2. Funcionamiento del Cronómetro</h2>

            <h3>Configuración de Temporizadores:</h3>
            <ol>
                <li>Seleccione <b>Admin > Pleno Ordinario/Extraordinario</b></li>
                <li>En la pantalla de configuración:
                    <ul>
                        <li>Introduzca el nombre del interveniente</li>
                        <li>Establezca el tiempo con los botones +/- minutos/segundos</li>
                        <li>Haga clic en <b>Agregar</b> para añadir el temporizador</li>
                    </ul>
                </li>
                <li>Los temporizadores añadidos aparecerán en la lista lateral</li>
                <li>Puede editar o eliminar temporizadores con los iconos correspondientes</li>
            </ol>

            <div class='nota'>
                <b>Nota:</b> Los cambios se guardan automáticamente cuando se añaden o modifican temporizadores.
            </div>

            <h3>Uso Durante el Pleno:</h3>
            <p>Una vez configurados los temporizadores, acceda a <b>Visualización > Ver Pleno...</b> para mostrar:</p>
            <ul>
                <li>Temporizadores activos con cuenta regresiva</li>
                <li>Indicador visual cuando el tiempo se agota</li>
                <li>Sonido de aviso (si está configurado)</li>
            </ul>
        </div>
        """

        # Sección de Visualización
        html_content += """
        <div class='seccion'>
            <h2>3. Modo Visualización</h2>

            <h3>Pantalla de Visualización:</h3>
            <p>Esta pantalla está diseñada para mostrarse durante las sesiones plenarias:</p>
            <ul>
                <li>Muestra el tiempo restante de cada intervención</li>
                <li>Cambia de color cuando el tiempo está por agotarse</li>
                <li>Muestra alertas visuales cuando el tiempo se ha agotado</li>
            </ul>

            <h3>Controles Adicionales:</h3>
            <p>Desde la ventana de controles (que se abre automáticamente):</p>
            <ul>
                <li>Puede pausar/reanudar temporizadores individuales</li>
                <li>Reiniciar tiempos si es necesario</li>
                <li>Ajustar volúmenes de notificaciones</li>
            </ul>
        </div>
        """

        html_content += """
        </body>
        </html>
        """

        self.texto_guia.setHtml(html_content)
        # Mover el cursor al inicio
        self.texto_guia.moveCursor(QTextCursor.MoveOperation.Start)