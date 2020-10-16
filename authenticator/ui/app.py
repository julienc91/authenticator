# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

from .otp import OTPList


class AuthenticatorApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(OTPList())
        self.window.setLayout(layout)
        self.window.setMinimumWidth(380)
        self.window.setStyleSheet("background-color: black; color: white;")

    def run(self):
        self.window.show()
        self.app.exec_()
