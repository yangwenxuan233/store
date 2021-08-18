import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 绘制折线图 y = a*x + b
x = np.arange(0,21,0.1)
y = 0.5 * x + 1
y1 = np.sin(x)
plt.plot(x,y,'b--',label='函数f(x)=ax+b')  # b 蓝色 -- 虚线
plt.plot(x,y1,'r',label='函数sin')
plt.legend(loc='best')
plt.show()




