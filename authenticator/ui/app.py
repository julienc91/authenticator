# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from .desktop_capture import DesktopCapture
from .otp import OTPCreateButton, OTPList


class BaseScreen(QtWidgets.QWidget):
    transparent = False

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app
        self.setup()

    def change_screen(self, screen_name: str):
        self._app.change_screen(screen_name)


class OTPScreen(BaseScreen):
    def setup(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(OTPList())
        layout.addWidget(
            OTPCreateButton(), alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
        )
        self.setLayout(layout)


class DesktopCaptureScreen(BaseScreen):
    transparent = True

    def setup(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(DesktopCapture())
        layout.setContentsMargins(0, 0, 0, 0)


class AuthenticatorApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.main_window = QtWidgets.QMainWindow()

        self.container = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._current_screen = "otp"
        self.screens = {
            "otp": OTPScreen(self),
            "desktop_capture": DesktopCaptureScreen(self),
        }
        self.main_window.setCentralWidget(self.container)

    @property
    def screen(self) -> BaseScreen:
        return self.screens[self._current_screen]

    def change_screen(self, screen_name: str):
        if self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

        self._current_screen = screen_name
        self.layout.addWidget(self.screen)
        if self.screen.transparent:
            self.main_window.setStyleSheet(
                "background-color: transparent; color: #fff;"
            )
        else:
            self.main_window.setStyleSheet("background-color: #000; color: #fff;")

    def run(self):
        self.main_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.main_window.setMinimumWidth(380)
        self.change_screen(self._current_screen)
        self.main_window.show()
        self.app.exec_()
