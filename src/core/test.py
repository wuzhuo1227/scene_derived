import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 我们将要画一个关于X,Y,Z的3D图

# 1.给3D图画一个坐标轴
fig = plt.figure()
ax = Axes3D(fig)
# 2.X,Y value
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
# 3.将X,Ymatch到底面上
X, Y = np.meshgrid(X, Y)
# 4.height.value。3D图形的高
Z = np.sqrt(X ** 2 + Y ** 2)  # numpy.sqrt()求平方根

# 5.开始画3D图啦
# rstride、csride分别为两个方向上的跨度，跨度越大越宽松，越小越密集；cmap设置为彩虹样式
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))  # 彩虹
# 等高线图contour---细线；contourf---连在一起的宽线条 ；zdir设置从哪个坐标轴压下去;  offset=n,表示等高线图的位置在n
ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap='rainbow')

# 设置z坐标轴的范围
ax.set_zlim(-2, 4)

plt.show()
