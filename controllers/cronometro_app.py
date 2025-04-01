import os
import pygame
from PyQt6.QtWidgets import (QMainWindow, QMenuBar, QMenu, QStackedWidget,
                             QMessageBox, QApplication)
from PyQt6.QtGui import QFont, QGuiApplication
from PyQt6.QtGui import QIcon

from models.almacenamiento import Almacenamiento
from models.cronometro import Cronometro
from views.vista_inicio import VistaInicio
from views.vista_dividida import VistaDividida
from views.visualizacion import VentanaVisualizacion
from views.ventana_controles import VentanaControles


class CronometroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configurar_ventana()
        self.inicializar_estados()
        self.inicializar_audio()
        self.init_ui()

    def configurar_ventana(self):
        self.setWindowTitle("Ayuntamiento de Espartinas")
        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)

    def inicializar_estados(self):
        self.minutos = 0
        self.segundos = 0
        self.temporizadores = []
        self.cronometro_editando = None
        self.tipo_pleno_actual = None
        self.fuente_oficial = QFont("Times New Roman", 48, QFont.Weight.Bold)

    def inicializar_audio(self):
        pygame.mixer.init()
        self.sound_alarm = pygame.mixer.Sound("assets/beep-01a.wav") if os.path.exists("assets/beep-01a.wav") else None

    def init_ui(self):
        self.stacked_main = QStackedWidget()
        self.setCentralWidget(self.stacked_main)

        # Configurar vistas
        self.pagina_inicio = VistaInicio(self.fuente_oficial)
        self.pagina_dividida = VistaDividida()

        # Conectar señales de la vista dividida
        self.conectar_señales_vista_dividida()

        # Añadir vistas al stacked widget
        self.stacked_main.addWidget(self.pagina_inicio)
        self.stacked_main.addWidget(self.pagina_dividida)
        self.stacked_main.setCurrentIndex(0)

        # Configurar menú
        self.crear_menu()

    def conectar_señales_vista_dividida(self):
        """Conecta todos los eventos de la vista dividida"""
        vista = self.pagina_dividida

        # Botones de ajuste de tiempo
        vista.btn_min_down.clicked.connect(lambda: self.ajustar_tiempo("min", -1))
        vista.btn_seg_down.clicked.connect(lambda: self.ajustar_tiempo("seg", -1))
        vista.btn_min_up.clicked.connect(lambda: self.ajustar_tiempo("min", 1))
        vista.btn_seg_up.clicked.connect(lambda: self.ajustar_tiempo("seg", 1))

        # Botón principal
        vista.btn_agregar.clicked.connect(self.accion_principal_temporizador)

    def crear_menu(self):
        barra_menu = self.menuBar()

        # Menú Admin
        admin_menu = barra_menu.addMenu("Admin")
        admin_menu.addAction("Pleno Ordinario").triggered.connect(lambda: self.mostrar_editor("ordinario"))
        admin_menu.addAction("Pleno Extraordinario").triggered.connect(lambda: self.mostrar_editor("extraordinario"))

        # Menú Visualización
        visualizacion_menu = barra_menu.addMenu("Visualización")
        visualizacion_menu.addAction("Ver Pleno Ordinario").triggered.connect(lambda: self.mostrar_pleno("ordinario"))
        visualizacion_menu.addAction("Ver Pleno Extraordinario").triggered.connect(
            lambda: self.mostrar_pleno("extraordinario"))

        # Opción Salir
        barra_menu.addAction("Salir").triggered.connect(QApplication.instance().quit)

    def mostrar_editor(self, tipo_pleno):
        """Cambia a la vista dividida con el cronómetro"""
        self.stacked_main.setCurrentIndex(1)
        self.tipo_pleno_actual = tipo_pleno
        self.cargar_temporizadores()

    def mostrar_pleno(self, tipo_pleno):
        cronometros = Almacenamiento.cargar_cronometros(tipo_pleno)
    
        if cronometros:
          self.ventana_visualizacion = VentanaVisualizacion(cronometros, tipo_pleno)
          self.ventana_visualizacion.show()

          self.ventana_controles = VentanaControles(cronometros, tipo_pleno)
          self.ventana_controles.tiempo_actualizado.connect(self.ventana_visualizacion.actualizar_tiempo)  # Conectar señal
          self.ventana_controles.show()
        else:
          print(f"No se encontraron cronómetros para el tipo de pleno: {tipo_pleno}")


    def cargar_temporizadores(self):
        """Carga los temporizadores desde el archivo"""
        datos = Almacenamiento.cargar_cronometros(self.tipo_pleno_actual)
        self.temporizadores = []
        self.pagina_dividida.lista_temporizadores.clear()

        for item in datos:
            self.agregar_temporizador_desde_datos(item["nombre"], item["minutos"], item["segundos"])

    def agregar_temporizador_desde_datos(self, nombre, minutos, segundos):
        """Agrega un temporizador desde datos existentes"""
        cronometro = Cronometro(nombre, minutos, segundos)
        self.temporizadores.append(cronometro)
        self.pagina_dividida.agregar_temporizador_ui(cronometro, self)

    def accion_principal_temporizador(self):
        """Maneja el botón principal (Agregar/Actualizar)"""
        if self.cronometro_editando:
            self.actualizar_temporizador()
        else:
            self.agregar_temporizador()

    def agregar_temporizador(self):
        """Agrega un nuevo temporizador"""
        nombre = self.pagina_dividida.titulo.text().strip()
        if not nombre or (self.minutos == 0 and self.segundos == 0):
            QMessageBox.warning(self, "Error", "El cronómetro debe tener un título y un tiempo mayor a 00:00.")
            return

        cronometro = Cronometro(nombre, self.minutos, self.segundos)
        self.temporizadores.append(cronometro)
        self.pagina_dividida.agregar_temporizador_ui(cronometro, self)

        Almacenamiento.guardar_cronometros(self.tipo_pleno_actual, self.temporizadores)
        self.resetear_controles()

    def actualizar_temporizador(self):
        """Actualiza un temporizador existente"""
        if not self.cronometro_editando:
            return

        nombre = self.pagina_dividida.titulo.text().strip()
        if not nombre or (self.minutos == 0 and self.segundos == 0):
            QMessageBox.warning(self, "Error", "El cronómetro debe tener un título y un tiempo mayor a 00:00.")
            return

        # Actualizar el cronómetro
        self.cronometro_editando.nombre = nombre
        self.cronometro_editando.minutos = self.minutos
        self.cronometro_editando.segundos = self.segundos

        # Actualizar UI
        self.pagina_dividida.actualizar_temporizador_ui(self.cronometro_editando)

        # Guardar y limpiar
        Almacenamiento.guardar_cronometros(self.tipo_pleno_actual, self.temporizadores)
        self.resetear_edicion()

    def editar_temporizador(self, cronometro):
        """Prepara la edición de un temporizador"""
        self.cronometro_editando = cronometro
        self.pagina_dividida.titulo.setText(cronometro.nombre)
        self.minutos = cronometro.minutos
        self.segundos = cronometro.segundos
        self.pagina_dividida.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")
        self.pagina_dividida.btn_agregar.setText("Actualizar")
        self.stacked_main.setCurrentIndex(1)

    def eliminar_temporizador(self, cronometro):
        """Elimina un temporizador"""
        # Eliminar el ítem de la lista gráfica
        for i in range(self.pagina_dividida.lista_temporizadores.count()):
            item = self.pagina_dividida.lista_temporizadores.item(i)
            widget = self.pagina_dividida.lista_temporizadores.itemWidget(item)
            if widget == cronometro.widget:
                self.pagina_dividida.lista_temporizadores.takeItem(i)
                break

        # Eliminar de la lista de temporizadores
        if cronometro in self.temporizadores:
            self.temporizadores.remove(cronometro)

        Almacenamiento.guardar_cronometros(self.tipo_pleno_actual, self.temporizadores)

    def ajustar_tiempo(self, tipo, valor):
        """Ajusta el tiempo mostrado en el editor"""
        if tipo == "min":
            self.minutos = max(0, min(59, self.minutos + valor))
        else:
            self.segundos = max(0, min(59, self.segundos + valor))

        self.pagina_dividida.display.setText(f"{self.minutos:02d}:{self.segundos:02d}")

    def resetear_controles(self):
        """Resetea los controles a sus valores por defecto"""
        self.pagina_dividida.titulo.clear()
        self.minutos = 0
        self.segundos = 0
        self.pagina_dividida.display.setText("00:00")

    def resetear_edicion(self):
        """Termina el modo de edición"""
        self.resetear_controles()
        self.cronometro_editando = None
        self.pagina_dividida.btn_agregar.setText("Agregar")