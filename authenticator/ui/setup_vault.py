# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from authenticator.ui.generic import (
    BlueButton,
    CheckBox,
    ErrorLabel,
    TextInput,
    TitleLabel,
)
from authenticator.vault.encryption import EncryptionKeyManager


class SetupVaultForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(TitleLabel("Setup your vault"))

        form_layout = QtWidgets.QFormLayout()
        self.password_field = TextInput(password=True)
        self.password_field.returnPressed.connect(self.create_vault)
        form_layout.addRow(QtWidgets.QLabel("Password"), self.password_field)
        self.remember_checkbox = CheckBox("Remember")
        form_layout.addRow(self.remember_checkbox)
        layout.addLayout(form_layout)

        self.error_label = ErrorLabel()
        layout.addWidget(self.error_label)

        submit_button = BlueButton("Create")
        submit_button.pressed.connect(self.create_vault)
        layout.addWidget(submit_button)

    def create_vault(self):
        key = self.password_field.text()
        remember = self.remember_checkbox.isChecked()
        if not key:
            self.error_label.setText("Setting a password is required")
            return

        EncryptionKeyManager().unlock(key, remember=remember)
        self.parent().change_screen("otp")
