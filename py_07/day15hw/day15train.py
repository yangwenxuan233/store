import pymysql

# 1.以下文件是用户的一些数据（姓名、年龄、净资产），要求使用数据库工具将文件中的数据写入到数据库中。并统计所有人的资产总和！
f1 = open(r"D:\pycode\py202107\day15hw\用户数据.txt", mode="r+", encoding="ANSI")

'''
create table user(
    `username` varchar(50),
    `age` varchar(50),
    `property` varchar(50)
);
'''


# 写入数据库
def db_write(param):
    con = pymysql.connect(host="localhost", user="root", password="root", database="new_schema", charset="utf8")
    cursor = con.cursor()  # 数据库连接
    sql = "insert into `user` values(%s, %s, %s)"
    cursor.execute(sql, param)
    con.commit()
    cursor.close()
    con.close()


# data = f1.readlines()
# list1 = [i.replace("\n", "") for i in data]
# list2 = list([i.split(",") for i in list1])
sum = 0
for i in [i.split(",") for i in [i.replace("\n", "") for i in f1.readlines()]]:
    db_write(i)
    sum += int(i[2])

# 所有人资产总和
print(sum)

f1.close()


# 2.使用python复制一张图片到D盘的python文件夹里。
f2 = open(r"D:\pycode\py202107\day15hw\image\大美女.jpg", mode="rb")
f3 = open(r"D:\python\大美女.jpg", mode="wb")
data = f2.read()
f3.write(data)
f3.flush()
f2.close()
f3.close()


# 3.编写程序模拟证件上传的功能，让用户输入证件的路径，并拷贝到一个统一的图片路径下。
def copy_file(origin_path, target_path):
    p1 = open(origin_path, mode="rb")
    p2 = open(target_path, mode="wb")
    data = p1.read()
    p2.write(data)
    p2.flush()
    p1.close()
    p2.close()


copy_file(r"D:\pycode\py202107\day15hw\image\大美女.jpg", r"D:\python\大美女.jpg")


# 4.编程实现：有names.txt文件，实现用户的注册，登陆，修改密码，上传头像并记录头像路径的功能。
class User():

    # 将txt文件中的数据去掉换行符，以，隔开，判断非空，按行存入列表。
    def read_data(self):
        file = open(r"D:\pycode\py202107\day15hw\names.txt", mode="r+", encoding="utf-8")
        data = []
        lines = [i.split(",") for i in [i.strip('\n') for i in file.readlines()]]
        for i in lines:
            if i[0] != "":
                data.append(i)
        file.close()
        return data

    # 在txt文件末尾增添数据
    def add_data(self, name, password, sex, age, address):
        file = open(r"D:\pycode\py202107\day15hw\names.txt", mode="a+", encoding="utf-8")
        file.write(name + "," + password + "," + sex + "," + age + "," + address + "," + " " + "\n")
        file.flush()
        file.close()

    # 将更改后的数据按行写入txt文件
    def change_data(self, data):
        file = open(r"D:\pycode\py202107\day15hw\names.txt", mode="w+", encoding="utf-8")
        for i in data:
            file.write(i[0] + "," + i[1] + "," + i[2] + "," + i[3] + "," + i[4] + "," + i[5] + "\n")
        file.flush()
        file.close()

    # 注册，不输入头像路径
    def sige_up(self, name, password, sex, age, address):
        data = self.read_data()
        status = 0
        for i in data:
            if name in i:
                status += 1
        if status == 0 or data:
            self.add_data(name, password, sex, age, address)
            print("注册成功")
            return

    # 登录，仅判断名字和密码是否对应
    def log_in(self, name, password):
        data = self.read_data()
        for i in data:
            if all([name == i[0], password == i[1]]):
                print("登录成功")
                return

    # 修改密码，修改特定行密码后重写文件
    def change_password(self, name, password, new_password):
        data = self.read_data()
        for i in data:
            if all([name == i[0], password == i[1]]):
                i[1] = new_password
                print("修改密码成功")
                break
        self.change_data(data)

    # 上传头像，重写txt文件记录图片路径并复制到指定路径，视为上传
    def upload_image(self, name, password, image_path, target_path, image_name):
        data = self.read_data()
        for i in data:
            if all([name == i[0], password == i[1]]):
                try:
                    i[5] = image_path + image_name
                    self.copy_file(image_path, target_path, image_name)
                    print("头像上传成功")
                finally:
                    break
        self.change_data(data)

    # 复制图片到指定路径
    def copy_file(self, origin_path, target_path, image_name):
        p1 = open(origin_path + image_name, mode="rb")
        p2 = open(target_path + image_name, mode="wb")
        data = p1.read()
        p2.write(data)
        p2.flush()
        p1.close()
        p2.close()


user = User()
user.sige_up('俞敏洪', "admin", "男", "23", "北京市昌平区沙河北大桥桥底下")
user.log_in('俞敏洪', "admin")
user.change_password("俞敏洪", "admin", "123456")
user.upload_image("俞敏洪", "123456", r"D:\pycode\py202107\day15hw\day15", r"D:\pycode\py202107\day15hw\image", r"\大美女.jpg")


# 5.现在有这样一个叫scores.txt的文件，里面有赫敏、哈利、罗恩、马尔福四个人的几次魔法作业的成绩。
# 但是呢，因为有些魔法作业有一定难度，教授不强制同学们必须上交，所以大家上交作业的次数并不一致。
file_read = open(r"D:\pycode\py202107\day15hw\scores.txt", mode="r+", encoding="utf-8")
file_write = open(r"D:\pycode\py202107\day15hw\scores_final.txt", mode="w+", encoding="utf-8")

data = [i.split(" ") for i in [i.strip('\n') for i in file_read.readlines()]]

new_data = []
for i in data:
    list = []
    sum = 0
    list.append(i[0])
    for j in range(1, len(i)):
        sum += int(i[j])
    list.append(str(sum))
    new_data.append(list)

for i in new_data:
    file_write.write(i[0] + " " + i[1] + "\n")
