import os
import time

import pyautogui
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 安全模式
pyautogui.FAILSAFE = True

time.sleep(3)

# 定位
location = pyautogui.locateCenterOnScreen(r'D:\pycode\ParaneterConfiguration\AutoClick\read_button.png')
print(location)

# 点击按钮
while True:
    pyautogui.click(location)
    # 操作间隔
    time.sleep(10)
