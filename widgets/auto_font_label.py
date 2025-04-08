from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFontMetrics, QFont
from PyQt6.QtCore import Qt

class AutoFontLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(False)
        self.original_font = self.font()
        self.setMinimumSize(1, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustFontSize()

    def adjustFontSize(self):
        if not self.text():
            return
        font = QFont(self.original_font)
        rect = self.contentsRect()
        size = 1
        max_size = 1000
        while size < max_size:
            font.setPointSize(size)
            metrics = QFontMetrics(font)
            if metrics.horizontalAdvance(self.text()) > rect.width() or metrics.height() > rect.height():
                break
            size += 1
        font.setPointSize(size - 1)
        self.setFont(font)


