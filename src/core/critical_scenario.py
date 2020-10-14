import numpy as np

from src.core.curve_fit import draw
from src.core.math_parameter import MathParameter
import matplotlib.pyplot as plt
import math


def generate(scenario_list):
    dx = np.array([t.obj_car.displacement_x for t in scenario_list])
    dx = np.fabs(dx)
    voy = np.array([t.obj_car.velocity_y for t in scenario_list])
    voy = np.fabs(voy)

    # 计算速度的最大最小区间
    s_max = int(np.max(dx) + 1)
    s_min = int(np.min(dx) - 1)

    # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
    step = int((s_max - s_min) / 5) + 1

    dx_cluster = []
    voy_par = []

    for i in range(6):
        ran_speed = np.where((dx > s_min + i * step) & (dx < s_min + (i + 1) * step))
        if len(ran_speed[0]) > 0:
            dx_cluster.append(s_min + i * step + step / 2)
            voy_par.append(MathParameter(voy[ran_speed]))

    degrees = [1]
    colors = ['b']
    font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15, }
    plt.figure(figsize=(30, 20))
    index = 0
    for rv in range(10, 41, 10):
        for ve in range(60, 19, -10):
            index += 1
            plt.subplot(4, 5, index)
            if ve-rv <= 0:
                continue
            draw_back(ve, ve-rv, max(dx), max(voy))
            draw(dx, voy, dx_cluster, voy_par, degrees, colors, '../parameters/dx_voy', 'dx', 'voy')
    plt.show()


def draw_back(ve, vo, max_x, max_y):
    # 单位统一为m/s
    # 本车速度
    ve = ve / 3.6
    # 目标车速度
    vo = vo / 3.6
    # 重力加速度
    g = 9.8
    # 反应时间
    tp = 1.15
    # 刹车到最大值的时间
    td = 0.6
    # 车辆匀变加速运动，加速度变化量
    k = -0.774 * g / td
    # 切向距离
    dy = 1.6
    dx_list = np.arange(0.1, max_x, 0.1)
    vy_list = np.arange(0.1, max_y, 0.1)
    good_point_x = []
    good_point_y = []
    error_x = []
    error_y = []
    for dx in dx_list:
        for vy in vy_list:
            if is_critical(ve, vo, k, tp, td, dy, dx, vy):
                error_x.append(dx)
                error_y.append(vy)
            else:
                good_point_x.append(dx)
                good_point_y.append(vy)
    plt.scatter(good_point_x, good_point_y, c='lightgreen', s=10,  alpha=0.6)
    plt.scatter(error_x, error_y, c='lightcoral', s=10,  alpha=0.6)
    # plt.show()


def is_critical(ve, vo, k, tp, td, dy, dx, vy):
    ve_ = ve + 0.5 * k * 0.6 * 0.6
    if vo > ve_:
        tc = tp + np.sqrt(2.0 * (vo - ve) / k)
        dc = tp * ve + ve * (tc - tp) + k / 6.0 * np.power(tc - tp, 3) - vo * tc
    else:
        tc = tp + td + (vo - ve_) / k
        dc = ve * tp + ve * td + k / 6.0 * np.power(td, 3) + ve_ * (tc - td) - 0.774 * 9.8 / 2.0 * np.power(tc - td,
                                                                                                            2) - vo * tc
    if dc < dx:
        return False
    ty = dy / vy
    if ty < tp:
        dr = (ve - vo) * ty
    elif tp < ty < td + tp:
        dr = tp * ve + ve * (ty - tp) + k / 6.0 * np.power(ty - tp, 3) - vo * ty
    elif td + tp < ty < tc:
        dr = ve * tp + ve * td + k / 6.0 * np.power(td, 3) + ve_ * (ty - td) - 0.85 * 9.8 / 2.0 * np.power(ty - td,
                                                                                                           2) - vo * ty
    else:
        return False
    if dr > dx:
        return False
    return True
