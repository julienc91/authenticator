# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets


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
