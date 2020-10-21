# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from authenticator.ui.generic import TitleLabel
from authenticator.vault.encryption import EncryptionKeyManager, VaultLockedException


class UnlockVaultForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(TitleLabel("Unlock the vault"))

        form_layout = QtWidgets.QFormLayout()
        self.password_field = QtWidgets.QLineEdit()
        self.password_field.returnPressed.connect(self.try_unlock)
        form_layout.addRow(QtWidgets.QLabel("Password"), self.password_field)
        self.remember_checkbox = QtWidgets.QCheckBox("Remember")
        form_layout.addRow(self.remember_checkbox)
        layout.addLayout(form_layout)

        self.error_label = QtWidgets.QLabel()
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        submit_button = QtWidgets.QPushButton("Unlock")
        submit_button.setStyleSheet(
            """
            background-color: #05B8CC; border: 1px solid #000; border-top: 20px solid #000; color: #fff;
        """
        )
        submit_button.pressed.connect(self.try_unlock)
        layout.addWidget(submit_button)

    def try_unlock(self):
        key = self.password_field.text()
        remember = self.remember_checkbox.isChecked()
        try:
            EncryptionKeyManager().unlock(key, remember=remember)
        except VaultLockedException:
            self.error_label.setText("Invalid password")
        else:
            self.parent().change_screen("otp")
