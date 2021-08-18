'''
    // background 的相关配置
    "update.enableWindowsBackgroundUpdates": true,
    "background.customImages": [
        "file:///D:/Picture/vs_background.png"//图片地址
    ],
    "background.style": {
        "content":"''",
        "pointer-events":"none",
        "position":"absolute",//图片位置
        "width":"100%",
        "height":"100%",
        "z-index":"99999",
        "background.repeat":"no-repeat",
        "background-size":"20%,20%",//图片大小
        "opacity":0.3
         //透明度
    },
    "background.useFront": true,
    "background.useDefault": false,
    "backgroundCover.imagePath": "d:\\Picture\\background.jpg", //是否使用默认图片

'''
# import time


# def now_time():
#     return time.strftime("%Y-%m-%d")


# print(now_time())

# from selenium import webdriver
# import time

# # 创建谷歌浏览器对象
# chromeDriver = webdriver.Chrome()

# # 打开百度网址
# chromeDriver.get("http://www.baidu.com")

# # 窗口最大化
# chromeDriver.maximize_window()

# # 寻找搜索输入框
# chromeDriver.find_element_by_id("kw").send_keys("java")

# # 点击百度一下按钮
# chromeDriver.find_element_by_id("su").click()
# time.sleep(3)

# # 退出浏览器
# chromeDriver.quit()

