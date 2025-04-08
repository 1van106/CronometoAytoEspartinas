import json
import os
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class Almacenamiento:
    @staticmethod
    def guardar_cronometros(tipo_pleno, cronometros):
        nombre_archivo = f"cronometros_{tipo_pleno}.json"
        datos = [{
            "nombre": c.nombre,
            "minutos": c.minutos,
            "segundos": c.segundos,
            "numeracion": i + 1,  # "i" es el índice proporcionado por enumerate
            "logo": c.logo_path  # Guardamos el logo_path
        } for i, c in enumerate(cronometros)]  # Usamos enumerate para obtener el índice 'i' y el cronómetro 'c'
        
        with open(nombre_archivo, "w") as file:
            json.dump(datos, file, indent=4)

########################################################################################################

    @staticmethod
    def cargar_cronometros(tipo_pleno):
        nombre_archivo = f"cronometros_{tipo_pleno}.json"
        try:
            with open(nombre_archivo, "r") as file:
                cronometros = json.load(file)

                # Añadir valores originales
                for cronometro in cronometros:
                    cronometro['minutos_originales'] = cronometro['minutos']
                    cronometro['segundos_originales'] = cronometro['segundos']

                    if cronometro.get('logo') and os.path.exists(cronometro['logo']):
                        logo_label = QLabel()
                        pixmap = QPixmap(cronometro['logo']).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
                        logo_label.setPixmap(pixmap)
                        
                        cronometro["logo_label"] = logo_label

                # Ordenar por numeración si existe
                cronometros.sort(key=lambda x: x.get("numeracion", 0))
                return cronometros
        except (FileNotFoundError, json.JSONDecodeError):
            return []