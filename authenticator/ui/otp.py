# -*- coding: utf-8 -*-

from typing import List

import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets

from authenticator.vault import interface
from authenticator.vault.encryption import EncryptionKeyManager
from authenticator.vault.models import OTP
from authenticator.vault.session import SessionMaker
from authenticator.ui.generic import ScrollableItems, TextInput


class OTPProgressWidget(QtWidgets.QProgressBar):
    def __init__(self, parent, otp):
        super().__init__(parent)
        self.otp = otp

        self.setTextVisible(False)
        self.setFixedHeight(8)
        self.setFixedWidth(40)

        self.setStyleSheet(
            """
            QProgressBar {
                background-color: #424242;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                border-radius: 2px;
            }
        """
        )
        self.update_progress()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_progress)
        timer.start(200)

    @property
    def _progress(self):
        interval = self.otp.interval
        timeout = self.otp.get_next_change_timeout()
        return 100.0 * timeout / interval

    def update_progress(self):
        self.setValue(self._progress)
        self.repaint()


class CopyButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(50)
        self.setIcon(QtGui.QIcon("authenticator/ui/assets/copy.png"))
        self.setStyleSheet("border: none;")


class OTPWidget(QtWidgets.QWidget):
    def __init__(self, otp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.otp = otp
        self.hover_timer = QtCore.QTimer(self)
        self.hover_timer.setInterval(200)
        self.hover_timer.setSingleShot(True)

        issuer_label = QtWidgets.QLabel(self._issuer)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(issuer_label)

        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QHBoxLayout()

        progress = OTPProgressWidget(self, otp)
        container_layout.addWidget(progress)

        code_label = QtWidgets.QLabel(self._code)
        code_label.setFont(QtGui.QFont("Monospace", 30, QtGui.QFont.Monospace))
        container_layout.addWidget(code_label)

        self.copy_button = CopyButton()
        self.copy_button.hide()
        self.copy_button.pressed.connect(self.copy_code)
        container_layout.addWidget(self.copy_button)
        container.setLayout(container_layout)

        main_layout.addWidget(container)
        self.setLayout(main_layout)
        self.setFixedHeight(120)

        self.code_label = code_label

        QtCore.QTimer.singleShot(
            self.otp.get_next_change_timeout(), self.update_code_label
        )

    @property
    def _code(self) -> str:
        code = self.otp.generate()
        digits = self.otp.digits
        return f"{int(code):0{digits}}"

    @property
    def _issuer(self) -> str:
        issuer = self.otp.issuer
        label = self.otp.label
        if issuer and label:
            return f"{issuer}:{label}"
        return f"{issuer}{label}"

    def update_code_label(self):
        self.code_label.setText(self._code)
        QtCore.QTimer.singleShot(
            self.otp.get_next_change_timeout() * 1000, self.update_code_label
        )

    def copy_code(self):
        pyperclip.copy(self._code)
        self.copy_button.hide()

    def enterEvent(self, _):
        self.hover_timer.start()
        self.hover_timer.timeout.connect(lambda: self.copy_button.show())

    def leaveEvent(self, _):
        if self.hover_timer:
            self.hover_timer.stop()
        self.copy_button.hide()


class OTPList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_text = ""

        self.otp_layout = QtWidgets.QVBoxLayout()
        self.otp_layout.setAlignment(QtCore.Qt.AlignTop)
        self.refresh_items()

        top_layout = QtWidgets.QHBoxLayout()
        lock_button = QtWidgets.QPushButton()
        lock_button.setIcon(QtGui.QIcon("authenticator/ui/assets/lock.png"))
        lock_button.pressed.connect(self.lock_vault)
        filter_input = TextInput(icon="authenticator/ui/assets/search.png")
        filter_input.textChanged.connect(self.update_search)
        top_layout.addWidget(filter_input)
        top_layout.addWidget(lock_button)

        container = QtWidgets.QWidget()
        container.setLayout(self.otp_layout)

        scroll = ScrollableItems(container, self)
        self.setFixedWidth(420)
        scroll.setFixedWidth(400)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addWidget(scroll)

    def get_items(self) -> List[OTP]:
        session = SessionMaker()
        return interface.get_all_otp(session, search=self.search_text)

    def update_search(self, search):
        self.search_text = search
        self.refresh_items()

    def refresh_items(self):
        while self.otp_layout.count():
            item = self.otp_layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

        for item in self.get_items():
            self.otp_layout.addWidget(OTPWidget(item))

    def lock_vault(self):
        EncryptionKeyManager().lock()
        self.parent().change_screen("unlock_vault")


class OTPCreateButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__("+", parent)
        self.setStyleSheet(
            """
            background-color: #05B8CC;
            border-radius: 30px;
            color: #fff;
            font-size: 60px;
            height: 55px;
            padding-bottom: 5px;
            text-align: center;
            width: 60px;
        """
        )

        self.clicked.connect(lambda: self.parent().change_screen("desktop_capture"))
