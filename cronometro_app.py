import os
import sys
import json
import pygame
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QGridLayout, QListWidgetItem, QStackedWidget,
    QMessageBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QGuiApplication, QIcon

from visualizacion import VentanaVisualizacion

class CronometroApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de pantalla completa
        self.setWindowTitle("Ayuntamiento de Espartinas")
        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        

        # Variables de estado
        self.minutos = 0
        self.segundos = 0
        self.corriendo = False
        self.temporizadores = []
        self.cronometro_editando = None

        # Inicializar sistema de audio
        pygame.mixer.init()
        self.sound_alarm = pygame.mixer.Sound("assets/beep-01a.wav") if os.path.exists("assets/beep-01a.wav") else None

        # Fuentes
        self.fuente_oficial = QFont("Times New Roman", 48, QFont.Weight.Bold)
        self.fuente_secundaria = QFont("Arial", 14)

        # Crear interfaz
        self.init_ui()

    def init_ui(self):
        # Widget principal con stacked layout
        self.stacked_main = QStackedWidget()
        self.setCentralWidget(self.stacked_main)

        # 1. PANTALLA INICIAL (completa)
        self.pagina_inicio = self.crear_pagina_inicio()

        # 2. PANTALLA DIVIDIDA (cronómetro + lista)
        self.pagina_dividida = self.crear_pagina_dividida()

        self.stacked_main.addWidget(self.pagina_inicio)
        self.stacked_main.addWidget(self.pagina_dividida)
        self.stacked_main.setCurrentIndex(0)

        # Menú
        self.crear_menu()

    def crear_pagina_inicio(self):
        pagina = QWidget()
        layout = QVBoxLayout()
        pagina.setLayout(layout)

        # Añadir espacio flexible arriba para centrar verticalmente
        layout.addStretch(1)

        # Título con menos margen superior
        titulo = QLabel("AYUNTAMIENTO DE ESPARTINAS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(self.fuente_oficial)
        titulo.setStyleSheet("""
            QLabel {
                color: blue;
                margin-bottom: 30px;
            }
        """)
        layout.addWidget(titulo)

        # Logo más grande y centrado
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = ".venv/image/logo_espartinas.png" if os.path.exists(
            ".venv/image/logo_espartinas.png") else "logo_espartinas.png"
        pixmap = QPixmap(logo_path)

        if not pixmap.isNull():
            pixmap = pixmap.scaled(450, 450,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setFixedSize(pixmap.size())
        else:
            logo_label.setText("[LOGO AYUNTAMIENTO]")
            logo_label.setStyleSheet("""
                QLabel {
                    color: white; 
                    font-size: 24px;
                    background-color: #cccccc;
                    border: 2px dashed #999999;
                    min-width: 450px;
                    min-height: 450px;
                }
            """)

        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir espacio flexible abajo para balancear el centrado
        layout.addStretch(1)

        return pagina

    def crear_pagina_dividida(self):
        pagina = QWidget()
        layout = QHBoxLayout()
        pagina.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- MITAD IZQUIERDA: Cronómetro ---
        self.left_frame = QFrame()
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout()
        self.left_frame.setLayout(left_layout)

        # Añadir espacio flexible arriba para centrar verticalmente
        left_layout.addStretch(1)

        # Editor de cronómetro
        self.titulo = QLineEdit("")
        self.titulo.setPlaceholderText("Título de la Intervención")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("""
            QLineEdit {
                font: bold 18px 'Arial';
                color: #2c3e50;
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin: 10px 50px;
                background: #ecf0f1;
            }
        """)
        left_layout.addWidget(self.titulo)

        self.display = QLabel("00:00")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setStyleSheet("""
            QLabel {
                font: bold 60px 'Arial';
                color: #3498db;
                margin: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 12px;
                border: 3px solid #bdc3c7;
            }
        """)
        left_layout.addWidget(self.display)

        controles_layout = QHBoxLayout()
        btn_min_down = QPushButton("◄ Min")
        btn_min_down.setStyleSheet(self.get_boton_style())
        btn_min_down.clicked.connect(lambda: self.ajustar_tiempo("min", -1))

        btn_seg_down = QPushButton("◄ Seg")
        btn_seg_down.setStyleSheet(self.get_boton_style())
        btn_seg_down.clicked.connect(lambda: self.ajustar_tiempo("seg", -1))

        btn_min_up = QPushButton("Min ►")
        btn_min_up.setStyleSheet(self.get_boton_style())
        btn_min_up.clicked.connect(lambda: self.ajustar_tiempo("min", 1))

        btn_seg_up = QPushButton("Seg ►")
        btn_seg_up.setStyleSheet(self.get_boton_style())
        btn_seg_up.clicked.connect(lambda: self.ajustar_tiempo("seg", 1))

        controles_layout.addStretch()
        controles_layout.addWidget(btn_min_down)
        controles_layout.addWidget(btn_seg_down)
        controles_layout.addSpacing(20)
        controles_layout.addWidget(btn_min_up)
        controles_layout.addWidget(btn_seg_up)
        controles_layout.addStretch()

        left_layout.addLayout(controles_layout)

        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.setStyleSheet(self.get_boton_style("#2ecc71"))
        self.btn_agregar.clicked.connect(self.agregar_temporizador)
        left_layout.addWidget(self.btn_agregar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir espacio flexible abajo para balancear el centrado
        left_layout.addStretch(1)

        # --- MITAD DERECHA: Lista de temporizadores ---
        self.right_frame = QFrame()
        self.right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_frame.setStyleSheet("background-color: #f8f9fa;")

        # Layout para la lista de temporizadores
        self.right_layout = QVBoxLayout()
        self.right_frame.setLayout(self.right_layout)

        self.lista_temporizadores = QListWidget()
        self.right_layout.addWidget(self.lista_temporizadores)

        # Añadir frames al layout principal
        layout.addWidget(self.left_frame, stretch=1)
        layout.addWidget(self.right_frame, stretch=1)

        return pagina

    def crear_menu(self):
        barra_menu = self.menuBar()

        # Menú Admin
        admin_menu = barra_menu.addMenu("Admin")

        # Submenú Pleno Ordinario
        admin_menu.addAction("Pleno Ordinario").triggered.connect(lambda: self.mostrar_editor("ordinario"))

        # Submenú Pleno Extraordinario
        admin_menu.addAction("Pleno Extraordinario").triggered.connect(lambda: self.mostrar_editor("extraordinario"))

        # Menú Visualización
        visualizacion_menu = barra_menu.addMenu("Visualización")
        visualizacion_menu.addAction("Ver Pleno Ordinario").triggered.connect(lambda: self.mostrar_pleno("ordinario"))
        visualizacion_menu.addAction("Ver Pleno Extraordinario").triggered.connect(lambda: self.mostrar_pleno("extraordinario"))

        # Opción Salir
        barra_menu.addAction("Salir").triggered.connect(QApplication.instance().quit)


    def mostrar_editor(self, tipo_pleno):
        """Cambia a la vista dividida con el cronómetro"""
        self.stacked_main.setCurrentIndex(1)
        self.tipo_pleno_actual = tipo_pleno
        self.cargar_datos(tipo_pleno)

    def mostrar_pleno(self, tipo_pleno):
        cronometros = self.cargar_datos(tipo_pleno)
        print(f"Cronómetros cargados: {cronometros}")  

        if cronometros:
          self.ventana_visualizacion = VentanaVisualizacion(cronometros, tipo_pleno)  # ✅ Se pasa tipo_pleno correctamente
          self.ventana_visualizacion.show()
        else:
          print("No se encontraron cronómetros para mostrar.")

    def guardar_datos(self):
      datos = []
      for cronometro in self.temporizadores:
        datos.append({
            "nombre": cronometro["nombre"],
            "minutos": cronometro["minutos"],
            "segundos": cronometro["segundos"]
        })

      print(f"Guardando datos: {datos}")  # Agregar esta línea para debug

      nombre_archivo = f"cronometros_{self.tipo_pleno_actual}.json"
      with open(nombre_archivo, "w") as file:
        json.dump(datos, file, indent=4)

    def cargar_datos(self, tipo_pleno):
        nombre_archivo = f"cronometros_{tipo_pleno}.json"
        try:
            with open(nombre_archivo, "r") as file:
                datos = json.load(file)
                self.temporizadores = []
                self.lista_temporizadores.clear()

                for item in datos:
                    self.agregar_temporizador_desde_datos(item["nombre"], item["minutos"], item["segundos"])

                return datos
        except (FileNotFoundError, json.JSONDecodeError):
            self.temporizadores = []
            self.lista_temporizadores.clear()
            return []

    def agregar_temporizador_desde_datos(self, nombre, minutos, segundos):
        contenedor = QWidget()
        contenedor_layout = QVBoxLayout(contenedor)

        # Título grande
        nombre_label = QLabel(nombre, alignment=Qt.AlignmentFlag.AlignCenter)
        nombre_label.setStyleSheet("font: bold 24px Arial; color: black;")
        contenedor_layout.addWidget(nombre_label)

        # Tiempo grande
        tiempo_label = QLabel(f"{minutos:02d}:{segundos:02d}", alignment=Qt.AlignmentFlag.AlignCenter)
        tiempo_label.setStyleSheet("font: 36px Arial; color: black; border: 3px solid black;")
        contenedor_layout.addWidget(tiempo_label)

        contenedor.setStyleSheet(
            "border: 2px solid black;"
            "padding: 3px;"
            "margin-bottom: 5px;"
            "background-color: #f0f0f0;"
        )

        # Botones de play y reset
        botones_layout = QHBoxLayout()
        btn_play = QPushButton("Play")
        btn_play.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        btn_play.clicked.connect(lambda: self.toggle_cronometro(contenedor, tiempo_label))

        btn_reset = QPushButton("Reset")
        btn_reset.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        btn_reset.clicked.connect(lambda: self.reset_cronometro(contenedor, tiempo_label, minutos, segundos))

        # Agregar icono de editar (lápiz)
        btn_editar = QPushButton()
        btn_editar.setIcon(QIcon("assets/lapiz.png")) if os.path.exists("assets/lapiz.png") else btn_editar.setText(
            "Editar")
        btn_editar.clicked.connect(lambda: self.editar_temporizador(contenedor))

        # Agregar icono de eliminar (papelera)
        btn_eliminar = QPushButton()
        btn_eliminar.setIcon(QIcon("assets/papelera.png")) if os.path.exists(
            "assets/papelera.png") else btn_eliminar.setText("Eliminar")
        btn_eliminar.clicked.connect(lambda: self.eliminar_temporizador(contenedor))

        botones_layout.addWidget(btn_play)
        botones_layout.addWidget(btn_reset)
        botones_layout.addWidget(btn_editar)
        botones_layout.addWidget(btn_eliminar)
        contenedor_layout.addLayout(botones_layout)

        # Agregar a la lista de temporizadores
        self.temporizadores.append({
            "nombre": nombre,
            "minutos": minutos,
            "segundos": segundos,
            "corriendo": False,
            "timer": None,
            "contenedor": contenedor,
            "tiempo_label": tiempo_label
        })

        item = QListWidgetItem()
        item.setSizeHint(contenedor.sizeHint())
        self.lista_temporizadores.addItem(item)
        self.lista_temporizadores.setItemWidget(item, contenedor)

    def agregar_temporizador(self):
        nombre = self.titulo.text().strip()
        if not nombre or (self.minutos == 0 and self.segundos == 0):
            QMessageBox.warning(self, "Error", "El cronómetro debe tener un título y un tiempo mayor a 00:00.")
            return

        self.agregar_temporizador_desde_datos(nombre, self.minutos, self.segundos)
        self.guardar_datos()

        # Limpiar campos después de agregar
        self.titulo.clear()
        self.minutos = 0
        self.segundos = 0
        self.display.setText("00:00")

    def reset_cronometro(self, contenedor, tiempo_label, minutos_originales, segundos_originales):
        # Buscar el cronómetro en la lista
        cronometro = next((c for c in self.temporizadores if c["contenedor"] == contenedor), None)
        if cronometro:
            if cronometro["corriendo"]:
                self.detener_cronometro(cronometro)

            cronometro["minutos"] = minutos_originales
            cronometro["segundos"] = segundos_originales
            tiempo_label.setText(f"{minutos_originales:02d}:{segundos_originales:02d}")

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
        if cronometro["timer"]:
            cronometro["timer"].stop()

    def editar_temporizador(self, contenedor):
        # Buscar el cronómetro en la lista
        cronometro = next((c for c in self.temporizadores if c["contenedor"] == contenedor), None)
        if cronometro:
            self.cronometro_editando = cronometro
            self.titulo.setText(cronometro["nombre"])
            self.minutos = cronometro["minutos"]
            self.segundos = cronometro["segundos"]
            self.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")
            self.stacked_main.setCurrentIndex(1)
             # El botón de guardar edita en lugar de agregar uno nuevo
            self.btn_agregar.setText("Actualizar")  
            self.btn_agregar.clicked.disconnect()  # Desconectar cualquier señal previa
            self.btn_agregar.clicked.connect(self.actualizar_temporizador)
            self.stacked_main.setCurrentIndex(1)
    
    def actualizar_temporizador(self):
        if not self.cronometro_editando:
           return
    
        nombre = self.titulo.text().strip()
        if not nombre or (self.minutos == 0 and self.segundos == 0):
           QMessageBox.warning(self, "Error", "El cronómetro debe tener un título y un tiempo mayor a 00:00.")
           return
    
        # Actualizar los valores del cronómetro editado
        self.cronometro_editando["nombre"] = nombre
        self.cronometro_editando["minutos"] = self.minutos
        self.cronometro_editando["segundos"] = self.segundos
    
        # Actualizar la UI
        self.cronometro_editando["tiempo_label"].setText(f"{self.minutos:02d}:{self.segundos:02d}")

        # Buscar el widget correspondiente en la lista y actualizarlo
        for i in range(self.lista_temporizadores.count()):
          item = self.lista_temporizadores.item(i)
          widget = self.lista_temporizadores.itemWidget(item)
        
          if widget == self.cronometro_editando["contenedor"]:
            # Encontrado, actualizar el nombre y el tiempo
            labels = widget.findChildren(QLabel)
            if labels:
                labels[0].setText(nombre)  # Título
                labels[1].setText(f"{self.minutos:02d}:{self.segundos:02d}")  # Tiempo
            
            break

        # Guardar los cambios en el JSON
        self.guardar_datos()

        # Regresar a la lista de cronómetros
        self.stacked_main.setCurrentIndex(1)

        # Restaurar el botón de guardar a su función original
        self.btn_agregar.setText("Agregar")
        self.btn_agregar.clicked.disconnect()
        self.btn_agregar.clicked.connect(self.agregar_temporizador)

        # Limpiar la referencia al cronómetro editado
        self.cronometro_editando = None
        self.guardar_datos()

    def eliminar_temporizador(self, contenedor):
        # Buscar el cronómetro en la lista
        cronometro = next((c for c in self.temporizadores if c["contenedor"] == contenedor), None)
        if cronometro:
            # Detener el temporizador si está corriendo
            if cronometro["corriendo"]:
                self.detener_cronometro(cronometro)

            # Buscar y eliminar el item de la lista
            for i in range(self.lista_temporizadores.count()):
                item = self.lista_temporizadores.item(i)
                if self.lista_temporizadores.itemWidget(item) == contenedor:
                    self.lista_temporizadores.takeItem(i)
                    break

            # Eliminar de la lista de temporizadores
            self.temporizadores.remove(cronometro)
            self.guardar_datos()

    def actualizar_tiempo(self, cronometro, tiempo_label):
        # Reducir el tiempo del cronómetro
        if cronometro["segundos"] > 0:
            cronometro["segundos"] -= 1
        elif cronometro["minutos"] > 0:
            cronometro["minutos"] -= 1
            cronometro["segundos"] = 59
        else:
            self.detener_cronometro(cronometro)
            if self.sound_alarm:
                self.sound_alarm.play()
            return

        tiempo_label.setText(f"{cronometro['minutos']:02d}:{cronometro['segundos']:02d}")

    def ajustar_tiempo(self, tipo, valor):
        if tipo == "min":
            self.minutos = max(0, min(59, self.minutos + valor))
        else:
            self.segundos = max(0, min(59, self.segundos + valor))

        self.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")

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
