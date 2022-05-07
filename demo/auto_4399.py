import pyautogui
import time

# 安全模式
pyautogui.FAILSAFE = True

time.sleep(3)
for count in range(5000):
    region = (567, 556, 404, 40)
    im = pyautogui.screenshot(region=region)
    for i in range(50, 404, 100):
        px = im.getpixel((i, 20))
        print(px)
        if px[0] == 2:
            pyautogui.click(region[0] + i, region[1] + 20)
