import matplotlib.pyplot as plt
import os



def plot_histogram(matrix):
    plt.imshow(matrix, cmap='jet', origin='lower')
    plt.colorbar()
    plt.show()


class ReadPHD:

    def __init__(self, path):
        """open file"""
        self.__path = path
        __file = open(path)
        self.__file_content = __file.readlines()
        self.__file_content = [x.strip() for x in self.__file_content]
        __file.close()

    def __is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __end_block_search(self, start):
        while True:
            start += 1
            s = self.__file_content[start]
            if s.find('#') != -1 or s == 'STOP': # or s.rstrip() == '' removed becouse strip added in __init__
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
        if self.__file_content.count('#Collection'):
            ind = self.__file_content.index('#Collection')
            s = self.__file_content[ind + 1].split()
            return s
        else:
            print(f'In file {self.__path} #Collection not found')

    def get_acquisition(self):
        if self.__file_content.count('#Acquisition'
                                     ''):
            ind = self.__file_content.index('#Acquisition'
                                            '')
            s = self.__file_content[ind+1].split()
            return s
        else:
            print(f'In file {self.__path} #Acquisition not found')

    def get_calibration(self):
        if self.__file_content.count('#Calibration'
                                     ''):
            ind = self.__file_content.index('#Calibration'
                                            '')
            s = self.__file_content[ind + 1].split()
            return s
        else:
            print(f'In file {self.__path} #Calibration not found')

    def get_processing(self):
        if self.__file_content.count('#Processing'
                                     ''):
            start = self.__file_content.index('#Processing'
                                              '') + 1
            return [list(map(float, self.__file_content[i].split())) for i in range(start, start+3)]
        else:
            print(f'In file {self.__path} #Processing not found')

    def get_energy_g(self):
        if self.__file_content.count('#g_Energy'
                                     ''):
            start = self.__file_content.index('#g_Energy'
                                              '')+1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #g_Energy not found')

    def get_energy_b(self):
        if self.__file_content.count('#b_Energy'
                                     ''):
            start = self.__file_content.index('#b_Energy'
                                              '') + 1
            matrix = [self.__file_content[i].split() for i in range(start, self.__end_block_search(start))]
            [j.pop(1) for j in matrix]
            return [list(map(float, i)) for i in matrix]
        else:
            print(f'In file {self.__path} #b_Energy not found')

    def get_resolution_g(self):
        if self.__file_content.count('#g_Resolution'
                                     ''):
            start = self.__file_content.index('#g_Resolution'
                                              '') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #g_Resolution not found')

    def get_resolution_b(self):
        if self.__file_content.count('#b_Resolution'
                                     ''):
            start = self.__file_content.index('#b_Resolution'
                                              '') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #b_Resolution not found')

    def get_limits_roi(self):
        if self.__file_content.count('#ROI_Limits'
                                     ''):
            start = self.__file_content.index('#ROI_Limits'
                                              '') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #ROI_Limits not found')

    def get_efficiency_g(self):
        if self.__file_content.count('#g_Efficiency'
                                     ''):
            start = self.__file_content.index('#g_Efficiency'
                                              '') + 1
            return [list(map(float, self.__file_content[i].split()))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #g_Efficiency not found')

    def get_efficiency_b_g(self):
        if self.__file_content.count('#b-gEfficiency'
                                     ''):
            start = self.__file_content.index('#b-gEfficiency'
                                              '') + 1
            return [list(map(float, [j for j in self.__file_content[i].split() if self.__is_float(j)]))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #b-gEfficiency not found')

    def get_ratios(self):
        if self.__file_content.count('#Ratios'
                                     ''):
            start = self.__file_content.index('#Ratios'
                                              '') + 1
            return [list(map(float, [j for j in self.__file_content[i].split() if self.__is_float(j)]))
                    for i in range(start, self.__end_block_search(start))]
        else:
            print(f'In file {self.__path} #Ratios not found')

    def get_spectrum_g(self):
        if self.__file_content.count('#g_Spectrum'
                                     ''):
            ind = self.__file_content.index('#g_Spectrum'
                                            '')
            # return self.__mat_to_list(ind)
            return self.__mat_to_list(ind)
        else:
            print(f'In file {self.__path} #g_Spectrum not found')

    def get_spectrum_b(self):
        if self.__file_content.count('#b_Spectrum'
                                     ''):
            ind = self.__file_content.index('#b_Spectrum'
                                            '')
            return self.__mat_to_list(ind)
        else:
            print(f'In file {self.__path} #b_Spectrum not found')

    def get_histogram(self):
        if self.__file_content.count('#Histogram'
                                     ''):
            ind = self.__file_content.index('#Histogram'
                                            '')
            parse = self.__file_content[ind+1].split()
            matrix = [list(map(int, self.__file_content[ind+i+2].split())) for i in range(int(parse[0]))
                      if self.__file_content[ind+i+2]]
            return matrix
        else:
            print(f'In file {self.__path} #Histogram not found')


def safe_data(name, *args):
    path = 'E:/GitReps/MIX_NobleGas/ReadPHD/MIX/' + name + '.txt'
    _file = open(path, 'a+')
    for i in args:
        _file.write(str(i))
    _file.close()


def process_files():
    # E:/Work/MIX_Files/Phase A/Red/SAMPLE
    # for file in os.listdir("E:/Work/MIX_Files/2020 01-04/Blue"):
    #     temp = ReadPHD("E:/Work/MIX_Files/2020 01-04/Blue/" + file)
    #     collection = temp.get_collection()
    #     if temp.get_spectrum_qualifier() == 'FULL':
    #         safe_data('Blue1', collection[0], '\t', collection[4], '\n''
    #         ')
    path = "E:/Work/MIX_Files/Phase A/Red/SAMPLE"
    for file in os.listdir(path):
        temp = ReadPHD(path + '/' + file)
        collection = temp.get_collection()
        msg_id = temp.get_msg_id()
        srid = temp.get_srid()
        processing = temp.get_processing()
        # if temp.get_spectrum_qualifier() == 'FULL':
        if '2020/05/04' < collection[0] < '2020/05/10':
            safe_data('Red2', collection[0], '\t', collection[4], '\t', msg_id, '\t', processing[0][0], '\t', srid)


def main():
    spike = ReadPHD("SPIKE20190502222812845.PHD")
    # print(spike.get_ratios())
    # collection = spike.get_collection()
    # print(collection[0] > '2020/08/04')
    a = spike.get_histogram()
    plot_histogram(a)
    # process_files()

    # a = spike.get_data_type()
    # print(a)
    # str = spike.getTransmitDateTime().rstrip()
    # date_obj = datetime.datetime.strptime(str, '%Y/%m/%d %H:%M:%S.%f')

if __name__ == '__main__':
    main()
