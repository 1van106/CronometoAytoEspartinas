# sesion_pleno.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter
import os

class SesionPleno:
    def __init__(self):
        self.sesion_pleno_activa = False
        self.cronometros = []  # Deberías tener una lista de cronómetros como en tu aplicación

    def iniciar_sesion(self):
        """Inicia la sesión del pleno"""
        self.sesion_pleno_activa = True
        print("Sesión del pleno iniciada.")
        # Aquí podrías reiniciar los cronómetros si es necesario
        #self.reiniciar_cronometros()

    def activar_sesion(self):
        """Activa la sesión y empieza a contar el tiempo"""
        if self.sesion_pleno_activa:
            print("La sesión del pleno ya está activa.")
        else:
            self.iniciar_sesion()

    def generar_reporte(self):
        reportes = []
       
        for cronometro in self.cronometros:
            nombre = cronometro['nombre']
            tiempo_total_segundos = cronometro.get('tiempo_total', 0)
            minutos = tiempo_total_segundos // 60
            segundos = tiempo_total_segundos % 60
            reportes.append(f"{nombre}: {minutos:02d}:{segundos:02d} (Total: {tiempo_total_segundos} segundos)")
    
        texto_reporte = "Reporte de Cronómetros\n" + "=" * 30 + "\n" + "\n".join(reportes)

        with open("reporte_cronometros.txt", "w") as archivo:
            archivo.write(texto_reporte)
            self.guardar_reporte()

        return texto_reporte
    
      
    
    def finalizar_sesion(self):
            """Finaliza la sesión del pleno"""
            if self.sesion_pleno_activa:
                print("Sesión del pleno finalizada.")
                self.sesion_pleno_activa = False  # Desactivar sesión
            else:
                print("No hay sesión activa para finalizar.")
    
    
    def mostrar_reporte_en_ventana(self):
        # Crear la ventana del reporte
        ventana_reporte = QDialog()
        ventana_reporte.setWindowTitle("Reporte de Cronómetros")
    
        # Crear un layout
        layout = QVBoxLayout()
    
        # Crear un QTextEdit para mostrar el reporte
        reporte_texto = QTextEdit()
        reporte_texto.setReadOnly(True)  # No permitir edición
    
        # Llamar a la función para generar el reporte (y almacenarlo en una variable)
        reportes = self.generar_reporte()  # Modifica esta función para devolver el reporte
        reporte_texto.setText(reportes)
    
        # Añadir el QTextEdit al layout
        layout.addWidget(reporte_texto)
    
        # Botón para guardar el reporte
        boton_guardar = QPushButton("Guardar Reporte")
        boton_guardar.clicked.connect(self.guardar_reporte)
        layout.addWidget(boton_guardar)
    
        # Botón para imprimir el reporte (si es necesario)
        boton_imprimir = QPushButton("Imprimir Reporte")
        boton_imprimir.clicked.connect(self.imprimir_reporte)
        layout.addWidget(boton_imprimir)
    
        # Establecer el layout en la ventana
        ventana_reporte.setLayout(layout)
        ventana_reporte.exec()
    

    def imprimir_reporte(self):
        from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
    
        printer = QPrinter(QPrinter.HighResolution)
        dialogo_imprimir = QPrintDialog(printer)
    
        if dialogo_imprimir.exec() == QPrintDialog.Accepted:
            # Imprimir el texto en el QTextEdit
            texto_imprimir = self.generar_reporte()  # Texto del reporte
            painter = QPainter(printer)
            painter.begin(printer)
            painter.drawText(100, 100, texto_imprimir)
            painter.end()


    def guardar_reporte(self):
        path, _ = QFileDialog.getSaveFileName(None, "Guardar Reporte", "", "Archivos de texto (*.txt)")
        if path:
            with open(path, "w") as file:
                file.write(self.generar_reporte())
