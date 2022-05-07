f = open(file="data.txt",mode="w+",encoding="utf-8")

f.write("静夜思")

f.flush() #将数据刷新到磁盘上

'''
    将咏鹅的数据，复制一份到D:\Data1.txt
'''

f = open(file="data.txt",mode="r+",encoding="utf-8")
f1 = open(file="D:\\data1.txt",mode="w+",encoding="utf-8")

data = f.read()

f1.write(data)
f1.flush()

f1.close()  # 关闭资源
f.close()



