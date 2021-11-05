import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = np.random.randint(1,100,size=(100,))
y = np.random.randint(1,100,size=(100,))

plt.scatter(x,y,c='r',marker='p',alpha=0.5)  # c 颜色 r红色  marker 形状 o 圆形 p 菱形 alpha 透明度
plt.show()
