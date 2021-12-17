import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def plot_histogram():
    spike = ReadPHD("SPIKE20190502222812845.PHD")
    matrix = spike.get_histogram()
    plt.pcolormesh(matrix, cmap='jet')
    plt.colorbar()
    # plt.show()


class ReadPHD:

    def __init__(self, path):
        """open file"""
        self.__path = path
        __file = open(path)
        self.__file_content = __file.readlines()
        __file.close()

    def __end_block_search(self, start):
        while True:
            start += 1
            s = self.__file_content[start]
            if s.find('#') != -1 or s.rstrip() == '' or s == 'STOP\n':
                return start

    def __mat_to_list(self, ind):
        return [int(counts) for i in range(ind + 2, self.__end_block_search(ind + 1))
                for counts in [self.__file_content[i].split()[j]
                               for j in range(len(self.__file_content[i].split())) if j != 0]]

    def get_msg_id(self):
        if self.__file_content[2].find('MSG_ID') != -1:
            s = self.__file_content[2].split()
            return s[1]
        else:
            print(f'In file {self.__path} No MSG_ID in file')

    def get_data_type(self):
        if self.__file_content[3].find('DATA_TYPE') != -1:
            s = self.__file_content[3].split()
            return s[1]
        else:
            print(f'In file {self.__path} No DATA_TYPE in file')

    def get_system_code(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 1].split()
                return s[0]
        print(f'In file {self.__path} #Header not found')

    def get_detector_code(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 1].split()
                return s[1]
        print(f'In file {self.__path} #Header not found')

    def get_system_type(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 1].split()
                return s[2]
        print(f'In file {self.__path} #Header not found')

    def get_system_geometry(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 1].split()
                return s[3]
        print(f'In file {self.__path} #Header not found')

    def get_spectrum_qualifier(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 1].split()
                return s[4]
        print(f'In file {self.__path} #Header not found')

    def get_srid(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                return self.__file_content[ind + 2]
        print(f'In file {self.__path} #Header not found')

    def get_file_msg_id(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 3].split()
                return s[0]
        print(f'In file {self.__path} #Header not found')

    def get_detbk_msg_id(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 3].split()
                return s[1]
        print(f'In file {self.__path} #Header not found')

    def get_gasbk_msg_id(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                s = self.__file_content[ind + 3].split()
                return s[2]
        print(f'In file {self.__path} #Header not found')

    def get_transmit_date_time(self):
        for s in self.__file_content:
            if s.find('#Header') != -1:
                ind = self.__file_content.index(s)
                return self.__file_content[ind + 4]
        print(f'In file {self.__path} #Header not found')

    def get_collection(self):
        if self.__file_content.count('#Collection\n'):
            ind = self.__file_content.index('#Collection\n')
            s = self.__file_content[ind + 1].split()
            return s
        else:
            print(f'In file {self.__path} #Collection not found')

    def get_acquisition(self):
        if self.__file_content.count('#Acquisition\n'):
            ind = self.__file_content.index('#Acquisition\n')
            s = self.__file_content[ind+1].split()
            return s
        else:
            print(f'In file {self.__path} #Acquisition not found')

    def get_calibration(self):
        if self.__file_content.count('#Calibration\n'):
            ind = self.__file_content.index('#Calibration\n')
            s = self.__file_content[ind + 1].split()
            return s
        else:
            print(f'In file {self.__path} #Calibration not found')

    def get_processing(self):
        if self.__file_content.count('#Processing\n'):
            start = self.__file_content.index('#Processing\n') + 1
            return [list(map(float, self.__file_content[i].split())) for i in range(start, start+3)]
        else:
            print(f'In file {self.__path} #Processing not found')

    def get_energy_g(self):
        if self.__file_content.count('#g_Energy\n'):
            start = self.__file_content.index('#g_Energy\n')+1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #g_Energy not found')

    def get_energy_b(self):
        if self.__file_content.count('#b_Energy\n'):
            start = self.__file_content.index('#b_Energy\n') + 1
            matrix = [self.__file_content[i].split() for i in range(start, self.__end_block_search(start))]
            [j.pop(1) for j in matrix]
            return [list(map(float, i)) for i in matrix]
        else:
            print(f'In file {self.__path} #b_Energy not found')

    def get_resolution_g(self):
        if self.__file_content.count('#g_Resolution\n'):
            start = self.__file_content.index('#g_Resolution\n') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #g_Resolution not found')

    def get_resolution_b(self):
        if self.__file_content.count('#b_Resolution\n'):
            start = self.__file_content.index('#b_Resolution\n') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #b_Resolution not found')

    def get_limits_roi(self):
        if self.__file_content.count('#ROI_Limits\n'):
            start = self.__file_content.index('#ROI_Limits\n') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #ROI_Limits not found')

    def get_efficiency_g(self):
        if self.__file_content.count('#g_Efficiency\n'):
            start = self.__file_content.index('#g_Efficiency\n') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #g_Efficiency not found')

    def get_efficiency_b_g(self):
        if self.__file_content.count('#b-gEfficiency\n'):
            start = self.__file_content.index('#b-gEfficiency\n') + 1
            return [list(map(float, [j for j in self.__file_content[i].split() if is_float(j)]))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #b-gEfficiency not found')

    def get_ratios(self):
        if self.__file_content.count('#Ratios\n'):
            start = self.__file_content.index('#Ratios\n') + 1
            return [list(map(float, [j for j in self.__file_content[i].split() if isinstance(float(j), float)]))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #Ratios not found')

    def get_spectrum_g(self):
        if self.__file_content.count('#g_Spectrum\n'):
            ind = self.__file_content.index('#g_Spectrum\n')
            # return self.__mat_to_list(ind)
            return self.__mat_to_list(ind)
        else:
            print(f'In file {self.__path} #g_Spectrum not found')

    def get_spectrum_b(self):
        if self.__file_content.count('#b_Spectrum\n'):
            ind = self.__file_content.index('#b_Spectrum\n')
            return self.__mat_to_list(ind)
        else:
            print(f'In file {self.__path} #b_Spectrum not found')

    def get_histogram(self):
        if self.__file_content.count('#Histogram\n'):
            ind = self.__file_content.index('#Histogram\n')
            parse = self.__file_content[ind+1].split()
            matrix = [list(map(int, self.__file_content[ind+i+2].split())) for i in range(int(parse[0]))
                      if self.__file_content[ind+i+2]]
            return matrix
        else:
            print(f'In file {self.__path} #Histogram not found')


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Загрузите страницу интерфейса
        uic.loadUi('qt_designer.ui', self)
        self.fig = plt.figure()

        self.canvas = FigureCanvasQTAgg(self.fig)

        # grid = QtWidgets.QGridLayout(self.centralwidget)
        # grid.addWidget(self.graphWidget, 0, 0)
        self.gridLayout.addWidget(self.canvas)
        # self.graphWidget = self.canvas
        # grid.addWidget(self.canvas)
        print(type(self.gridLayout))
        a = QHBoxLayout()
        print(type(a))
        spike = ReadPHD("I:/Learning/Projects/MIX_NobleGas/read_phd/SAMPLE20211203070613605.PHD")
        # Гистограмма 256-256
        matrix = spike.get_histogram()

        # plt.pcolormesh(matrix, cmap='jet')
        # plt.pcolormesh(matrix, cmap='jet')
        # fig = plt.pcolormesh(matrix, cmap='jet')
        plt.imshow(matrix, cmap='jet', origin='lower')
        plt.colorbar()
        # _, test1 = plt.subplots()
        # print (type(test1))
        # test1.matshow(matrix)
        # print(type(test1))
        # plt.show()
        # test1 = plt.subplots()
        # print(type(test1))
        #
        # # гамма спектр столбцами
        # # index = list(range(0,256))
        # # gamma = spike.get_spectrum_g()
        # # print(index)
        # # plt.bar(index, gamma, width=1)
        #
        # #линейный гамма спектр
        # # index = list(range(0, 256))
        # # gamma = spike.get_spectrum_g()
        # # print(index)
        # # plt.plot(index, gamma)
        #
        self.addToolBar(NavigationToolbar(self.canvas, self))
        #
        # # self.canvas.figure.show()
        # # self.canvas.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
        self.canvas.draw()
    # мы добавили метод plot(), который принимает два массива:
    # temperature и hour, затем строит данные с помощью метода graphWidget.plot().

    # def plot(self, hour, temperature):
    #     self.graphWidget.plot(hour, temperature)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())