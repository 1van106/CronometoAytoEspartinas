from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QGridLayout,
    QListWidgetItem, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon
import pygame
import json

# Clase para la ventana de visualización de cronómetros
class VentanaVisualizacion(QWidget):
    def __init__(self, cronometros):
        super().__init__()
        self.setWindowTitle("Visualización de Cronómetros")
        self.resize(800, 600)
        self.init_ui(cronometros)

    def init_ui(self, cronometros):
        layout = QVBoxLayout(self)
        grid_layout = QGridLayout()  # Se usará para organizar en filas y columnas

        for i, cronometro in enumerate(cronometros):
            contenedor = QWidget()
            contenedor_layout = QVBoxLayout(contenedor)

            # Título
            nombre_label = QLabel(cronometro["nombre"])
            nombre_label.setStyleSheet("font: bold 24px Arial; color: black;")
            contenedor_layout.addWidget(nombre_label)

            # Tiempo
            tiempo_label = QLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
            tiempo_label.setStyleSheet("font: 36px Arial; color: black;")
            contenedor_layout.addWidget(tiempo_label)

            contenedor.setStyleSheet(
                "border: 3px solid black;"
                "padding: 3px;"
                "margin: 5px;"
                "background-color: #f0f0f0;"
            )

            # Agregar al grid layout (2 columnas)
            fila = i // 2
            columna = i % 2
            grid_layout.addWidget(contenedor, fila, columna)

        layout.addLayout(grid_layout)
class CronometroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ayuntamiento de Espartinas")
        self.resize(800, 600)

        self.minutos = 0  
        self.segundos = 0
        self.temporizadores = []
        self.fuente_oficial = QFont("Times New Roman", 48, QFont.Weight.Bold)
        self.cronometro_editando = None  

        pygame.mixer.init()  # Inicializar el sistema de audio
        self.sound_alarm = pygame.mixer.Sound("assets/beep-01a.wav")

        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.pagina_inicio = self.crear_pagina_inicio()
        self.pagina_agregar = self.crear_pagina_agregar()
        self.stacked_widget.addWidget(self.pagina_inicio)
        self.stacked_widget.addWidget(self.pagina_agregar)
        self.stacked_widget.setCurrentIndex(0)
        self.crear_menu()

    def crear_pagina_inicio(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        logo_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedHeight(200)

        pixmap = QPixmap("logo_espartinas.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            logo_label.setText("[LOGO]")

        layout.addWidget(logo_label)
        titulo = QLabel("AYUNTAMIENTO DE ESPARTINAS", alignment=Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(self.fuente_oficial)
        titulo.setStyleSheet("color: #1a3e72; margin: 30px; letter-spacing: 2px;")
        layout.addWidget(titulo)
        layout.addStretch()
        return pagina

    def crear_pagina_agregar(self):
        pagina = QWidget()
        layout = QHBoxLayout(pagina)
        izquierda = QVBoxLayout()

        self.titulo = QLineEdit("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.titulo.setPlaceholderText("Título de la Intervención")  
        self.titulo.setStyleSheet("font: bold 18px Arial; color: #2c3e50; padding: 10px; border: 3px solid black; background: #ecf0f1;")
        izquierda.addWidget(self.titulo)

        self.display = QLabel("00:00", alignment=Qt.AlignmentFlag.AlignCenter)
        self.display.setStyleSheet("font: bold 68px Arial; color: #bdc3c7; background: white;  border: 3px solid black;")
        izquierda.addWidget(self.display)

        controles_layout = QHBoxLayout()

        btn_min_down = QPushButton("◄", clicked=lambda: self.ajustar_tiempo("min", -1))
        btn_seg_down = QPushButton("◄", clicked=lambda: self.ajustar_tiempo("seg", -1))
        btn_min_up = QPushButton("►", clicked=lambda: self.ajustar_tiempo("min", 1))
        btn_seg_up = QPushButton("►", clicked=lambda: self.ajustar_tiempo("seg", 1))

        for btn in [btn_min_down, btn_seg_down, btn_min_up, btn_seg_up]:
            btn.setStyleSheet(self.get_boton_style())
            controles_layout.addWidget(btn)

        izquierda.addLayout(controles_layout)
        self.btn_agregar = QPushButton("Agregar", clicked=self.agregar_temporizador)
        self.btn_agregar.setStyleSheet(self.get_boton_style("#3498db"))
        izquierda.addWidget(self.btn_agregar, alignment=Qt.AlignmentFlag.AlignCenter)

        derecha = QVBoxLayout()
        self.lista_temporizadores = QListWidget()
        derecha.addWidget(self.lista_temporizadores)

        layout.addLayout(izquierda)
        layout.addLayout(derecha)
        return pagina

    def crear_menu(self):
        barra_menu = self.menuBar()

        # Menú Admin
        archivo_menu = barra_menu.addMenu("Admin")

        # Submenú Pleno Ordinario
        archivo_menu.addAction("Pleno Ordinario").triggered.connect(self.mostrar_agregar)
    
        # Submenú Pleno Extraordinario
        archivo_menu.addAction("Pleno Extraordinario").triggered.connect(self.mostrar_agregar)

        archivo_menu.addAction("Salir").triggered.connect(QApplication.quit)

        # Menú Abrir
        abrir_menu = barra_menu.addMenu("Abrir")
        abrir_menu.addAction("Abrir Pleno Ordinario").triggered.connect(lambda: self.mostrar_pleno("ordinario"))
        abrir_menu.addAction("Abrir Pleno Extraordinario").triggered.connect(lambda: self.mostrar_pleno("extraordinario"))

    def mostrar_agregar(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def guardar_datos(self):
      datos = []
      for cronometro in self.temporizadores:
        datos.append({
            "nombre": cronometro["nombre"],
            "minutos": cronometro["minutos"],
            "segundos": cronometro["segundos"]
        })

      with open("cronometros.json", "w") as file:
        json.dump(datos, file, indent=4)

    def cargar_datos(self, tipo):
      try:
        with open("cronometros.json", "r") as file:
            datos = json.load(file)
            return datos  # Devuelve la lista de cronómetros guardados
      except (FileNotFoundError, json.JSONDecodeError):
        return []  # Si el archivo no existe o hay error, devuelve lista vacía

    def mostrar_abrir(self):
      self.stacked_widget.setCurrentIndex(2)  # Suponiendo que la pantalla de "Abrir" sea el índice 2

      # Limpiar la pantalla y agregar cronómetros solo para visualización
      self.pagina_abrir = QWidget()
      layout_abrir = QVBoxLayout(self.pagina_abrir)
      for cronometro in self.temporizadores:
        contenedor = cronometro["contenedor"]
        # Cambiar los cronómetros para que solo se muestren sin botones
        layout_abrir.addWidget(contenedor)

      self.stacked_widget.addWidget(self.pagina_abrir)

    def agregar_temporizador(self):
        nombre = self.titulo.text().strip()
        if not nombre or (self.minutos == 0 and self.segundos == 0):
            QMessageBox.warning(self, "Error", "El cronómetro debe tener un título y un tiempo mayor a 00:00.")
            return

        # Crear contenedor para el cronómetro (esto debe ser siempre, tanto para agregar como para editar)
        contenedor = QWidget()
        contenedor_layout = QVBoxLayout(contenedor)
        
        # Título grande
        nombre_label = QLabel(nombre, alignment=Qt.AlignmentFlag.AlignCenter)
        nombre_label.setStyleSheet("font: bold 24px Arial; color: black;")
        contenedor_layout.addWidget(nombre_label)

        # Tiempo grande
        tiempo_label = QLabel(f"{self.minutos:02d}:{self.segundos:02d}", alignment=Qt.AlignmentFlag.AlignCenter)
        tiempo_label.setStyleSheet("font: 36px Arial; color: black; border: 3px solid black;")
        contenedor_layout.addWidget(tiempo_label)

        contenedor.setStyleSheet(
        "border: 2px solid black;"  # Borde azul para distinguir los contenedores
        "padding: 3px;"  # Espaciado interno más pequeño
        "margin-bottom: 5px;"  # Menos separación entre cronómetros
        "background-color: #f0f0f0;"  # Fondo gris claro para mejor visualización
        )  

        # Botones de play y reset
        botones_layout = QHBoxLayout()
        btn_play = QPushButton("Play", clicked=lambda: self.toggle_cronometro(contenedor, tiempo_label))
        btn_play.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        btn_reset = QPushButton("Reset", clicked=lambda: self.reset_cronometro(tiempo_label))
        btn_reset.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        botones_layout.addWidget(btn_play)
        botones_layout.addWidget(btn_reset)

        # Agregar icono de editar (lápiz)
        btn_editar = QPushButton()
        btn_editar.setIcon(QIcon("assets/lapiz.png"))
        btn_editar.clicked.connect(lambda: self.editar_temporizador(contenedor))
        botones_layout.addWidget(btn_editar)

        # Agregar icono de eliminar (papelera)
        btn_eliminar = QPushButton()
        btn_eliminar.setIcon(QIcon("assets/papelera.png"))
        btn_eliminar.clicked.connect(lambda: self.eliminar_temporizador(contenedor))
        botones_layout.addWidget(btn_eliminar)
        contenedor_layout.addLayout(botones_layout)

        # Si estamos editando, actualizamos el cronómetro
        if self.cronometro_editando:
            cronometro = self.cronometro_editando
            cronometro["nombre"] = nombre
            cronometro["minutos"] = self.minutos
            cronometro["segundos"] = self.segundos
            cronometro["tiempo_label"].setText(f"{self.minutos:02d}:{self.segundos:02d}")
            cronometro["contenedor"].findChild(QLabel).setText(nombre)  # Actualizar el título
            self.cronometro_editando = None  # Limpiar la referencia de edición
        else:
            # Si no estamos editando, agregamos un nuevo cronómetro
            self.temporizadores.append({
                "nombre": nombre, "minutos": self.minutos, "segundos": self.segundos, 
                "corriendo": False, "timer": None, "contenedor": contenedor, "tiempo_label": tiempo_label
            })
            item = QListWidgetItem()
            item.setSizeHint(contenedor.sizeHint())
            self.lista_temporizadores.addItem(item)
            self.lista_temporizadores.setItemWidget(item, contenedor)

            # Guardar los datos en JSON después de agregar o editar un cronómetro
            self.guardar_datos()

            self.titulo.clear()
            self.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")

    def reset_cronometro(self, tiempo_label):
        # Restaurar el cronómetro a su tiempo editado
        tiempo_label.setText(f"{self.minutos:02d}:{self.segundos:02d}")

    def toggle_cronometro(self, contenedor, tiempo_label):
        # Buscar el cronómetro en la lista
        cronometro = next((c for c in self.temporizadores if c["contenedor"] == contenedor), None)
        if cronometro:
            if cronometro["corriendo"]:
                self.detener_cronometro(cronometro)
            else:
                self.iniciar_cronometro(cronometro, tiempo_label)

    def iniciar_cronometro(self, cronometro, tiempo_label):
        # Iniciar cronómetro hacia atrás
        cronometro["corriendo"] = True
        cronometro["timer"] = QTimer(self)
        cronometro["timer"].timeout.connect(lambda: self.actualizar_tiempo(cronometro, tiempo_label))
        cronometro["timer"].start(1000)

    def detener_cronometro(self, cronometro):
        # Detener cronómetro
        cronometro["corriendo"] = False
        cronometro["timer"].stop()

    def editar_temporizador(self, contenedor):
        # Buscar el cronómetro en la lista
        cronometro = next((c for c in self.temporizadores if c["contenedor"] == contenedor), None)
        if cronometro:
            self.cronometro_editando = cronometro  # Guardar el cronómetro a editar
            self.titulo.setText(cronometro["nombre"])
            self.minutos = cronometro["minutos"]
            self.segundos = cronometro["segundos"]
            self.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")
            self.stacked_widget.setCurrentIndex(1)  # Mostrar la pantalla de agregar

    def eliminar_temporizador(self, contenedor):
       # Buscar el cronómetro en la lista
       cronometro = next((c for c in self.temporizadores if c["contenedor"] == contenedor), None)
       if cronometro:
        # Buscar el item correspondiente en la lista mediante la referencia del widget
        item = None
        for i in range(self.lista_temporizadores.count()):
            list_item = self.lista_temporizadores.item(i)
            widget = self.lista_temporizadores.itemWidget(list_item)
            if widget == contenedor:
                item = list_item
                break

        if item:
            row = self.lista_temporizadores.row(item)  # Obtener la fila del item
            self.lista_temporizadores.takeItem(row)  # Eliminar el item de la lista
            self.temporizadores.remove(cronometro) 
    
    def actualizar_visualizacion(self):
      # Actualizar la vista de los cronómetros
      for i in range(self.lista_temporizadores.count()):
        item = self.lista_temporizadores.item(i)
        widget = self.lista_temporizadores.itemWidget(item)
        nombre_label = widget.findChild(QLabel)
        tiempo_label = widget.findChild(QLabel, "tiempo_label")  # Usamos un identificador para obtener el tiempo
        if tiempo_label:
            # Buscar el cronómetro correspondiente
            cronometro = next((c for c in self.temporizadores if c["contenedor"] == widget), None)
            if cronometro:
                tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")
    def actualizar_tiempo(self, cronometro, tiempo_label):
        # Reducir el tiempo del cronómetro
        if cronometro["segundos"] > 0:
            cronometro["segundos"] -= 1
        elif cronometro["minutos"] > 0:
            cronometro["minutos"] -= 1
            cronometro["segundos"] = 59
        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")

    def ajustar_tiempo(self, tipo, valor):
        if tipo == "min":
            self.minutos = max(0, self.minutos + valor)  # No permitir minutos negativos
        elif tipo == "seg":
            self.segundos = max(0, self.segundos + valor)  # No permitir segundos negativos

        # Actualizar la visualización de la pantalla de edición
        self.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")

    def get_boton_style(self, color="#3498db"):
        return f"font: bold 20px Arial; color: white; padding: 10px; border-radius: 5px; background-color: {color};"
    
   

    def crear_pagina_visualizacion(self, cronometros):
      pagina = QWidget()
      layout = QVBoxLayout(pagina)

      for cronometro in cronometros:
        contenedor = QWidget()
        contenedor_layout = QVBoxLayout(contenedor)
        
        # Título grande
        nombre_label = QLabel(cronometro["nombre"], alignment=Qt.AlignmentFlag.AlignCenter)
        nombre_label.setStyleSheet("font: bold 24px Arial; color: black;")
        contenedor_layout.addWidget(nombre_label)

        # Tiempo grande
        tiempo_label = QLabel(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}", alignment=Qt.AlignmentFlag.AlignCenter)
        tiempo_label.setStyleSheet("font: 36px Arial; color: #bdc3c7; border: 3px solid black;")
        contenedor_layout.addWidget(tiempo_label)

        contenedor.setStyleSheet(
            "border: 2px solid black;"
            "padding: 3px;"
            "margin-bottom: 5px;"
            "background-color: #f0f0f0;"
        )

        layout.addWidget(contenedor)

      return pagina
    
    def mostrar_pleno(self, tipo):
      cronometros = self.cargar_datos(tipo)
      pagina_visualizacion = self.crear_pagina_visualizacion(cronometros)

      self.ventana_visualizacion = VentanaVisualizacion(cronometros)
      self.ventana_visualizacion.show()
      


if __name__ == "__main__":
    app = QApplication([])
    window = CronometroApp()
    window.show()
    app.exec()


