#!/usr/bin/env python
import asyncio
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from qasync import QEventLoop, asyncClose, asyncSlot


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.button = QPushButton("Load", self)
        self.button.clicked.connect(self.onButtonClicked)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    @asyncSlot()
    async def onButtonClicked(self):
        """
        Use async code in a slot by decorating it with @asyncSlot.
        """
        self.button.setText("Loading...")
        await asyncio.sleep(1)
        self.button.setText("Load")

    @asyncClose
    async def closeEvent(self, event: QCloseEvent):  # type: ignore[override]
        """
        Use async code in a closeEvent by decorating it with @asyncClose.
        """
        self.button.setText("Closing...")
        await asyncio.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Prevent event loop from stopping
    # given the change to clean up on last window closed
    app.setQuitOnLastWindowClosed(False)

    app_close_event = asyncio.Event()
    app.lastWindowClosed.connect(app_close_event.set)

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    async def async_main():
        await app_close_event.wait()

    asyncio.run(async_main(), loop_factory=QEventLoop)
