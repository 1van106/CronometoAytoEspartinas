import os
import shutil
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QFrame,QGraphicsDropShadowEffect,QSizePolicy,
                             QListWidgetItem,QComboBox, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFontDatabase, QFont, QColor,QPixmap

########################################################################################################

class VistaDividida(QWidget):
    def __init__(self):
        super().__init__()
        # Paleta de colores con gris anaranjado
        self.COLOR_FONDO = "#332211"  # Gris oscuro con tono anaranjado
        self.COLOR_PRIMARIO = "#FF8C42"  # Naranja cálido
        self.COLOR_SECUNDARIO = "#FF9F5E"  # Naranja más claro
        self.COLOR_TEXTO = "#F5F5F5"  # Blanco ligeramente cálido
        self.COLOR_TEXTO_OSCURO = "#1A120B"  # Para texto sobre naranja
        self.COLOR_BORDE = "#FF9F5E"  # Borde naranja

        font_id = QFontDatabase.addApplicationFont("assets/DS-DIGIB.TTF")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
          self.fuente_led = QFont(font_families[0], 20)
        else:
          self.fuente_led = QFont("Arial", 20)
        

        self.init_ui()

########################################################################################################

    def init_ui(self):
        self.setStyleSheet("background: #F5F5F5")
        self.resize(400, 800)
        self.show()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Frame izquierdo (editor de cronómetro)
        self.left_frame = QFrame()
        self.left_frame.setStyleSheet(f"""
          background: #F5F5F5;
          border-right: 2px solid #2B2D31;
        """)
        left_layout = QVBoxLayout(self.left_frame)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)

        # Crear el combobox para seleccionar el logo
        self.combo_logos = QComboBox(self)
        
        self.cargar_logos()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.combo_logos)

        # Título
        self.titulo = QLineEdit("")
        self.titulo.setPlaceholderText("Nombre de la Intervencion")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_titulo()
        left_layout.addWidget(self.titulo)

        # Contenedor del tiempo
        tiempo_layout = QHBoxLayout()  # Aquí mantenemos el layout horizontal
        left_layout.addLayout(tiempo_layout)

        # Contenedor para "Min"
        contenedor_min = QVBoxLayout()
        
    
        # Etiqueta de "Min" arriba del contenedor
        min_label = QLabel("MIN")
        min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        min_label.setStyleSheet(f"""
          font: bold 20px '{self.fuente_led.family()}';
          color: #2B2D31;
          background: none;
          border: none;
        """)
        contenedor_min.addWidget(min_label)

        self.min_display = QLabel("00")
        self.min_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_display(self.min_display)
        contenedor_min.addWidget(self.min_display)

        # Botones de control para Min
        botones_min_layout = QHBoxLayout()
        self.btn_min_down = QPushButton("-")
        self.btn_min_up = QPushButton("+")
        self.configurar_boton_control(self.btn_min_down)
        self.configurar_boton_control(self.btn_min_up)
        botones_min_layout.addWidget(self.btn_min_down)
        botones_min_layout.addWidget(self.btn_min_up)
        contenedor_min.addLayout(botones_min_layout)

        tiempo_layout.addLayout(contenedor_min)

        # Contenedor para "Seg"
        contenedor_seg = QVBoxLayout()
        
    
        # Etiqueta de "Seg" arriba del contenedor
        seg_label = QLabel("SEG")
        seg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        seg_label.setStyleSheet(f"""
          font: bold 20px '{self.fuente_led.family()}';
          color: #2B2D31;
          background: none;
          border: none;
        """)
        contenedor_seg.addWidget(seg_label)

        self.seg_display = QLabel("00")
        self.seg_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.configurar_estilo_display(self.seg_display)
        contenedor_seg.addWidget(self.seg_display)

        # Botones de control para Seg
        botones_seg_layout = QHBoxLayout()
        self.btn_seg_down = QPushButton("-")
        self.btn_seg_up = QPushButton("+")
        self.configurar_boton_control(self.btn_seg_down)
        self.configurar_boton_control(self.btn_seg_up)
        botones_seg_layout.addWidget(self.btn_seg_down)
        botones_seg_layout.addWidget(self.btn_seg_up)
        contenedor_seg.addLayout(botones_seg_layout)

        tiempo_layout.addLayout(contenedor_seg)

        self.configurar_selector_logo(left_layout)

        # Botón principal
        self.btn_agregar = QPushButton("AGREGAR")
        self.configurar_boton_principal(self.btn_agregar)
        left_layout.addWidget(self.btn_agregar, alignment=Qt.AlignmentFlag.AlignCenter)

        left_layout.addStretch()

        # Frame derecho (lista de temporizadores)
        self.right_frame = QFrame()
        self.right_frame.setStyleSheet(f"""
          background:#F5F5F5;
          
        """)

        self.right_layout = QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        self.lista_temporizadores = QListWidget()
        self.lista_temporizadores.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.lista_temporizadores.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.lista_temporizadores.model().rowsMoved.connect(self.actualizar_numeracion_temporizadores)
        self.lista_temporizadores.setCursor(Qt.CursorShape.OpenHandCursor)


        self.lista_temporizadores.setStyleSheet("""
          QListWidget {
            background: transparent;
            border: none;
            outline: none;
          }
          QListWidget::item {
            margin-bottom: 8px;
          }
          QListWidget::item:selected {
            background: transparent;
          }
          QListWidget::item:selected {
            background-color: rgba(43, 45, 49, 0.5);;
            border: 1px dashed #2B2D31;
          }
        """)
        self.right_layout.addWidget(self.lista_temporizadores)

        layout.addWidget(self.left_frame, stretch=1)
        layout.addWidget(self.right_frame, stretch=1)
        
######################################################################################################## 

    def cargar_logos(self):
        """Carga los logos disponibles desde el directorio assets"""
        logos_dir = "logos" 

        self.combo_logos.clear()  # Limpiamos el comboBox antes de cargar los nuevos logos
        self.combo_logos.addItem("Sin Logo", None)

        for logo in os.listdir(logos_dir):
            if logo.endswith((".png", ".jpg", ".jpeg")):
                logo_path = os.path.join(logos_dir, logo)
                self.combo_logos.addItem(logo, logo_path)
    
######################################################################################################## 
    
    def seleccionar_logo(self, index):
        """Maneja la selección del logo"""
        logo_path = self.combo_logos.currentData()
        print(f"Logo seleccionado: {logo_path}")
        if logo_path:
            self.cronometro_editando.logo = logo_path  # Actualiza el logo del temporizador
            # Ahora actualiza la interfaz
            if hasattr(self.pagina_dividida, 'logo_label'):
              self.pagina_dividida.logo_label.setPixmap(QPixmap(logo_path))
              self.pagina_dividida.logo_label.show() 

########################################################################################################    

    def abrir_dialogo_logo(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar logo", "", "Imágenes (*.png *.jpg *.jpeg)")
        if ruta_archivo:
            nombre_archivo = os.path.basename(ruta_archivo)
            destino = os.path.join("logos", nombre_archivo)

            # Copiar el archivo al assets si aún no existe
            if not os.path.exists(destino):
                shutil.copy(ruta_archivo, destino)

            self.cargar_logos()
            self.combo_logos.setCurrentText(nombre_archivo) 

########################################################################################################

    def configurar_selector_logo(self, layout_principal):
        layout_logo = QHBoxLayout()

        self.combo_logos = QComboBox()
        self.combo_logos.setStyleSheet("background: 2B2D31; padding: 6px; border-radius: 4px;")
        self.combo_logos.setFixedHeight(32)

        # Cargar logos disponibles
        self.cargar_logos()

        btn_cargar_logo = QPushButton("Cargar Logo")
        btn_cargar_logo.setFixedHeight(32)
        btn_cargar_logo.clicked.connect(self.abrir_dialogo_logo)

        layout_logo.addWidget(QLabel("Logo:"))
        layout_logo.addWidget(self.combo_logos)
        layout_logo.addWidget(btn_cargar_logo)

        layout_principal.addLayout(layout_logo)

########################################################################################################


    def actualizar_numeracion_temporizadores(self):
      for index in range(self.lista_temporizadores.count()):
        item = self.lista_temporizadores.item(index)
        widget = self.lista_temporizadores.itemWidget(item)
        if widget:
            numero_label = widget.findChild(QLabel, "numero_label")
            if numero_label:
                numero_label.setText(f"#{index + 1}")
      self.lista_temporizadores.update()


########################################################################################################

    def configurar_estilo_titulo(self):
        self.titulo.setFont(self.fuente_led)
        self.titulo.setStyleSheet(f"""
            QLineEdit {{
                color: #2B2D31;
                padding: 12px;
                border: 2px solid #2B2D31;
                border-radius: 6px;
                background: transparent;
            }}
            QLineEdit:focus {{
                border: 2px solid #2B2D31;
                background: transparent;
            }}
        """)

########################################################################################################

    def configurar_estilo_display(self, label):
        
        
        label.setStyleSheet(f"""
            QLabel {{
                color: #2B2D31;
                font:bold 40px '{self.fuente_led.family()}';
                padding: 10px 10px;
                background:#F5F5F5;
                border-radius: 10px;
                border: 3px dashed #2B2D31;
            }}
        """)

########################################################################################################

    def configurar_botones_control(self, layout):
        contenedor_controles = QWidget()
        contenedor_controles.setStyleSheet("background: #F5F5F5;")
        controles_layout = QHBoxLayout(contenedor_controles)
        controles_layout.setContentsMargins(0, 0, 0, 0)
        controles_layout.setSpacing(10)

        for btn in [self.btn_min_down, self.btn_seg_down, self.btn_min_up, self.btn_seg_up]:
            self.configurar_boton_control(btn)
            controles_layout.addWidget(btn)

        layout.addWidget(contenedor_controles, alignment=Qt.AlignmentFlag.AlignCenter)

########################################################################################################

    def configurar_boton_control(self, boton):
        boton.setFont(self.fuente_led)
        boton.setStyleSheet(f"""
            QPushButton {{
                color: #F5F5F5;
                background: #2B2D31;
                padding: 8px 12px;
                border: none;
                border-radius: 5px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {self.COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                background:  {self.COLOR_SECUNDARIO};
            }}
        """)

########################################################################################################

    def configurar_boton_principal(self, boton):
        boton.setFont(self.fuente_led)
        boton.setStyleSheet(f"""
            QPushButton {{
                color: #F5F5F5;
                background: #2B2D31;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                min-width: 200px;
                text-transform: uppercase;
            }}
            QPushButton:hover {{
                background: {self.COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                background: {self.COLOR_SECUNDARIO};
            }}
        """)

########################################################################################################

    def agregar_temporizador_ui(self, cronometro, controlador):
        """Agrega un temporizador a la interfaz con estilo moderno"""
        item = QListWidgetItem()
        widget = self.crear_widget_temporizador(cronometro, controlador)
        item.setSizeHint(widget.sizeHint())
        self.lista_temporizadores.addItem(item)
        self.lista_temporizadores.setItemWidget(item, widget)
        cronometro.widget = widget
        
########################################################################################################

    def crear_widget_temporizador(self, cronometro, controlador):
        """Crea un widget de temporizador con diseño moderno"""
        widget = QWidget()
        widget.setStyleSheet(f"""
            background: #F5F5F5;
            border: 2px solid #2B2D31;
            padding: 6px;
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)  # No márgenes en el layout
        info_layout.setSpacing(4) 

        # Número del temporizador
        numero_label = QLabel(f"#{self.lista_temporizadores.count() + 1}")
        numero_label.setObjectName("numero_label")
        numero_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        numero_label.setStyleSheet(f"""
            font: bold 24px '{self.fuente_led.family()}';
            color: #2B2D31;
            padding: 10px;
            border:None;
        """)
        numero_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Fijar tamaño
        info_layout.addWidget(numero_label)

        # Logo del temporizador (si existe)
        logo_label = None
        if cronometro.logo:
            logo_label = QLabel()
            logo_pixmap = QPixmap(cronometro.logo)
            logo_label.setPixmap(logo_pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Alineación vertical centrada
            logo_label.setStyleSheet(f"""
              border: None;
              padding: 2px;
              margin: 0;
            """)
          
            info_layout.addWidget(logo_label)
    

        numero_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        info_layout.addWidget(logo_label)


        # Título del temporizador
        nombre_label = QLabel(cronometro.nombre)
        nombre_label.setFont(self.fuente_led)
        nombre_label.setStyleSheet(f"""
            color:#2B2D31;
            border: None;
            margin:0;
        """)
        nombre_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        nombre_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        info_layout.addWidget(nombre_label)

        layout.addLayout(info_layout)

        # Tiempo del temporizador
        tiempo_label = QLabel(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")
        tiempo_label.setStyleSheet(f"""
            color: #2B2D31;
            font:bold 40px '{self.fuente_led.family()}';
            padding: 10px;
            margin:10px;
            border: 2px dashed #2B2D31;
        """)
        tiempo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tiempo_label)

        # Guardar referencias
        widget.label_nombre = nombre_label
        widget.label_tiempo = tiempo_label

        # Botones de acción
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(0, 0, 10, 0)
        botones_layout.setSpacing(10)

        # Botón Editar
        btn_editar = QPushButton()
        btn_editar.setCursor(Qt.CursorShape.ArrowCursor)
        if os.path.exists("assets/lapiz.png"):
            btn_editar.setIcon(QIcon("assets/lapiz.png"))
            btn_editar.setToolTip("Editar")
        else:
            btn_editar.setText("Editar")
        btn_editar.setStyleSheet(f"""
            QPushButton {{
                background: #F5F5F5;
                border: 2px solid #2B2D31;
                border-radius: 4px;
                padding:10px;
                min-width: 16px;
                max-width: 16px;
                min-height: 16px;
                max-height: 16px;
            }}
            QPushButton:hover {{
                background: {self.COLOR_SECUNDARIO};
            }}
        """)
        btn_editar.clicked.connect(lambda: controlador.editar_temporizador(cronometro))
        

        # Botón Eliminar
        btn_eliminar = QPushButton()
        btn_eliminar.setCursor(Qt.CursorShape.ArrowCursor)

        if os.path.exists("assets/papelera.png"):
            btn_eliminar.setIcon(QIcon("assets/papelera.png"))
            btn_eliminar.setToolTip("Eliminar")
        else:
            btn_eliminar.setText("X")
        btn_eliminar.setStyleSheet(f"""
            QPushButton {{
                background:  #F5F5F5;
                border: 2px solid #2B2D31;
                border-radius: 4px;
                padding: 10px;
                margin:10px;
                min-width: 16px;
                max-width: 16px;
                min-height: 16px;
                max-height: 16px;
                
            }}
            QPushButton:hover {{
                background: #FF6B5B;
            }}
        """)
        btn_eliminar.clicked.connect(lambda: controlador.eliminar_temporizador(cronometro))

        botones_layout.addStretch()
        botones_layout.addWidget(btn_editar)
        botones_layout.addWidget(btn_eliminar)
        

        layout.addLayout(botones_layout)

        return widget


########################################################################################################


    def actualizar_temporizador_ui(self, cronometro):
        """Actualiza la UI de un temporizador existente"""
        if cronometro.widget:
          cronometro.widget.label_nombre.setText(cronometro.nombre)
          cronometro.widget.label_tiempo.setText(f"{cronometro.minutos:02d}:{cronometro.segundos:02d}")