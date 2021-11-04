class ReadSOH:

    def __init__(self, path):
        """open file"""
        self.__path = path
        __file = open(path)
        self.__file_content = __file.readlines()
        # self.__file_content = [s.replace('\"', '').replace('\n', '').split(';') for s in self.__file_content]
        __file.close()

    def get_msg_id(self):
        if self.__file_content[2].find('MSG_ID') != -1:
            s = self.__file_content[2].split()
            return s[1]
        else:
            print(f'In file {self.__path} No MSG_ID in file')

    def search_param(self, name):
        return [s for s in self.__file_content if s.count(name) != 0]

    def print(self):
        print(self.__file_content[6].replace('\"', '').split(';')[2])


def save_list_in_file(data_list, name, ext):
    save_file = open(f'MIX/{name}.{ext}', 'a+')
    for s in data_list:
        save_file.write(s)
    save_file.close()


def main():
    soh1 = ReadSOH("F:/Work/MIX_Files/MIX_09102019_22062020.csv")
    save_list_in_file(soh1.search_param("a4_fs1"), 'a4_fs1', 'csv')
    save_list_in_file(soh1.search_param("a4_fs2"), 'a4_fs2', 'csv')
    save_list_in_file(soh1.search_param("a4_fs3"), 'a4_fs3', 'csv')
    save_list_in_file(soh1.search_param("a4_fs4"), 'a4_fs4', 'csv')

    # print([soh1.search_param("a4_fs2")[i] for i in range(5)])
    # save_file.close()
    # soh1.print()
    # l = 'a1aw'.replace('1', 'A').replace('w', 'B')
    # print(l)
    # print('"05.01.2020 00:00:55";"PRESSURE";"a4_ps1";"1.420"\n'.count('a4_ps1'))


if __name__ == '__main__':
    main()