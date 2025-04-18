import os
import pygame
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QMenuBar, QMenu, QStackedWidget,
                             QMessageBox, QApplication, QWidgetAction, QLabel,
    QWidget, QHBoxLayout)
from PyQt6.QtGui import QFont, QGuiApplication, QAction
from PyQt6.QtGui import QIcon, QPixmap



from models.almacenamiento import Almacenamiento
from models.cronometro import Cronometro
from views.vista_inicio import VistaInicio
from views.vista_dividida import VistaDividida
from views.visualizacion import VentanaVisualizacion
from views.ventana_controles import VentanaControles
from views.guia import VentanaGuia
from views.info import VentanaInfo


class CronometroApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.configurar_ventana()
        self.inicializar_estados()
        self.inicializar_audio()
        self.init_ui()

########################################################################################################

    def configurar_ventana(self):
        self.setWindowTitle("Ayuntamiento de Espartinas")
        self.setWindowIcon(QIcon("assets/logo_espartinas_copy1.png"))
        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.resize(1200, 800)

########################################################################################################

    def inicializar_estados(self):
        self.minutos = 0
        self.segundos = 0
        self.temporizadores = []
        self.cronometro_editando = None
        self.logo=None
        self.logo_path=None
        self.tipo_pleno_actual = None
        self.fuente_oficial = QFont("Times New Roman", 48, QFont.Weight.Bold)

########################################################################################################

    def inicializar_audio(self):
        pygame.mixer.init()
        self.sound_alarm = pygame.mixer.Sound("assets/beep-01a.wav") if os.path.exists("assets/beep-01a.wav") else None

########################################################################################################

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

########################################################################################################

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

        # ⬇️ Nueva conexión para detectar reordenamiento manual
        vista.lista_temporizadores.model().rowsMoved.connect(self.reordenar_temporizadores)


########################################################################################################

    def crear_menu(self):
        barra_menu = self.menuBar()

        # Configuración clave para mostrar texto
        barra_menu.setNativeMenuBar(False)  # Desactiva menús nativos

        # Menú Admin
        admin_menu = barra_menu.addMenu("Admin")
        admin_menu.addAction("Pleno Ordinario").triggered.connect(lambda: self.mostrar_editor("ordinario"))
        admin_menu.addAction("Pleno Extraordinario").triggered.connect(lambda: self.mostrar_editor("extraordinario"))

        # Menú Visualización
        visualizacion_menu = barra_menu.addMenu("Visualización")
        visualizacion_menu.addAction("Ver Pleno Ordinario").triggered.connect(lambda: self.mostrar_pleno("ordinario"))
        visualizacion_menu.addAction("Ver Pleno Extraordinario").triggered.connect(
            lambda: self.mostrar_pleno("extraordinario"))
        
        # Opción Ayuda
        ayuda_menu = barra_menu.addMenu("Ayuda")
        guia_widget = QWidget()
        guia_layout = QHBoxLayout(guia_widget)
        guia_layout.setContentsMargins(10, 0, 10, 0)  # Márgenes laterales iguales
        guia_layout.setSpacing(5)  # Espacio reducido entre texto e icono

        # Texto con alineación perfecta
        guia_text = QLabel("Guía")
        guia_text.setStyleSheet("""
               QLabel {
                   color: black;
                   padding: 0;
                   margin: 0;
                   font: 9pt "Segoe UI";
               }
           """)

        # Icono con tamaño preciso
        guia_icon = QLabel()
        guia_icon.setPixmap(QIcon("assets/help_icon.png").pixmap(14, 14))
        guia_icon.setStyleSheet("padding: 0; margin: 0;")

        guia_layout.addWidget(guia_text, alignment=Qt.AlignmentFlag.AlignVCenter)
        guia_layout.addStretch()  # Empuja el icono a la derecha
        guia_layout.addWidget(guia_icon, alignment=Qt.AlignmentFlag.AlignVCenter)

        guia_action = QWidgetAction(ayuda_menu)
        guia_action.setDefaultWidget(guia_widget)
        guia_action.triggered.connect(self.mostrar_guia)
        ayuda_menu.addAction(guia_action)

        # Opción Información
        info_action = QAction("Información", self)
        info_action.triggered.connect(self.mostrar_info)
        ayuda_menu.addAction(info_action)

        salir_action = QAction(self)
        salir_action.setIcon(QIcon("assets/exit_icon.png"))
        salir_action.triggered.connect(QApplication.instance().quit)
        barra_menu.addAction(salir_action)

        # Estilo del Menu Bar
        barra_menu.setStyleSheet("""
                /* Barra de menú principal */
                QMenuBar {
                    background-color: white;
                    color: black;
                }
                QMenuBar::item {
                    background: transparent;
                    color: black;
                    padding: 5px 15px;
                }
                QMenuBar::item:selected {
                    background-color: #e0e0e0;  /* Gris claro al seleccionar */
                    color: black;
                }
                
                /* Menús desplegables */
                QMenu {
                    background-color: white;
                    color: black;
                    border: 1px solid #d0d0d0;
                }
                QMenu::item {
                    background-color: transparent;
                    color: black;
                    padding: 5px 20px 5px 10px;
                    height: 22px;
                }
                QMenu::item:selected {
                    background-color: #e0e0e0;  /* Gris claro al seleccionar */
                    color: black;
                }
                QMenu::icon {
                    left: 5px;  /* Posición de iconos en submenú */
                }
                
                /* Elementos personalizados */
                QWidgetAction {
                    background: transparent;
                    min-width: 120px;
                }
            """)

########################################################################################################

    def mostrar_guia(self):
        """Muestra la ventana de guía de usuario"""
        self.ventana_guia = VentanaGuia()
        self.ventana_guia.show()

########################################################################################################

    def mostrar_info(self):
        """Muestra la ventana de información de la aplicación"""
        self.ventana_info = VentanaInfo()
        self.ventana_info.show()

########################################################################################################

    def mostrar_editor(self, tipo_pleno):
        """Cambia a la vista dividida con el cronómetro"""
        self.stacked_main.setCurrentIndex(1)
        self.tipo_pleno_actual = tipo_pleno
        self.cargar_temporizadores()

########################################################################################################

    def mostrar_pleno(self, tipo_pleno):
        # Cargar cronómetros según el tipo de pleno
        if tipo_pleno == "ordinario":
            cronometros = Almacenamiento.cargar_cronometros_ordinario()
        elif tipo_pleno == "extraordinario":
            cronometros = Almacenamiento.cargar_cronometros_extraordinario()
        else:
            print(f"Tipo de pleno desconocido: {tipo_pleno}")
            return

        if cronometros:
            # Crear y mostrar la ventana de visualización
            self.ventana_visualizacion = VentanaVisualizacion(cronometros, tipo_pleno)
            self.ventana_visualizacion.show()

            # Crear y mostrar la ventana de controles
            self.ventana_controles = VentanaControles(cronometros, tipo_pleno, self.sound_alarm)
            self.ventana_controles.tiempo_actualizado.connect(self.ventana_visualizacion.actualizar_tiempo)  # Conectar señal
            self.ventana_controles.show()
        else:
            print(f"No se encontraron cronómetros para el tipo de pleno: {tipo_pleno}")


########################################################################################################

    def cargar_temporizadores(self):
        """Carga los temporizadores desde el archivo"""
        # Cargar cronómetros según el tipo de pleno actual
        if self.tipo_pleno_actual == "ordinario":
            datos = Almacenamiento.cargar_cronometros_ordinario()
        elif self.tipo_pleno_actual == "extraordinario":
            datos = Almacenamiento.cargar_cronometros_extraordinario()
        else:
            print(f"Tipo de pleno desconocido: {self.tipo_pleno_actual}")
            return

        self.temporizadores = []
        self.pagina_dividida.lista_temporizadores.clear()

        # Agregar los cronómetros cargados a la interfaz
        for item in datos:
            self.agregar_temporizador_desde_datos(
                item["nombre"], 
                item["minutos"], 
                item["segundos"], 
                item.get("numeracion"),
                logo=item.get("logo")
            )


########################################################################################################

    def agregar_temporizador_desde_datos(self, nombre, minutos, segundos, numeracion=None, logo=None):
        """Agrega un temporizador desde datos existentes"""
        cronometro = Cronometro(nombre, minutos, segundos, numeracion=numeracion, logo=logo)
        self.temporizadores.append(cronometro)
        self.pagina_dividida.agregar_temporizador_ui(cronometro, self)

########################################################################################################

    def accion_principal_temporizador(self):
        """Maneja el botón principal (Agregar/Actualizar)"""
        if self.cronometro_editando:
            self.actualizar_temporizador()
        else:
            self.agregar_temporizador()

########################################################################################################

    def agregar_temporizador(self):
        """Agrega un nuevo temporizador"""
        nombre = self.pagina_dividida.titulo.text().strip()
        if not nombre or (self.minutos == 0 and self.segundos == 0):
            QMessageBox.warning(self, "Error", "El cronómetro debe tener un título y un tiempo mayor a 00:00.")
            return
    
        logo_path = self.pagina_dividida.combo_logos.currentData()  # Obtener el logo seleccionado

        # Crear el cronómetro con el logo
        cronometro = Cronometro(nombre, self.minutos, self.segundos, logo=logo_path)

        # Agregar el cronómetro a la lista y actualizar la UI
        self.temporizadores.append(cronometro)
        self.pagina_dividida.agregar_temporizador_ui(cronometro, self)
    
        # Guardar los cronómetros
        Almacenamiento.guardar_cronometros(self.tipo_pleno_actual, self.temporizadores)
        self.resetear_controles()

########################################################################################################

    def actualizar_temporizador(self):
        """Actualiza un temporizador existente"""
        if not self.cronometro_editando:
            return

        nombre = self.pagina_dividida.titulo.text().strip()
        if not nombre or (self.minutos == 0 and self.segundos == 0):
            QMessageBox.warning(self, "Error", "El cronómetro debe tener un título y un tiempo mayor a 00:00.")
            return
    
        logo_path = self.pagina_dividida.combo_logos.currentData()

        # Actualizar el cronómetro editado con los nuevos valores
        self.cronometro_editando.nombre = nombre
        self.cronometro_editando.minutos = self.minutos
        self.cronometro_editando.segundos = self.segundos
        self.cronometro_editando.logo_path = logo_path  # Asegúrate de usar 'logo_path'
        print(f"Actualizando cronómetro: {self.cronometro_editando.nombre} - {self.cronometro_editando.minutos}:{self.cronometro_editando.segundos} - Logo: {self.cronometro_editando.logo_path}")
        # Actualizar UI para reflejar los cambios
        self.pagina_dividida.actualizar_temporizador_ui(self.cronometro_editando)
        print(f"Tipo de pleno actual: {self.tipo_pleno_actual}")
        # Guardar todos los cronómetros en el archivo
        Almacenamiento.guardar_cronometros(self.tipo_pleno_actual, self.temporizadores)
    
        # Resetear el modo de edición
        self.resetear_edicion()
   
########################################################################################################

    def editar_temporizador(self, cronometro):
        """Prepara la edición de un temporizador"""
        self.cronometro_editando = cronometro
        self.pagina_dividida.titulo.setText(cronometro.nombre)
        self.minutos = cronometro.minutos
        self.segundos = cronometro.segundos
        self.pagina_dividida.min_display.setText(f"{self.minutos:02d}")  
        self.pagina_dividida.seg_display.setText(f"{self.segundos:02d}") 
        self.pagina_dividida.btn_agregar.setText("Actualizar")

        if cronometro.logo_path:
        # Si hay logo, actualizar el logo
            if hasattr(self.pagina_dividida, 'logo_label'):
                self.pagina_dividida.logo_label.setPixmap(QPixmap(cronometro.logo))
                self.pagina_dividida.logo_label.show()
        else:
        # Si no hay logo, limpiar o establecer un logo por defecto
            if hasattr(self.pagina_dividida, 'logo_label'):
                self.pagina_dividida.logo_label.clear() 

        self.stacked_main.setCurrentIndex(1)

########################################################################################################

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

########################################################################################################

    def ajustar_tiempo(self, tipo, valor):
        """Ajusta el tiempo mostrado en el editor"""
        if tipo == "min":
            self.minutos = max(0, min(59, self.minutos + valor))
        else:
            self.segundos = max(0, min(59, self.segundos + valor))

        self.pagina_dividida.min_display.setText(f"{self.minutos:02d}")  
        self.pagina_dividida.seg_display.setText(f"{self.segundos:02d}")

########################################################################################################

    def resetear_controles(self):
        """Resetea los controles a sus valores por defecto"""
        self.pagina_dividida.titulo.clear()
        self.minutos = 0
        self.segundos = 0
        self.pagina_dividida.min_display.setText("00")
        self.pagina_dividida.seg_display.setText("00")

########################################################################################################

    def resetear_edicion(self):
        """Termina el modo de edición"""
        self.resetear_controles()
        self.cronometro_editando = None
        self.pagina_dividida.btn_agregar.setText("Agregar")

########################################################################################################

    def reordenar_temporizadores(self):
        """Actualiza el orden interno de los cronómetros tras moverlos en la UI"""
        nuevos_temporizadores = []

        for i in range(self.pagina_dividida.lista_temporizadores.count()):
          item = self.pagina_dividida.lista_temporizadores.item(i)
          widget = self.pagina_dividida.lista_temporizadores.itemWidget(item)

          for cronometro in self.temporizadores:
            if cronometro.widget == widget:
                cronometro.numeracion = i + 1  # Asigna numeración nueva según posición
                nuevos_temporizadores.append(cronometro)
                break

        self.temporizadores = nuevos_temporizadores
        Almacenamiento.guardar_cronometros(self.tipo_pleno_actual, self.temporizadores)