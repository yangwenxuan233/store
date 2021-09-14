import pyautogui
import time

# 安全模式
pyautogui.FAILSAFE = True

time.sleep(3)
for count in range(500):
    region = (567, 556, 404, 40)
    im = pyautogui.screenshot(region=region)
    im.save('test.png')
    for i in range(50, 404, 100):
        px = im.getpixel((i, 20))
        print(px)
        if px[0] == 1:
            pyautogui.click(region[0] + i, region[1] + 20)
