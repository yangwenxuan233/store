import struct


class DataStruct():
    '''解包部分'''
    # 数据分割
    def read_generator(data, dict):
        for i in dict:
            yield data[0: dict[i]]
            data = data[dict[i]:]

    # 1个字节转制
    def struct_unpack_one(data):
        Data = struct.unpack('>B', data)
        return str(Data[0])

    # 2个字节转制
    def struct_unpack_two(data):
        m1 = data[0]
        m2 = data[1]
        MUN = m2 * 256 + m1
        return str(MUN)

    def struct_unpack_two_APD_Vol(data):
        m1 = data[0]
        m2 = data[1]
        MUN = m2 * 256 + m1
        DATA = ~(-1 & 0xffff ^ int(hex(MUN), 16))
        if MUN < 30000:
            return str(MUN)
        else:
            return str(DATA)

    def struct_unpack_four(data):
        num = []
        for i in range(4):
            m = str(data[i])
            if len(m) == 1:
                m = '0' + m
            num.append(m)
        NUM = ''.join(num)
        return NUM

    def struct_inpack_ip(data):
        m1 = str(data[0])
        if len(m1) < 3:
            m1 = (3 - len(m1)) * ('0') + m1
        m2 = str(data[1])
        if len(m2) < 3:
            m2 = (3 - len(m2)) * ('0') + m2
        m3 = str(data[2])
        if len(m3) < 3:
            m3 = (3 - len(m3)) * ('0') + m3
        m4 = str(data[3])
        if len(m4) < 3:
            m4 = (3 - len(m4)) * ('0') + m4
        ip = [m1, ' . ', m2, ' . ', m3, ' . ', m4]
        NUM = ''.join(ip)
        return NUM

    # 6个字节转制
    def struct_unpack_six(data):
        num = []
        for i in range(6):
            m = str(data[i])
            if len(m) == 1:
                m = '0' + m
            num.append(m)
        NUM = ''.join(num)
        return NUM

    def struct_unpack_sn(data):
        m1 = chr(data[0])
        m2 = chr(data[1])
        m3 = chr(data[2])
        m4 = chr(data[3])
        m5 = chr(data[4])
        m6 = chr(data[5])
        m7 = chr(data[6])
        m8 = chr(data[7])
        m9 = chr(data[8])
        m10 = chr(data[9])
        m11 = chr(data[10])
        m12 = chr(data[11])
        m13 = chr(data[12])
        NUM = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8 + m9 + m10 + m11 + m12 + m13
        return NUM

    def struct_unpack_mac(data):
        m1 = hex(data[0])
        if m1.startswith('0x'):
            m1 = m1[2:]
        if len(str(m1)) == 1:
            m1 = '0' + str(m1)
        m2 = hex(data[1])
        if m2.startswith('0x'):
            m2 = m2[2:]
        if len(str(m2)) == 1:
            m2 = '0' + str(m2)
        m3 = hex(data[2])
        if m3.startswith('0x'):
            m3 = m3[2:]
        if len(str(m3)) == 1:
            m3 = '0' + str(m3)
        m4 = hex(data[3])
        if m4.startswith('0x'):
            m4 = m4[2:]
        if len(str(m4)) == 1:
            m4 = '0' + str(m4)
        m5 = hex(data[4])
        if m5.startswith('0x'):
            m5 = m5[2:]
        if len(str(m5)) == 1:
            m5 = '0' + str(m5)
        m6 = hex(data[5])
        if m6.startswith('0x'):
            m6 = m6[2:]
        if len(str(m6)) == 1:
            m6 = '0' + str(m6)
        mac = m1 + ' : ' + m2 + ' : ' + m3 + ' : ' + m4 + ' : ' + m5 + ' : ' + m6
        NUM = ''.join(mac)
        return NUM

    # 8个字节转制
    def struct_unpack_eight(data):
        Data = struct.unpack('>Q', data)
        return Data

    '''打包部分'''
    # 数据长度生成器
    def lenth_generator(dict):
        for i in dict:
            yield [i, dict[i]]

    # 转制1个字节
    def struct_pack_one(data):
        Data = struct.pack('>B', int(data))
        return Data

    def struct_pack_two(data):
        m = bin(int(data, 10) & 0xffff)
        n = int(m, 2)
        m1 = struct.pack('>B', int(int(n) // 256))
        m2 = struct.pack('>B', int(int(n) % 256))
        MUN = m2 + m1
        return MUN

    # 转制4个字节
    def struct_pack_four(data):
        num = data
        m1 = struct.pack('>B', int(num[0: 2]))
        m2 = struct.pack('>B', int(num[2: 4]))
        m3 = struct.pack('>B', int(num[4: 6]))
        m4 = struct.pack('>B', int(num[6: 8]))
        Data = m1 + m2 + m3 + m4
        return Data

    def struct_pack_four_ip(data):
        mun = data
        m1 = struct.pack('>B', int(mun[0: 3]))
        m2 = struct.pack('>B', int(mun[6: 9]))
        m3 = struct.pack('>B', int(mun[12: 15]))
        m4 = struct.pack('>B', int(mun[18: 21]))
        Data = m1 + m2 + m3 + m4
        return Data

    # 转制6个字节
    def struct_pack_six(data):
        num = data
        m1 = struct.pack('>B', int(num[0: 2]))
        m2 = struct.pack('>B', int(num[2: 4]))
        m3 = struct.pack('>B', int(num[4: 6]))
        m4 = struct.pack('>B', int(num[6: 8]))
        m5 = struct.pack('>B', int(num[8: 10]))
        m6 = struct.pack('>B', int(num[10: 12]))
        Data = m1 + m2 + m3 + m4 + m5 + m6
        return Data

    def struct_pack_mac(data):
        mun = data
        m1 = struct.pack('>B', int(mun[0: 2], 16))
        m2 = struct.pack('>B', int(mun[5: 7], 16))
        m3 = struct.pack('>B', int(mun[10: 12], 16))
        m4 = struct.pack('>B', int(mun[15: 17], 16))
        m5 = struct.pack('>B', int(mun[20: 22], 16))
        m6 = struct.pack('>B', int(mun[25: 27], 16))
        Data = m1 + m2 + m3 + m4 + m5 + m6
        return Data

    def struct_pack_sn(data):
        m1 = struct.pack('>B', ord(data[0]))
        m2 = struct.pack('>B', ord(data[1]))
        m3 = struct.pack('>B', ord(data[2]))
        m4 = struct.pack('>B', ord(data[3]))
        m5 = struct.pack('>B', ord(data[4]))
        m6 = struct.pack('>B', ord(data[5]))
        m7 = struct.pack('>B', ord(data[6]))
        m8 = struct.pack('>B', ord(data[7]))
        m9 = struct.pack('>B', ord(data[8]))
        m10 = struct.pack('>B', ord(data[9]))
        m11 = struct.pack('>B', ord(data[10]))
        m12 = struct.pack('>B', ord(data[11]))
        m13 = struct.pack('>B', ord(data[12]))
        Data = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8 + m9 + m10 + m11 + m12 + m13
        return Data

    # 转制8个字节
    def struct_pack_eight(data):
        Data = struct.pack('>Q', data)
        return Data
