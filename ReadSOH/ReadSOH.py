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
    # save_list_in_file(soh1.search_param("a4_fs1"), 'sec/date', 'csv')
    # save_list_in_file(soh1.search_param("a4_fs2"), 'sec/a4_fs2', 'csv')
    # save_list_in_file(soh1.search_param("a4_fs3"), 'sec/a4_fs3', 'csv')
    # save_list_in_file(soh1.search_param("a4_fs4"), 'sec/a4_fs4', 'csv')
    # a = soh1.search_param("a4_fs1")[1].replace('\"', '')
    # date_l_old = [b.replace('\"', '').split(';')[0].split('.') for b in soh1.search_param("a4_fs1")]
    # for a in date_l_old:
    #     a[0], a[1] = a[1], a[0]
    #
    # date_l_new = [s[0] + '.' + s[1] + '.' + s[2] + '\n' for s in c]
    open_file = open('MIX/flow_data.txt')
    flow_list = open_file.readlines()
    flow_list = [s.split(';') for s in flow_list]
    result = []
    for l in flow_list:
        result.append(l[0]+'\n')
        result.append(l[1])

    save_list_in_file(result, 'flowlist2', 'csv')


if __name__ == '__main__':
    main()