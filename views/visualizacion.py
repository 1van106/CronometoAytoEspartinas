from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap, QKeyEvent
from widgets.auto_font_label import AutoFontLabel

class VentanaVisualizacion(QWidget):
    def __init__(self, cronometros, tipo_pleno):
        super().__init__()

        # Cargar la fuente
        font_id = QFontDatabase.addApplicationFont("assets/DS-DIGI.TTF")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        self.fuente_led = QFont(font_families[0]) if font_families else QFont("Arial")

        self.setWindowTitle(f"Pleno {tipo_pleno.capitalize()}")
        self.setStyleSheet("background-color: black;")
        self.cronometros = cronometros
        self.labels_tiempos = []

        self._drag_pos = None  # Para movimiento con el ratón

        # Layout principal
        layout = QGridLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        for i, cronometro in enumerate(cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)
            contenedor_layout.setSpacing(10)
            contenedor_layout.setContentsMargins(0, 0, 0, 0)

            # Fila superior con numeración, logo y nombre
            fila_superior = QHBoxLayout()
            fila_superior.setSpacing(10)
            fila_superior.setContentsMargins(10, 10, 10, 10)

            numeracion_label = QLabel(f"{i + 1}")
            numeracion_label.setStyleSheet("font: bold 30px Arial; color: #2B2D31; background-color: transparent; padding: 4px;")
            numeracion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fila_superior.addWidget(numeracion_label)

            if cronometro.get("logo"):
                logo_label = QLabel()
                pixmap = QPixmap(cronometro["logo"]).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(pixmap)
                logo_label.setStyleSheet("border: none;")
                fila_superior.addWidget(logo_label)

            nombre_label = QLabel(cronometro["nombre"])
            nombre_label.setStyleSheet("font: bold 30px Arial; color: black; background-color: transparent;")
            fila_superior.addWidget(nombre_label)
            fila_superior.addStretch()

            contenedor_layout.addLayout(fila_superior)

            tiempo_label = AutoFontLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
            tiempo_label.setStyleSheet("""
              background-color: #E0E0E0;
              color: #6B6B6B;
              border: none;
            """)
            tiempo_label.setFont(self.fuente_led)
            contenedor_layout.addWidget(tiempo_label, stretch=1)

            # Agregar el numeracion_label al diccionario de cada cronometro
            cronometro["numeracion_label"] = numeracion_label

            # Agregar el numeracion_label al diccionario de cada cronometro
            cronometro["numeracion_label"] = numeracion_label
            cronometro["tiempo_label"] = tiempo_label
            cronometro["contenedor"] = contenedor
            

            self.labels_tiempos.append(tiempo_label)

            contenedor.setLayout(contenedor_layout)
            contenedor.setStyleSheet(" background-color: #E0E0E0;")

            fila = i // 2
            columna = i % 2
            layout.addWidget(contenedor, fila, columna)


        self.setLayout(layout)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

########################################################################################

    def keyPressEvent(self, event: QKeyEvent):
        """Cerrar con ESC"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()

########################################################################################

    # Drag and Move 
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

########################################################################################

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint()
            delta = new_pos - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = new_pos

########################################################################################

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = None

########################################################################################   

    def actualizar_tiempo(self, index, minutos, segundos):
        """Actualiza el texto del cronómetro correspondiente"""
        if 0 <= index < len(self.labels_tiempos):
            self.labels_tiempos[index].setText(f"{minutos:02d}:{segundos:02d}")

########################################################################################   

    def actualizar_color(self, index, fondo_color, texto_color):
        """Actualiza el color de fondo y texto del cronómetro especificado"""
        if 0 <= index < len(self.cronometros):
            contenedor = self.cronometros[index]["contenedor"]
            tiempo_label = self.cronometros[index]["tiempo_label"]
            numeracion_label = self.cronometros[index]["numeracion_label"]  # Título/número

            # Cambiar estilo del contenedor
            contenedor.setStyleSheet(
              f"background-color: {fondo_color}; "
            )

            # Cambiar estilo del display del tiempo (sin afectar el tamaño de la fuente)
            tiempo_label.setStyleSheet(
              f"background-color: {fondo_color}; color: {texto_color}; border: none;"
            )

            # Cambiar el color del título/número (sin afectar el tamaño de la fuente)
            numeracion_label.setStyleSheet(
              f"color: {texto_color}; background-color: transparent;"
            )

########################################################################################   

    def cambiar_a_blanco(self, index):
        """Cambia el color a blanco cuando el cronómetro está activo"""
        self.actualizar_color(index, "#FFFFFF", "black")

########################################################################################   

    def cambiar_a_rojo_translucido(self, index):
        """Cambia el color a rojo translúcido cuando el tiempo se ha pasado"""
        self.actualizar_color(index, "rgba(255, 100, 100, 0.3)", "black")

########################################################################################   

    def apagar_cronometro(self, index):
        """Apaga el cronómetro (colores apagados cuando está detenido)"""
        self.actualizar_color(index, "#E0E0E0", "#6B6B6B")

########################################################################################   

    def closeEvent(self, event):
        """Cierra la ventana correctamente"""
        event.accept()