from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextBrowser,
                             QPushButton, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtGui import QIcon



class VentanaGuia(QWidget):
    def __init__(self):
        super().__init__()

        # Título y tamaño de la ventana
        self.setWindowTitle("Guía de Usuario - Cronómetro Municipal")

        self.setWindowIcon(QIcon("assets/logo_espartinas_copy1.png"))
        self.resize(1000, 750)

        # Estilo general del fondo
        self.setStyleSheet("background-color: #f8f9fa;")

        # Layout principal de la ventana
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Área de scroll principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("border: none; background-color: #f8f9fa;")

        # Widget contenedor del contenido desplazable
        contenido_widget = QWidget()
        contenido_widget.setStyleSheet("background-color: white;")

        # Layout para el contenido dentro del scroll
        self.layout_contenido = QVBoxLayout(contenido_widget)
        self.layout_contenido.setContentsMargins(40, 40, 40, 40)
        self.layout_contenido.setSpacing(30)

        # QTextBrowser que mostrará la guía en formato HTML
        self.texto_guia = QTextBrowser()
        self.texto_guia.setOpenExternalLinks(True)  # Permitir enlaces externos
        self.texto_guia.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border: none;
                font-size: 14px;
                color: #333;
                padding: 0;
            }
        """)

        # Llama a la función que arma el HTML de la guía
        self.configurar_guia_completa()

        # Añadir QTextBrowser al layout
        self.layout_contenido.addWidget(self.texto_guia)
        scroll_area.setWidget(contenido_widget)

        # Agregar scroll_area al layout principal
        layout_principal.addWidget(scroll_area)

        # Botón para cerrar la guía
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
        btn_cerrar.clicked.connect(self.close)  # Acción del botón
        layout_principal.addWidget(btn_cerrar, alignment=Qt.AlignmentFlag.AlignCenter)

########################################################################################################

    def configurar_guia_completa(self):
        """
        Crea el contenido HTML de la guía de usuario.
        Puedes personalizar este contenido para incluir imágenes, estilos, títulos y secciones.
        Las imágenes deben estar en una ruta accesible desde donde se ejecuta la app.
        """
        html_content = """ 
        <!DOCTYPE html>
        <html>
        <head>
        <style>

            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
            }

            .seccion {
                margin-bottom: 30px;
            }

            h1 {
                color: #2c3e50;
                font-size: 32px;
                text-align: center;
                margin: 0 0 20px 0;
                background-color: #eaf2f8;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            }

            h2 {
                color: #3498db;
                font-size: 24px;
                margin: 20px 0 10px 0;
                border-left: 5px solid #3498db;
                padding-left: 10px;
            }

            h3 {
                color: #2c3e50;
                font-size: 20px;
                margin: 15px 0 5px 0;
            }

            p {
                margin: 10px 0;
            }

            ul, ol {
                margin: 10px 0 10px 20px;
                padding: 0;
            }

            li {
                margin-bottom: 6px;
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
                margin: 20px 0;
                font-style: italic;
            }

            .imagen {
                text-align: center;
                margin: 20px 0;
                width: 100%;
            }

            .imagen img,
            .imagen .img-ajustada {
                display: inline-block;
                max-width: 600px;
                width: 100%;
                height: auto;
                border: 1px solid #ccc;
                border-radius: 6px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
                margin: 0 auto;
            }
            
        </style>
        </head>
        
        <body>

        <!-- Título principal -->
        <div class='seccion'>
            <h1>Guía de Usuario del Cronómetro Municipal</h1>
            <p style="text-align: center;">
                Esta aplicación está diseñada para gestionar los tiempos de intervención en los plenos del Ayuntamiento de Espartinas.
            </p>
            <div class="imagen">
                <img class="img-ajustada" src="assets/vista_general.png" alt="Vista general de la aplicación">
            </div>
        </div>

        <!-- Menú principal -->
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
                <li><b>Salir:</b> Cierra la aplicación</li>
            </ul>
            <div class="imagen">
                <img src="assets/menu.png" alt="Captura del menú principal">
            </div>
        </div>

        <!-- Configuración de cronómetro -->
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
                        <li>A la derecha se generará un listado con los temporizadores creados</li>
                        <li>Arrastre y suelte los temporizadores del listado para cambiar el orden si lo desea</li>
                    </ul>
                </li>
            </ol>
            <div class='nota'>
                <b>Nota:</b> Los cambios se guardan automáticamente cuando se añaden o modifican temporizadores.
            </div>
            <div class="imagen">
                <img class="img-ajustada" src="assets/configuracion.jpg" alt="Configuración del temporizador">
            </div>

                    </ul>
                </li>
            </ol>

        </div>

        <!-- Modo de visualización -->
        <div class='seccion'>
            <h2>3. Modo Visualización</h2>
            <li>Seleccione <b>Visualización > Pleno Ordinario/Extraordinario</b> para ver los temporizadores activos</li>
            <p>Se mostrarán dos ventanas una para el control de los temporizadores y otra para la visualización.</p>
            <h3>Ventana Visualización:</h3>
            <p>Esta ventana se utiliza durante el pleno para mostrar los tiempos en curso.</p>
            <ul>
                <li>Arrastre y suelte la ventana en el monitor donde vaya a ser visualizado</li>
                <li>Cuenta regresiva visible</li>
                <li>Indicador visual cuando el tiempo se agota</li>
                <li>Sonido de aviso</li>
            </ul>
            <h3>Ventana de controles:</h3>
            <p>Esta ventana se utiliza durante el pleno para controlar los tiempos en curso.</p>
            <ul>
                <li>Botones Play, Stop y Reset en cada temporizador</li>
                <li>Atajos de teclado:</li>
                <p>
                Puedes controlar los temporizadores con el teclado sin necesidad de usar el ratón, lo que facilita el manejo durante el pleno.
                </p>
                <ul>
                    <li><b>1</b>: Inicia o pausa el primer temporizador</li>
                    <li><b>Ctrl + 1</b>: Reinicia el primer temporizador</li>
                    <li><b>2</b>: Inicia o pausa el segundo temporizador</li>
                    <li><b>Ctrl + 2</b>: Reinicia el segundo temporizador</li>
                    <li><b>3</b>: Inicia o pausa el tercer temporizador</li>
                    <li><b>Ctrl + 3</b>: Reinicia el tercer temporizador</li>
                    <li><i>Y así sucesivamente con los demás temporizadores...</i></li>
                </ul>
            </ul>
            <div class="imagen">
                <img class="img-ajustada" src="assets/pantalla_visualizacion1.png" alt="Pantalla de controles y visualización del pleno">
            </div>    
        </div>

        <!-- Sincronización de Cronómetros -->
        <div class='seccion'>
            <h2>4. Sincronización de Cronómetros</h2>
            <p>
                La funcionalidad de sincronización permite gestionar múltiples cronómetros de manera que, cuando uno termine, el siguiente cronómetro en la secuencia comenzará automáticamente a descontar su tiempo. Esto se logra mediante el uso de un "nombre base" compartido entre los cronómetros.
            </p>
            <h3>¿Cómo funciona?</h3>
            <ol>
                <li><b>Configuración inicial:</b> Cuando creas un cronómetro, le asignas un nombre único. Los cronómetros que comparten el mismo "nombre base" estarán sincronizados. El nombre base es la parte inicial del nombre del cronómetro, seguido de un punto.</li>
                <li><b>Sincronización:</b> Los cronómetros que comparten el mismo nombre base se vinculan. Esto significa que, cuando uno termine, el siguiente comenzará automáticamente. Por ejemplo, "Intervención PSOE. 1" y "Intervención PSOE. 2" compartirán el nombre base "Intervención PSOE".</li>
                <li><b>Secuencia de ejecución:</b> Al terminar un cronómetro sincronizado, el siguiente cronómetro con el mismo nombre base comenzará. Los cronómetros se ejecutan en secuencia sin necesidad de intervención manual.</li>
            </ol>
            <h3>Ejemplo de sincronización:</h3>
            <ol>
                <li>Cuando el cronómetro <b>Intervención PSOE. 1</b> llegue a cero, el cronómetro <b>Intervención PSOE. 2</b> comenzará a descontar automáticamente.</li>
                <li>Si tienes más cronómetros con el mismo nombre base (por ejemplo, <b>Intervención PSOE. 3</b>, <b>Intervención PSOE. 4</b>, etc.), el mismo comportamiento ocurrirá: al terminar uno, el siguiente comenzará automáticamente.</li>
            </ol>
            <h3>Ventajas:</h3>
            <ul>
                <li>Facilita la gestión de cronómetros cuando hay múltiples intervenciones consecutivas de la misma persona o grupo.</li>
            </ul>
            <div class="nota">
                <b>Nota:</b> La sincronización solo funciona cuando los cronómetros comparten el mismo nombre base y están correctamente configurados en la aplicación.
            </div>
        </div>
        </body>
        </html>
        """
        self.texto_guia.setHtml(html_content)

        self.texto_guia.moveCursor(QTextCursor.MoveOperation.Start)  # Mostrar desde el inicio

        self.texto_guia.moveCursor(QTextCursor.MoveOperation.Start)  # Mostrar desde el inicio

