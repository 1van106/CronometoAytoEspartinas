from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox)
from PyQt6.QtGui import QAction


class VentanaConMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("Aplicación con Menú")
        self.setGeometry(100, 100, 800, 600)  # (x, y, ancho, alto)

        # Creamos la barra de menú
        self.crear_menu()

    def crear_menu(self):
        # Creamos la barra de menú
        barra_menu = self.menuBar()

        # Menú "Archivo" (con la opción "Agregar")
        menu_archivo = barra_menu.addMenu("Archivo")

        # Acción "Agregar"
        accion_agregar = QAction("Agregar", self)
        accion_agregar.triggered.connect(self.agregar)
        menu_archivo.addAction(accion_agregar)

        # Acción "Eliminar"
        accion_eliminar = QAction("Eliminar", self)
        accion_eliminar.triggered.connect(self.eliminar)
        menu_archivo.addAction(accion_eliminar)

        # Menú "Editar" (con la opción "Modificar")
        menu_editar = barra_menu.addMenu("Editar")

        # Acción "Modificar"
        accion_modificar = QAction("Modificar", self)
        accion_modificar.triggered.connect(self.modificar)
        menu_editar.addAction(accion_modificar)

        # Menú "Ayuda"
        menu_ayuda = barra_menu.addMenu("Ayuda")

        # Acción "Acerca de..."
        accion_acerca = QAction("Acerca de...", self)
        accion_acerca.triggered.connect(self.mostrar_ayuda)
        menu_ayuda.addAction(accion_acerca)

    # Funciones que se ejecutan al hacer clic en los menús
    #def agregar(self):

    #def eliminar(self):

    #def modificar(self):

    def mostrar_ayuda(self):


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaConMenu()
    ventana.show()
    app.exec()