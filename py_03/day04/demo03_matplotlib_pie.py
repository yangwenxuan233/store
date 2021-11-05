import matplotlib.pyplot as plt
import numpy as np
# 正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
# 正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# 编程语言的行业占有率
ax = plt.subplot()
ax.set_title('编程语言占比')
pl = ['java','c','c++','python']
data = [500,300,300,400]
# labels = [type + '' + '{0}%'.format(x/np.sum(data)*100) for type,x in zip(pl,data)]

# 保留小数点后两位
labels = [type + '' + '%.2f%%' % (x/np.sum(data)*100) for type,x in zip(pl,data)]
plt.pie(data,labels=labels,explode=[0,0.3,0,0])  # explode突出重点[距离]
plt.show()
