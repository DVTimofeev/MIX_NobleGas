from ReadPHD import ReadPHD
import matplotlib.pyplot as plt
import sys
from PyQt5 import uic, Qt
from PyQt5.QtWidgets import *
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)


class SnappingNavigationToolbar(NavigationToolbar):
    """Navigation toolbar with data snapping"""

    def __init__(self, canvas, parent, coordinates=True):
        super().__init__(canvas, parent, coordinates)

    def on_press(self, event):
        if self.mode == '':
            print('mouse pressed')
            MainWindow.draw_vertical_line(main, x=event.xdata)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        # initialization of parameters
        self.__param_init()
        # initialization of parent class MainWindow
        super(MainWindow, self).__init__(*args, **kwargs)
        # Loading user interface from QtDesigner
        uic.loadUi('double_plots.ui', self)
        self._draw_plots()
        self.specs.canvas.mpl_connect('button_press_event', self.toolbar.on_press)
        self.browse.clicked.connect(self.browsefiles)

    def __param_init(self):
        """Base initialization of parameters"""
        # X axis for g_spectre (default = 256)
        self.index = list(range(0, 256))
        # zero sheet for g_spectre
        self.g_spectre = [0 for _ in self.index]
        # zero sheet for histogram
        self.histogram = [self.g_spectre for _ in self.index]
        # PHD file
        # self.test_phd = None
        # self.roi = None
        # other
        # self.fig = None
        # self.ax1 = None
        # self.ax2 = None
        self.y_max = 0
        self.vertical_lines_count = 0

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', '...')
        self.file_url.setText(fname[0])
        self.open_file(fname[0])

    def _draw_plots(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})
        self.fig.subplots_adjust(left=0.05, right=0.99, wspace=0.1, hspace=0.1)
        self._update_draw()
        self.specs.canvas.figure = self.fig
        self.toolbar = SnappingNavigationToolbar(self.specs.canvas, self)
        self.addToolBar(self.toolbar)

    def _update_draw(self):
        self.y_max = max(self.g_spectre)
        self.ax1.clear()
        self.ax2.clear()
        self.specs.canvas.figure = self.fig
        self.ax2.imshow(self.histogram, cmap='jet', origin='lower')
        self.ax2.set_title('Histogram')
        index = list(range(0, 256))
        self.ax1.bar(index, self.g_spectre, width=1)
        self.ax1.set_title('G-Spectre')
        self.ax1.set_xlim(0, 256)
        self.specs.canvas.draw()

    def draw_vertical_line(self, x):
        if self.vertical_lines_count == 2:
            self.vertical_lines_count = 0
            self._update_draw()
        else:
            self.fig.axes[0].vlines(x, 0, self.y_max, colors='#ffbb11')
            self.specs.canvas.draw()
            self.vertical_lines_count += 1

    def open_file(self, url):
        self.test_phd = ReadPHD(url)
        self.histogram = self.test_phd.get_histogram()
        self.g_spectre = self.test_phd.get_spectrum_g()
        self._update_draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

    # test_PHD = ReadPHD("I:/Learning/Projects/MIX_NobleGas/read_phd/SAMPLE20211203070613605.PHD")
    # roi = test_PHD.get_ratios()
    # histogram = test_PHD.get_histogram()
    # g_spectre = test_PHD.get_spectrum_g()
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig.subplots_adjust(wspace=0.4, hspace=0.6)
    # ax2.imshow(histogram, cmap='jet', origin='lower')
    # ax2.set_title('Histogram')
    # # ax2.set_xlim(0, 256)
    # # ax2.set_ylim(0, 256)
    # ax2.hlines(20, 20, 40, colors='green')
    # ax2.vlines(20, 20, 40, colors='#ffbb11')
    # index = list(range(256))
    #
    # ax1.bar(index, g_spectre, width=1)
    # ax1.set_title('G-Spectre')
    # # ax1.set_xlim(0, 256)
    # # ax1.set_ylim(0, 10000)
    # plt.show()
