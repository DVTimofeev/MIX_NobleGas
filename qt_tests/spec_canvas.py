from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure


class SpecCanvas(QWidget):
    def __init__(self,  parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.setLayout(vertical_layout)

    def clear(self):
        self.canvas.figure.clear()

