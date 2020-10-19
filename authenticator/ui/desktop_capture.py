# -*- coding: utf-8 -*-

import tempfile
from typing import Optional

import mss
from mss.tools import to_png
from PyQt5 import QtCore, QtWidgets

import vault.interface


class DesktopCapture(QtWidgets.QFrame):
    TOOLBAR_HEIGHT_MARGIN = 15

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("root")
        self.setStyleSheet(
            """
            QFrame { border: 20px solid #000; }
            QLabel { background-color: #000; color: #fff; }
            QPushButton { background-color: #05B8CC; border: 1px solid #000; border-top: 20px solid #000; color: #fff; }
        """
        )

        texts = [
            "Move the window above the QR Code to scan.",
            "Resize the window if necessary.",
        ]

        self.capture_zone = QtWidgets.QWidget()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        def add_label(text=""):
            label = QtWidgets.QLabel(text)
            label.setFixedHeight(25)
            label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(label)
            return label

        for t in texts:
            add_label(t)

        layout.addWidget(self.capture_zone)

        self.error_label = add_label()

        button_layout = QtWidgets.QHBoxLayout()

        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        scan_button = QtWidgets.QPushButton("Scan")
        scan_button.clicked.connect(self.capture)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(scan_button)
        layout.addLayout(button_layout)

    @staticmethod
    def get_main_window() -> Optional[QtWidgets.QMainWindow]:
        app = QtWidgets.QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QtWidgets.QMainWindow):
                return widget
        return None

    def cancel(self):
        self.parent().change_screen("otp")

    def capture(self):
        from .. import qr_code

        main_window = self.get_main_window()
        absolute_coordinates = main_window.pos()
        relative_coordinates = self.capture_zone.pos()

        x = absolute_coordinates.x() + relative_coordinates.x()
        y = (
            absolute_coordinates.y()
            + relative_coordinates.y()
            + QtWidgets.QStyle.PM_TitleBarHeight
            # PM_TitleBarHeight is not always accurate (on Linux for instance), add a margin
            # to make sure we get the entire capture zone
            + self.TOOLBAR_HEIGHT_MARGIN
        )
        h = self.capture_zone.height()
        w = self.capture_zone.width()

        coordinates = {"top": y, "left": x, "width": w, "height": h}
        with mss.mss() as screen_capture:
            img = screen_capture.grab(coordinates)

        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            to_png(img.rgb, img.size, output=f.name)
            data = qr_code.read(f.name)

        if not data:
            self.error_label.setText("No QR Code detected")
        elif not vault.interface.is_uri_valid(data):
            self.error_label.setText("This QR Code is not valid")
        else:
            self.error_label.setText("")
            self.parent().change_screen("add_otp", **{"uri": data})
