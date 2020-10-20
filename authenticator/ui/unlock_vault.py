# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from ..vault.encryption import EncryptionKeyManager, VaultLockedException


class UnlockVaultForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()
        self.password_field = QtWidgets.QLineEdit()
        form_layout.addRow(QtWidgets.QLabel("Password"), self.password_field)
        layout.addLayout(form_layout)

        self.error_label = QtWidgets.QLabel()
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.error_label)

        submit_button = QtWidgets.QPushButton("Unlock")
        submit_button.pressed.connect(self.try_unlock)
        layout.addWidget(submit_button)

    def try_unlock(self):
        key = self.password_field.text()
        try:
            EncryptionKeyManager().unlock(key)
        except VaultLockedException:
            self.error_label.setText("Invalid password")
        else:
            self.parent().change_screen("otp")