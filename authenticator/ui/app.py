# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from .add_otp import AddOtpForm
from .desktop_capture import DesktopCapture
from .otp import OTPCreateButton, OTPList


class BaseScreen(QtWidgets.QWidget):
    transparent = False

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app
        self.kwargs = {}
        self.setup()

    def change_screen(self, screen_name: str, **kwargs):
        self._app.change_screen(screen_name, **kwargs)

    def set_kwargs(self, **kwargs):
        self.kwargs.update(kwargs)

    def setup(self):
        raise NotImplementedError

    def on_screen_show(self):
        pass

    def on_screen_close(self):
        pass


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


class AddOtpScreen(BaseScreen):
    def __init__(self, *args, **kwargs):
        self.form_widget = None
        super().__init__(*args, **kwargs)

    def setup(self):
        layout = QtWidgets.QVBoxLayout(self)
        self.form_widget = AddOtpForm()
        layout.addWidget(self.form_widget)

    def on_screen_show(self):
        self.form_widget.set_uri(self.kwargs["uri"])


class AuthenticatorApp:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.main_window = QtWidgets.QMainWindow()

        self.container = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._current_screen_name = "otp"
        self._current_screen = None
        self.screens = {
            "otp": lambda: OTPScreen(self),
            "desktop_capture": lambda: DesktopCaptureScreen(self),
            "add_otp": lambda: AddOtpScreen(self),
        }
        self.main_window.setCentralWidget(self.container)

    @property
    def screen(self) -> BaseScreen:
        if self._current_screen is None:
            self._current_screen = self.screens[self._current_screen_name]()
        return self._current_screen

    def change_screen(self, screen_name: str, **kwargs):
        if self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            widget.on_screen_close()
            widget.deleteLater()
            self._current_screen = None

        self._current_screen_name = screen_name
        self.screen.set_kwargs(**kwargs)
        self.screen.on_screen_show()
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
        self.change_screen(self._current_screen_name)
        self.main_window.show()
        self.app.exec_()
