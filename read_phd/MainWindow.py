import sys
from ReadPHD import  ReadPHD
from PyQt5 import QtWidgets, uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from MainForm import Ui_MainWindow

#Classes for ploting
from widgetmpl import WidgetMPL

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Загрузите страницу интерфейса
        # uic.loadUi('MainForm.ui', self)

        #
        spike = ReadPHD("I:\Learning\Projects\MIX_NobleGas\ReadPHD\SAMPLE20211203070613605.PHD")
        # # Гистограмма 256-256
        matrix = spike.get_histogram()
        fig, fig_plot = plt.subplots()

        # fig = plt.pcolormesh(matrix, cmap='jet')
        fig_plot.imshow(matrix, cmap='jet', origin='lower')


        # гамма спектр столбцами
        # index = list(range(0,256))
        # gamma = spike.get_spectrum_g()
        # print(index)
        # plt.bar(index, gamma, width=1)

        #линейный гамма спектр
        # index = list(range(0, 256))
        # gamma = spike.get_spectrum_g()
        # print(index)
        # plt.plot(index, gamma)

        # self.addToolBar(NavigationToolbar(self.canvas, self))

        # self.gamma_spectre = plt.figure()
        # self.head_plot = plt.figure()
        # self.canvas_gamma = WidgetMPL(fig)
        # self.heat.canvas = WidgetMPL()
        # print(type(self.head_plot))
        # print(type(self.canvas_heat))
        # print(type(1))
        # self.gammaspec.addWidget(self.canvas_gamma)
        # self.heatplot.addWidget(self.canvas_heat)
        # self.heatplot = self.canvas_heat
        # self.heat.canvas.axes.clear()
        # self.addToolBar(NavigationToolbar(self.heat.canvas, self))
        self.heat.canvas.axes.imshow(matrix, cmap='jet', origin='lower')
        # self.canvas_gamma.draw()
        # self.canvas.draw()
        # self.head_plot.imshow(matrix)
        # self.verticalLayout.heat.canvas.draw()
        # self.gammaspec.canvas.draw()
        self.heat.canvas.draw()
    # мы добавили метод plot(), который принимает два массива:
    # temperature и hour, затем строит данные с помощью метода graphWidget.plot().

    # def plot(self, hour, temperature):
    #     self.graphWidget.plot(hour, temperature)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
