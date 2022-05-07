import time


class TextFile():
    def write_txt(path, list1, list2):
        # 文件以序列号+当前时间命名
        filename = str(list1[20]) + "_" + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        file = path + '/' + filename + ".txt"
        with open(file, 'a', encoding='utf-8') as f:
            for i in range(49):
                f.write(list1[i] + '   # ' + list2[i] + '\n')
            f.close()

    def read_txt(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = f.readlines()
            list = [i.rstrip() for i in [i[0] for i in [i.split('#') for i in data]]]
            f.close()
        return list
