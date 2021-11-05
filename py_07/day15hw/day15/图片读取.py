
f = open(file="大美女.jpg",mode="rb")
f1 = open(file="d:\\大美女.jpg",mode="wb")
data = f.read()

f1.write(data)

f1.flush()
f1.close()
f.close()


print(data)






