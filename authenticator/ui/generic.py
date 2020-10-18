# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets


class ScrollableItems(QtWidgets.QScrollArea):
    def __init__(self, children, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWidget(children)
        self.setWidgetResizable(True)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
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
