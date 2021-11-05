class Calc:
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def dev(self, a, b):
        return a // b

# # 1.准备测试数据
# a = 6
# b = 5
# c = -11
#
# # 2.调用被测程序
# calc = Calc()
# sum = calc.add(a,b)
# # 3.判断期望结果与实际结果是否一致
# if c == sum:
#     print("用例通过！")
# else:
#     print("用户不通过！")
#     #将这个用例结果写入Excel
