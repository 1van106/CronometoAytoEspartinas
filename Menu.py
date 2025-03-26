from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu,
                             QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class CronometroApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Cronómetro Elegante")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 450)

        # Variables de estado
        self.minutos = 0
        self.segundos = 0
        self.corriendo = False

        # Crear interfaz
        self.init_ui()

    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 1. Título editable (estilizado)
        self.titulo = QLineEdit("Mi Cronómetro")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("""
            QLineEdit {
                font: bold 24px 'Arial';
                color: #2c3e50;
                padding: 15px;
                border: 3px solid #3498db;
                border-radius: 10px;
                margin: 20px 100px;
                background: #ecf0f1;
            }
        """)
        layout.addWidget(self.titulo)

        # 2. Display del tiempo (estilizado)
        self.display = QLabel("00:00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setStyleSheet("""
            QLabel {
                font: bold 72px 'Arial';
                color: #3498db;
                margin: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 15px;
                border: 4px solid #bdc3c7;
            }
        """)
        layout.addWidget(self.display)

        # 3. Controles de tiempo
        controles_layout = QHBoxLayout()

        # Botón - Minutos
        btn_min_down = QPushButton("◄ Min")
        btn_min_down.setStyleSheet(self.get_boton_style())
        btn_min_down.clicked.connect(lambda: self.ajustar_tiempo("min", -1))

        # Botón - Segundos
        btn_seg_down = QPushButton("◄ Seg")
        btn_seg_down.setStyleSheet(self.get_boton_style())
        btn_seg_down.clicked.connect(lambda: self.ajustar_tiempo("seg", -1))

        # Botón + Minutos
        btn_min_up = QPushButton("Min ►")
        btn_min_up.setStyleSheet(self.get_boton_style())
        btn_min_up.clicked.connect(lambda: self.ajustar_tiempo("min", 1))

        # Botón + Segundos
        btn_seg_up = QPushButton("Seg ►")
        btn_seg_up.setStyleSheet(self.get_boton_style())
        btn_seg_up.clicked.connect(lambda: self.ajustar_tiempo("seg", 1))

        # Añadir botones al layout
        controles_layout.addStretch()
        controles_layout.addWidget(btn_min_down)
        controles_layout.addWidget(btn_seg_down)
        controles_layout.addSpacing(40)
        controles_layout.addWidget(btn_min_up)
        controles_layout.addWidget(btn_seg_up)
        controles_layout.addStretch()

        layout.addLayout(controles_layout)

        # 4. Botones de control
        self.btn_inicio = QPushButton("Iniciar")
        self.btn_inicio.setStyleSheet(self.get_boton_style("#2ecc71"))
        self.btn_inicio.clicked.connect(self.toggle_cronometro)
        layout.addWidget(self.btn_inicio, alignment=Qt.AlignmentFlag.AlignCenter)

        # 5. Barra de menú (simplificada)
        self.crear_menu()

        # Timer para el cronómetro
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)

    def get_boton_style(self, color="#3498db"):
        return f"""
            QPushButton {{
                font: bold 14px 'Arial';
                color: white;
                background: {color};
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                min-width: 100px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background: #2980b9;
            }}
        """

    def ajustar_tiempo(self, unidad, cambio):
        if self.corriendo:
            return

        if unidad == "min":
            self.minutos = max(0, min(59, self.minutos + cambio))
        else:
            self.segundos = max(0, min(59, self.segundos + cambio))

        self.actualizar_display()

    def actualizar_display(self):
        self.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")

    def toggle_cronometro(self):
        self.corriendo = not self.corriendo

        if self.corriendo:
            self.btn_inicio.setText("Detener")
            self.btn_inicio.setStyleSheet(self.get_boton_style("#e74c3c"))
            self.timer.start(1000)
        else:
            self.btn_inicio.setText("Iniciar")
            self.btn_inicio.setStyleSheet(self.get_boton_style("#2ecc71"))
            self.timer.stop()

    def actualizar_tiempo(self):
        if self.segundos > 0:
            self.segundos -= 1
        elif self.minutos > 0:
            self.minutos -= 1
            self.segundos = 59
        else:
            self.toggle_cronometro()

        self.actualizar_display()

    def crear_menu(self):
        barra_menu = self.menuBar()

        # Menú Archivo
        archivo_menu = barra_menu.addMenu("Archivo")
        archivo_menu.addAction("Agregar")
        archivo_menu.addAction("Eliminar")
        archivo_menu.addAction("Salir")

        # Menú Editar
        editar_menu = barra_menu.addMenu("Editar")

        # Menú Ayuda
        barra_menu.addMenu("Ayuda").addAction("Acerca de")


if __name__ == "__main__":
    app = QApplication([])
    ventana = CronometroApp()
    ventana.show()
    app.exec()