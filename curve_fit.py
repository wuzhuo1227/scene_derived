# coding=utf-8
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import operator
from functools import reduce

def flatten(a):
    return [item for sublist in a for item in sublist]

# 多项式拟合
def polynomial_fit(x, y, degrees, colors, with_label=1):
    x = flatten(x)
    y = flatten(y)

    x = np.array(x)
    print('x is :\n', x)
    y = np.array(y)
    print('y is :\n', y)
    # 用degree次多项式拟合
    # plot1 = plt.plot(x, y, 's', label='original values')
    # print('x1', x1)
    for idx, degree in enumerate(degrees):
        f1 = np.polyfit(x, y, degree)
        print('f with degree ', degree, ' is :\n', degree, f1)

        p1 = np.poly1d(f1)
        print('p1 is :\n', p1)

        # 也可使用yvals=np.polyval(f1, x)
        xt = np.arange(64, 106, 0.001)
        yvals = p1(xt)  # 拟合y值
        print('yvals is :\n', yvals)
        # 绘图
        if with_label:
            plt.plot(xt, yvals, colors[idx], label='polyfit values with degree' + str(degree))
        else:
            plt.plot(xt, yvals, colors[idx])

    # plt.xlabel('x')
    # plt.ylabel('y')
    plt.legend(loc=4)  # 指定legend的位置右下角
    # plt.show()


def exfunc(x, a, b, c):
    res = a * np.exp(-b * x) + c
    # print(x, a, b, c, res)
    return res


def exponential_fit(x, y):
    x = np.array(x)
    y = np.array(y)

    plt.scatter(x[:], y[:], 25, "red")
    A, B, C = curve_fit(exfunc, x, y)[0]
    print(A, B, C)
    x1 = np.arange(0, 40, 0.01)
    # print(x1)
    y1 = [exfunc(i, A, B, C) for i in x1]
    # print(y1)
    plt.plot(x1, y1, "green")
    plt.show()


# x = [0, 5, 10, 15, 25, 30, 35, 40]
# y = [137.06164605656792, 153.61101550877845, 198.06929110588567, 351.71281986502646, 164.91239598679968,
#      249.18723108318608, 229.29386057427064, 195.95795665082829]
# polynomial_fit(x, y, [1, 2, 3, 4], ['b', 'y', 'g', 'r'])

# exponential_fit(x, y)
# exponential_fit(x, y)
