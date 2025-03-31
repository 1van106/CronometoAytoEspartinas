import sys
from PyQt6.QtWidgets import QApplication
from cronometro_app import CronometroApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CronometroApp()  
    ventana.show()
    sys.exit(app.exec())
