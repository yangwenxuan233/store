from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0,10,0.1)
xs,ys = np.meshgrid(x,x)
print(xs,ys)

# 计算z值:z=2*x^2+y^2+1
z = 2*xs**2 + ys**2 + 1
fig = plt.figure()
ax = Axes3D(fig)

# 表面
ax.plot_surface(xs,ys,z,rstride=1,cstride=1)
plt.show()

