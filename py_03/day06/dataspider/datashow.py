from dataspider.dao.jobdao import JobDao
import math
import matplotlib.pyplot as plt
import numpy as np

jobDao = JobDao()
# 职位数量对比
piedata = jobDao.statisticJobTypeCount()
print(piedata)

# 职位薪资对比，柱状图
barData = jobDao.statisticJobTypeMeanSalary()
print(barData)

# 城市薪资对比
barData2 = jobDao.statisticJobCitySalary()
print(barData2)


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,1,2)
# ax1
pl = [x['job_type'] for x in piedata]
data = [x['c'] for x in piedata]
# labels = [type + '' + '{0}%'.format(x/np.sum(data)*100) for type,x in zip(pl,data)]
# 保留小数点后两位
labels = [type + '' + '%.2f%%' % (x/np.sum(data)*100) for type,x in zip(pl,data)]
ax1.pie(data,labels=labels,explode=[0,0.3,0.7,0])  # explode突出重点[距离]
ax1.set_title('编程语言职位数量占比')


x = [i for i in range(0,len(barData))]
y = [math.floor(i['money']) for i in barData]
ax2Bars = ax2.bar(x,y)
ax2.set_xlabel('职位类别')
ax2.set_ylabel('薪资（元）')

ax2.set_xticks(x)
ax2.set_xticklabels([i['job_type'] for i in barData])
colors = ['#' + str(np.random.randint(100000,999999)) for i in range(len(barData2))]
for bar,color in zip(ax2Bars,colors):
    bar.set_color(color)
    pass
ax2.set_title('不同的职位薪资对比')

''''# ax2
x = np.random.randint(1,100,size=(100,))
y = np.random.randint(1,100,size=(100,))
ax2.scatter(x,y,c='r',marker='p',alpha=0.5)'''

# ax3

x = np.arange(1,len(barData2)+1,1)
y = [math.floor(i['money']) for i in barData2]
bars = ax3.bar(x,y,width=0.5)

# RGB:#AAFFCC
colors = ['#' + str(np.random.randint(100000,999999)) for i in range(len(barData2))]
for bar,color in zip(bars,colors):
    bar.set_color(color)
    pass
ax3.set_xlabel('城市')
ax3.set_ylabel('薪资（元）')
ax3.set_xticks(x)
ax3.set_xticklabels([i['job_city'] for i in barData2],rotation=90)
ax3.set_title('不同城市薪资对比')
# plt.text(1,3,'texttest')   # (横轴，纵轴，内容）
# for xx,yy in zip(x,y):
#    plt.text(xx,yy+0.5,'{0}万'.format(yy),ha='center',va='bottom')
#    pass
plt.grid(linestyle='--')  # 网格线是虚线
ax3.plot(x,y,'b--')
plt.show()