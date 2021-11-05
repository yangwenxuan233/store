import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 绘制柱状图
x = np.arange(1,13,1)
y = np.random.randint(30,120,size=(12,))
ax = plt.subplot()
bars = ax.bar(x,y,width=0.5)
ax.set_title('XXX销售部门月度销售额')
# RGB:#AAFFCC
for bar in bars:
    bar.set_color('#' + str(np.random.randint(100000,999999,size=(1,))[0]))
    pass
ax.set_xlabel('月份')
ax.set_ylabel('销售额（万/元）')
ax.set_xticks(x)
ax.set_xticklabels([str(i) + '月' for i in range(1,13,1)])
plt.text(1,3,'texttest')   # (横轴，纵轴，内容）
for xx,yy in zip(x,y):
    plt.text(xx,yy+0.5,'{0}万'.format(yy),ha='center',va='bottom')
    pass
plt.grid(linestyle='--')  # 网格线是虚线
ax.plot(x,y,'b--')
plt.show()
