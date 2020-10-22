# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from authenticator.ui.generic import BlueButton, TextInput, TitleLabel
from authenticator.vault import interface
from authenticator.vault.session import SessionMaker


class AddOtpForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = None
        self._otp = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addWidget(TitleLabel("Add a new code"))

        form_layout = QtWidgets.QFormLayout()
        self.label_input = TextInput()
        self.label_input.textChanged.connect(self.update_label)
        self.issuer_input = TextInput()
        self.issuer_input.textChanged.connect(self.update_issuer)
        form_layout.addRow(QtWidgets.QLabel("Account name"), self.label_input)
        form_layout.addRow(QtWidgets.QLabel("Service name"), self.issuer_input)

        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()
        cancel_button = BlueButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        confirm_button = BlueButton("Save")
        confirm_button.clicked.connect(self.save)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)

        layout.addLayout(button_layout)

    def set_uri(self, uri):
        self.session = SessionMaker()
        self._otp = interface.add_otp(uri, self.session)
        self.refresh()

    def refresh(self):
        self.label_input.setText(self._otp.label)
        self.issuer_input.setText(self._otp.issuer)

    def update_label(self, value):
        interface.update_otp(self._otp, label=value)

    def update_issuer(self, value):
        interface.update_otp(self._otp, issuer=value)

    def cancel(self):
        self.session.rollback()
        self.parent().change_screen("otp")

    def save(self):
        self.session.commit()
        self.parent().change_screen("otp")
