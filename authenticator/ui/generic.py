# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class ScrollableItems(QtWidgets.QScrollArea):
    def __init__(self, children, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWidget(children)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setStyleSheet(
            """
            QScrollBar::handle:vertical {
                background-color: #05B8CC;
                border-radius: 5px;
                height: 50px;
                width: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                color: none;
                height: 0;
                width: 0;
            }
        """
        )
        QtWidgets.QScroller.grabGesture(
            self.viewport(), QtWidgets.QScroller.LeftMouseButtonGesture
        )


class TitleLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setPixelSize(20)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setContentsMargins(0, 0, 0, 30)


class BlueButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(
            "background-color: #05B8CC; border: 1px solid #000; border-top: 20px solid #000; color: #fff;"
        )


class TextInput(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        is_password = kwargs.pop("password", False)
        icon = kwargs.pop("icon", None)
        super().__init__(*args, **kwargs)

        if is_password:
            self.setEchoMode(self.Password)

        if icon:
            icon = QtGui.QIcon(icon)
            self.addAction(icon, self.LeadingPosition)

        self.setStyleSheet(
            "background-color: #fff; border: 1px solid #05B8CC; color: #000;"
        )


class ErrorLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("color: #f00;")
        self.setFixedHeight(self.minimumSizeHint().height())


class CheckBox(QtWidgets.QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(
            """
            QCheckBox::indicator:checked { background-color: #05B8CC; border: 1px solid #fff; color: #000; }
            QCheckBox::indicator:unchecked { background-color: #000; border: 1px solid #fff; color: #fff; }
        """
        )
