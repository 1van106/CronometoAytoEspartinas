import json


class Almacenamiento:
    @staticmethod
    def guardar_cronometros(tipo_pleno, cronometros):
        nombre_archivo = f"cronometros_{tipo_pleno}.json"
        datos = [{
            "nombre": c.nombre,
            "minutos": c.minutos,
            "segundos": c.segundos
        } for c in cronometros]

        with open(nombre_archivo, "w") as file:
            json.dump(datos, file, indent=4)

########################################################################################################

    @staticmethod
    def cargar_cronometros(tipo_pleno):
        nombre_archivo = f"cronometros_{tipo_pleno}.json"
        try:
          with open(nombre_archivo, "r") as file:
            cronometros = json.load(file)
            # Añadir los valores originales a cada cronómetro cargado
            for cronometro in cronometros:
                cronometro['minutos_originales'] = cronometro['minutos']
                cronometro['segundos_originales'] = cronometro['segundos']
            return cronometros
        except (FileNotFoundError, json.JSONDecodeError):
          return []