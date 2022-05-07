#  Python3 和 Python2 之间的区别？
#  python3采用更加严格的缩进，废除了一些命令语句，改为函数形式执行，也修改了部分语法
#  python3和python2并不兼容，python3对很多库进行了重构和修改，python2的代码需要做一些修改才能能在3.x环境下运行

#  标识符	 是否合法	标识符	是否合法
#  char		 是        Cy%ty	否
#  Oax_li	 是	       $123	    否
#  fLul		 是        3_3 	    否
#  BYTE		 是        T_T	    否

import numpy as np

a = 56
b = 78
a = b - a
b = b - a
a = a + b
print("a=", a, "b=", b, "\n")

stu1 = 45
stu2 = 23
print("stu1+stu2=", stu1 + stu2, "\n")

array1 = np.random.randint(5, size=5)
print(array1)
print("五个数的和=", array1.sum(axis=0))
print("五个数的平均数=", array1.mean(axis=0), "\n")

num1 = 45
num2 = 0
num2 = num1
print("num2=", num2)
