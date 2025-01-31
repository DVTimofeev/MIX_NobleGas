from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random

import matplotlib.pyplot as plt
import os

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
    return plt

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


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("qt_designer1.ui", self)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        self.pushButton_generate_random_signal.clicked.connect(self.update_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)
        self.MplWidget.canvas.axes.clear()

        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()
        print(type(self.MplWidget.canvas.axes))


app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()