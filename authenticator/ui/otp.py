# -*- coding: utf-8 -*-

from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets

from authenticator.vault import interface
from authenticator.vault.encryption import EncryptionKeyManager
from authenticator.vault.models import OTP
from authenticator.vault.session import SessionMaker
from authenticator.ui.generic import ScrollableItems


class OTPProgressWidget(QtWidgets.QProgressBar):
    def __init__(self, parent, otp):
        super().__init__(parent)
        self.otp = otp

        self.setTextVisible(False)
        self.setFixedHeight(8)
        self.setFixedWidth(40)

        self.setStyleSheet(
            """
            background-color: #424242;
            QProgresBar::chunk {
                background-color: #05B8CC;
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


class OTPFilter(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        search_icon = QtGui.QIcon("authenticator/ui/assets/search.png")
        self.addAction(search_icon, QtWidgets.QLineEdit.LeadingPosition)
        self.textChanged.connect(self.parent().update_search)

        self.setStyleSheet(
            """
            QLineEdit {
                background-color: #fff;
                color: #000;
            }
        """
        )


class OTPWidget(QtWidgets.QWidget):
    def __init__(self, otp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.otp = otp

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
            self.otp.get_next_change_timeout(), self.update_code_label
        )


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
        top_layout.addWidget(OTPFilter(self))
        top_layout.addWidget(lock_button)

        container = QtWidgets.QWidget()
        container.setLayout(self.otp_layout)

        scroll = ScrollableItems(container)

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
            font-size: 50px;
            height: 60px;
            width: 60px;
        """
        )

        self.clicked.connect(lambda: self.parent().change_screen("desktop_capture"))
