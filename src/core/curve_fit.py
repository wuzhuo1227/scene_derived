# coding=utf-8
# 曲线拟合功能函数文件
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

# from matplotlib.font_manager import FontManager
# fm = FontManager()
# mat_fonts = set(f.name for f in fm.ttflist)
# print(mat_fonts)
# exit(0)

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


def flatten(a):
    return [item for sublist in a for item in sublist]


# 多项式拟合
def polynomial_fit(x, y, degrees, colors, text_name, with_label=1, ranges_min=60, ranges_max=110, loc=4):
    font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15}
    # x = flatten(x)
    # y = flatten(y)

    x = np.array(x)
    # print('x is :\n', x)
    y = np.array(y)
    # print('y is :\n', y)
    # 用degree次多项式拟合
    # plot1 = plt.plot(x, y, 's', label='original values')
    # print('x1', x1)

    # 将拟合参数写入文件
    with open(text_name, 'w') as f:
        for idx, degree in enumerate(degrees):
            f1 = np.polyfit(x, y, degree)
            # print('f with degree ', degree, ' is :\n', degree, f1)
            f.write(str(degree) + ':' + ','.join(str(x) for x in f1) + '\n')
            p1 = np.poly1d(f1)
            # d1 = p1.integ(1)
            # d2 = p1.integ(2)
            # print('p1 is :\n', p1)
            # print('d1 is :\n', d1)
            # print('d1 is :\n', d2)
            # 也可使用yvals=np.polyval(f1, x)
            xt = np.arange(ranges_min, ranges_max, 0.001)
            yvals = p1(xt)  # 拟合y值
            # ytval = d1(xt)
            print('yvals is :\n', yvals)
            # 绘图
            # if with_label:
            #     plt.plot(xt, yvals, colors[idx], label='polyfit values with degree' + str(degree))
            # else:
            plt.plot(xt, yvals, colors[idx])
            # plt.plot(xt, d1(xt), 'r')
            # plt.plot(xt, d2(xt), 'g')
            # plt.plot(xt, ytval, 'r')
    # plt.legend(loc=loc)  # 指定legend的位置右下角


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


def draw(x0, y0, x1, y1, degrees, colors, path, xlabel, ylabel):
    font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15}
    # 设置画布大小
    # plt.figure(figsize=(10, 10))
    # 速度-加速度
    plt.xlim([min(x0) - 5, max(x0) + 5])
    plt.scatter(x0, y0, color='grey', label=u'实测值')
    plt.ylabel(ylabel, font)
    plt.xlabel(xlabel, font)
    # 调用多项式拟合，拟合的维度有 degrees 设定
    polynomial_fit(x1, [item.max_std for item in y1], degrees, ['b'], path + '_max.txt',
                   ranges_min=min(x0) - 1, ranges_max=max(x0) + 1)
    polynomial_fit(x1, [item.min_std for item in y1], degrees, ['g'], path + '_min.txt', 0,
                   ranges_min=min(x0) - 1, ranges_max=max(x0) + 1)
    polynomial_fit(x1, [item.mean for item in y1], degrees, ['r'], path, 0,
                   ranges_min=min(x0) - 1, ranges_max=max(x0) + 1)

    plt.scatter(x1, [item.max_std for item in y1], color='blue', marker='^', label=u'上界µ+3$\sigma$')
    plt.scatter(x1, [item.min_std for item in y1], color='green', marker='v', label=u'下界µ-3$\sigma$')
    plt.scatter(x1, [item.mean for item in y1], color='red', marker='x', label=u'平均值µ')
    plt.legend(loc='best', fontsize=15)
    # plt.show()
