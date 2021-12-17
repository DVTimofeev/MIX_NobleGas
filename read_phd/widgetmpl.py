from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure


class WidgetMPL(QWidget):

    # def __init__(self, fig, parent=None):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self.fig = fig
        # # self.canvas = FigureCanvasQTAgg.__init__(self, self.fig)
        # self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas = FigureCanvasQTAgg(Figure())
        #
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.canvas)
        # #
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(horizontal_layout)
