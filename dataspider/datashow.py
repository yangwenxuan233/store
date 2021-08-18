from dataspider.dao.bilibilidao import JobDao
import math
import matplotlib.pyplot as plt
import numpy as np

bilibiliDao = JobDao()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure()
ax3 = fig.add_subplot()

type = bilibiliDao.statistictype()

x = np.arange(1, 6, 1)
data = [x['t_bilibili_type'] for x in type]
print(data)
y = bilibiliDao.statisticplayvolume(data[0])
k = [x['t_bilibili_playvolume'] for x in y]
k = [x[:-1] for x in k]
k = [float(i)for i in k]
print(k)
plt.plot(x, k, '*-',  color='skyblue', label=data[0])

y = bilibiliDao.statisticplayvolume(data[1])
k = [x['t_bilibili_playvolume'] for x in y]
k = [x[:-1] for x in k]
k = [float(i) for i in k]
print(k)
plt.plot(x, k, '*-',  color='r', label=data[1])

y = bilibiliDao.statisticplayvolume(data[2])
k = [x['t_bilibili_playvolume'] for x in y]
k = [x[:-1] for x in k]
k = [float(i) for i in k]
print(k)
plt.plot(x, k, '*-', color='b', label=data[2])

y = bilibiliDao.statisticplayvolume(data[3])
k = [x['t_bilibili_playvolume'] for x in y]
k = [x[:-1] for x in k]
k = [float(i) for i in k]
print(k)
plt.plot(x, k, '*-', color='y', label=data[3])

y = bilibiliDao.statisticplayvolume(data[4])
k = [x['t_bilibili_playvolume'] for x in y]
k = [x[:-1] for x in k]
k = [float(i) for i in k]
print(k)
plt.plot(x, k, '*-',  color='orange', label=data[4])


plt.xticks(x)


ax3.set_xlabel('综合排名top5')
ax3.set_ylabel('点击量(万次)')
plt.legend()
plt.show()
