import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,1,2)
# ax1
pl = ['java','c','c++','python']
data = [500,300,300,400]
# labels = [type + '' + '{0}%'.format(x/np.sum(data)*100) for type,x in zip(pl,data)]
# 保留小数点后两位
labels = [type + '' + '%.2f%%' % (x/np.sum(data)*100) for type,x in zip(pl,data)]
ax1.pie(data,labels=labels,explode=[0,0.3,0,0])  # explode突出重点[距离]

# ax2
x = np.random.randint(1,100,size=(100,))
y = np.random.randint(1,100,size=(100,))
ax2.scatter(x,y,c='r',marker='p',alpha=0.5)

# ax3
x = np.arange(1,13,1)
y = np.random.randint(30,120,size=(12,))
bars = ax3.bar(x,y,width=0.5)
ax3.set_title('XXX销售部门月度销售额')
# RGB:#AAFFCC
for bar in bars:
    bar.set_color('#' + str(np.random.randint(100000,999999,size=(1,))[0]))
    pass
ax3.set_xlabel('月份')
ax3.set_ylabel('销售额（万/元）')
ax3.set_xticks(x)
ax3.set_xticklabels([str(i) + '月' for i in range(1,13,1)])
# plt.text(1,3,'texttest')   # (横轴，纵轴，内容）
for xx,yy in zip(x,y):
    plt.text(xx,yy+0.5,'{0}万'.format(yy),ha='center',va='bottom')
    pass
plt.grid(linestyle='--')  # 网格线是虚线
ax3.plot(x,y,'b--')

plt.show()
