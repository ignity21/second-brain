#!/usr/bin/env python
import random
import sys

from PySide6 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World!")
        self.resize(300, 200)
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Hello, World!", self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button = QtWidgets.QPushButton("Change Text", self)
        self.button.clicked.connect(self.change_text)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    @QtCore.Slot()
    def change_text(self):
        texts = [
            "Hello, World!",
            "Bonjour le monde!",
            "Hola, Mundo!",
            "Hallo, Welt!",
            "Ciao, Mondo!",
        ]
        self.label.setText(random.choice(texts))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
