# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from authenticator.ui.add_otp import AddOtpForm
from authenticator.ui.desktop_capture import DesktopCapture
from authenticator.ui.otp import OTPCreateButton, OTPList
from authenticator.ui.setup_vault import SetupVaultForm
from authenticator.ui.unlock_vault import UnlockVaultForm
from authenticator.vault.encryption import EncryptionKeyManager


class BaseScreen(QtWidgets.QWidget):
    transparent = False

    def __init__(self, app: "AuthenticatorApp", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app
        self.kwargs = {}

        if (
            self.__class__.__name__ not in ["UnlockVaultScreen", "SetupVaultScreen"]
            and EncryptionKeyManager().is_locked()
        ):
            self.change_screen("unlock_vault")
            return

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


class SetupVaultScreen(BaseScreen):
    def setup(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(SetupVaultForm())
        self.setLayout(layout)

    def on_screen_show(self):
        self._app.main_window.resize(self.sizeHint().width(), self.sizeHint().height())


class UnlockVaultScreen(BaseScreen):
    def setup(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(UnlockVaultForm())
        self.setLayout(layout)

    def on_screen_show(self):
        if not EncryptionKeyManager().is_locked():
            self.change_screen("otp")
        else:
            self._app.main_window.resize(
                self.sizeHint().width(), self.sizeHint().height()
            )


class OTPScreen(BaseScreen):
    def setup(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(OTPList(self))
        layout.addWidget(
            OTPCreateButton(), alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
        )

    def on_screen_show(self):
        self._app.main_window.resize(self.sizeHint().width(), 600)
        self._app.main_window.setFixedWidth(440)

    def on_screen_close(self):
        ...
        self._app.main_window.setMaximumWidth(
            self._app.main_window.screen().size().width()
        )


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

        self._current_screen_name = (
            "setup_vault" if EncryptionKeyManager.is_setup() else "unlock_vault"
        )
        self._current_screen = None
        self.screens = {
            "setup_vault": lambda: SetupVaultScreen(self),
            "unlock_vault": lambda: UnlockVaultScreen(self),
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
        self.layout.addWidget(self.screen)
        self.screen.on_screen_show()
        if self.screen.transparent:
            self.main_window.setStyleSheet(
                "background-color: transparent; color: #fff;"
            )
        else:
            self.main_window.setStyleSheet("background-color: #000; color: #fff;")

    def run(self):
        self.main_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.main_window.setMinimumHeight(200)
        self.change_screen(self._current_screen_name)
        self.main_window.show()
        self.app.exec_()
