from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit,
                             QPushButton, QScrollArea, QFrame)
from PyQt6.QtCore import Qt


class VentanaGuia(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guía de Usuario - Cronómetro Municipal")
        self.resize(900, 700)

        # Configuración del layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(10, 10, 10, 10)

        # Área scrollable para contenido largo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Widget contenedor del contenido
        contenido_widget = QWidget()
        layout_contenido = QVBoxLayout(contenido_widget)
        layout_contenido.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 1. Sección de Introducción
        self.agregar_seccion(layout_contenido,
                             "Introducción",
                             "Esta aplicación está diseñada para gestionar los tiempos de intervención "
                             "en los plenos del Ayuntamiento de Espartinas.")

        # 2. Sección del Menú Principal
        self.agregar_seccion(layout_contenido,
                             "Menú Principal",
                             self.obtener_descripcion_menu())

        # 3. Sección de Funcionamiento Básico
        self.agregar_seccion(layout_contenido,
                             "Funcionamiento del Cronómetro",
                             self.obtener_descripcion_cronometro())

        # 4. Sección de Visualización
        self.agregar_seccion(layout_contenido,
                             "Modo Visualización",
                             self.obtener_descripcion_visualizacion())

        scroll.setWidget(contenido_widget)
        layout_principal.addWidget(scroll)

        # Botón de cerrar
        btn_cerrar = QPushButton("Cerrar Guía")
        btn_cerrar.clicked.connect(self.close)
        layout_principal.addWidget(btn_cerrar)

        self.setLayout(layout_principal)

    def agregar_seccion(self, layout, titulo, contenido):
        """Añade una sección estructurada a la guía"""
        # Marco para la sección
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("margin-bottom: 20px;")
        frame_layout = QVBoxLayout(frame)

        # Título de sección
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        frame_layout.addWidget(lbl_titulo)

        # Contenido
        texto = QTextEdit()
        texto.setHtml(contenido)
        texto.setReadOnly(True)
        frame_layout.addWidget(texto)

        layout.addWidget(frame)

    def obtener_descripcion_menu(self):
        """Devuelve la descripción HTML del menú"""
        return """
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
        """

    def obtener_descripcion_cronometro(self):
        """Devuelve la descripción HTML del cronómetro"""
        return """
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

        <h3>Uso Durante el Pleno:</h3>
        <p>Una vez configurados los temporizadores, acceda a <b>Visualización > Ver Pleno...</b> para mostrar:</p>
        <ul>
            <li>Temporizadores activos con cuenta regresiva</li>
            <li>Indicador visual cuando el tiempo se agota</li>
            <li>Sonido de aviso (si está configurado)</li>
        </ul>
        """

    def obtener_descripcion_visualizacion(self):
        """Devuelve la descripción HTML del modo visualización"""
        return """
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
        """