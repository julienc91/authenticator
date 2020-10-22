# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from authenticator.ui.generic import (
    BlueButton,
    CheckBox,
    ErrorLabel,
    TextInput,
    TitleLabel,
)
from authenticator.vault.encryption import EncryptionKeyManager, VaultLockedException


class UnlockVaultForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(TitleLabel("Unlock the vault"))

        form_layout = QtWidgets.QFormLayout()
        self.password_field = TextInput(password=True)
        self.password_field.returnPressed.connect(self.try_unlock)
        form_layout.addRow(QtWidgets.QLabel("Password"), self.password_field)
        self.remember_checkbox = CheckBox("Remember")
        form_layout.addRow(self.remember_checkbox)
        layout.addLayout(form_layout)

        self.error_label = ErrorLabel()
        layout.addWidget(self.error_label)

        submit_button = BlueButton("Unlock")
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
