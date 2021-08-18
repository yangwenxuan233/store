'''
    老手机：
        诺基亚：
            来电显示：手机号，彩铃
    新手机：
        华为：
            来电显示：手机号，铃声,大头贴，归属地

'''
import time
class Oldphone(object):
    phoneNumber = ""
    voice = ""

    def call(self,number):
        print(self.phoneNumber , "正在给",number ,"打电话，正在响铃",self.voice,",已接通：")
        for i in range(8):
            print(".",end="")
            time.sleep(1)

class NewPhone(Oldphone):
    picture = ""
    address = ""

    def call(self,number):
        # 1.手机号与彩铃这个功能交给老手机来运行
        super().call(number)

        # 2.大头贴与归属地交给新手机来显示
        print("来电号码归属于",self.address , "显示大头贴为：",self.picture)

phone = NewPhone()
phone.phoneNumber = "13552648187"
phone.voice = "凤凰传奇"
phone.address = "河北保定"
phone.picture = "野猪佩奇"

phone.call("15248458484")












