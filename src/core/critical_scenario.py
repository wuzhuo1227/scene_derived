import numpy as np

from src.core.curve_fit import draw
from src.core.math_parameter import MathParameter
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from src.config.parameters import Function
import os
import csv


def generate(scenario_list):
    dx = np.array([t.obj_car.displacement_x for t in scenario_list])
    dx = np.fabs(dx)
    voy = np.array([t.obj_car.velocity_y for t in scenario_list])
    voy = np.fabs(voy)
    ve = np.array([t.ego_car.velocity_x for t in scenario_list])
    vo = np.array([t.obj_car.velocity_x for t in scenario_list])

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
    figure = plt.figure(figsize=(30, 30))
    index = 0


    # for rv in range(10, 47, 4):
    #     index += 1
    #     plt.subplot(3, 3, index)
    # 绘制采样点
    draw_back(20, ve, dx, voy, figure)

    plt.figure(figsize=(30, 30))
    for rv in range(10, 41, 10):
        for ve in range(60, 19, -10):
            index += 1
            plt.subplot(4, 5, index)
            if ve - rv <= 0:
                continue
            draw_back2(ve, ve - rv, max(dx), max(voy))
            draw(dx, voy, dx_cluster, voy_par, degrees, colors, '../parameters/dx_voy', 'dx', 'voy')
    plt.show()

def draw_back(rv, ve, dx, voy, figure):
    # 单位统一为m/s
    # 相对速度
    rv = rv / 3.6
    ve = ve / 3.6
    voy = voy / 3.6
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

    # 取值范围定为最大值的1.2倍
    dx_list = np.arange(0.1, max(dx) * 1.2, 1)
    vy_list = np.arange(0.1, max(voy) * 1.2, 0.1)
    ve_list = np.arange(0.1, max(ve) * 1.2, 1)

    m = np.ones((len(dx_list), len(vy_list), len(ve_list)))
    bm = np.ones((len(dx_list), len(vy_list), len(ve_list)))

    total = 0
    illegal = 0
    real_num = 0
    critical_num = 0
    real_critical_num = 0
    real_safe_num = 0

    dx_vy_min = Function('../parameters/dis_eyv_min.txt')
    dx_vy_max = Function('../parameters/dis_eyv_max.txt')
    dx_ve_min = Function('../parameters/dis_ev_min.txt')
    dx_ve_max = Function('../parameters/dis_ev_max.txt')
    ve_vy_min = Function('../parameters/ev_eyv_min.txt')
    ve_vy_max = Function('../parameters/ev_eyv_max.txt')
    # 0 不合法点，1 参数空间内不合法点，2参数空间内危险点，3参数空间内安全点
    for i in range(len(dx_list)):
        for j in range(len(vy_list)):
            for k in range(len(ve_list)):
                if check(dx_vy_min, dx_vy_max, dx_list[i], vy_list[j] * 3.6) and check(dx_ve_min, dx_ve_max, dx_list[i],
                                                                                       ve_list[k] * 3.6) and check(
                    ve_vy_min,
                    ve_vy_max,
                    ve_list[k] * 3.6,
                    vy_list[j] * 3.6):
                    real_num += 1
                    if ve_list[k] <= rv:
                        illegal += 1
                        m[i][j][k] = 1  # 不合法点
                    elif is_critical(ve_list[k], ve_list[k] - rv, k, tp, td, dy, dx_list[i], vy_list[j]):
                        real_critical_num += 1
                        m[i][j][k] = 2
                    else:
                        real_safe_num += 1
                        m[i][j][k] = 3
                else:
                    m[i][j][k] = 0

    print(f"total:{total}, real:{real_num}, illegal:{illegal}, critical:{real_critical_num}, safe:{real_safe_num}")
    # print(m.shape)
    # 安全的参数空间点 3
    x = []
    y = []
    z = []
    # 危险的参数空间点 2
    ex = []
    ey = []
    ez = []
    # 参数空间内不合法点 1

    ill_x = []
    ill_y = []
    ill_z = []

    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            for k in range(m.shape[2]):
                if m[i][j][k] == 0:
                    pass
                else:
                    if m[i][j][k] == 1:
                        ill_x.append(dx_list[i])
                        ill_y.append(vy_list[j])
                        ill_z.append(ve_list[k])
                    elif m[i][j][k] == 2:
                        ex.append(dx_list[i])
                        ey.append(vy_list[j])
                        ez.append(ve_list[k])
                    elif m[i][j][k] == 3:
                        x.append(dx_list[i])
                        y.append(vy_list[j])
                        z.append(ve_list[k])
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    ex = np.array(ex)
    ey = np.array(ey)
    ez = np.array(ez)
    ill_x = np.array(ill_x)
    ill_y = np.array(ill_y)
    ill_z = np.array(ill_z)

    # 绘制背景
    axs = Axes3D(figure)
    axs.scatter3D(x, y, z, c='lightgreen', s=20, alpha=0.5)
    axs.scatter3D(ex, ey, ez, c='lightcoral', s=20, alpha=0.5)

    # axs.scatter3D(bx, by, bz, c='black', s=20, alpha=1.0)
    # axs.scatter3D(ill_x, ill_y, ill_z, c='black', s=15, alpha=0.4)
    axs.set_xlabel('距离', fontdict={'size': 30})
    axs.set_ylabel('切向速度', fontdict={'size': 30})
    axs.set_zlabel('本车速度', fontdict={'size': 30})

    dex = []
    voey = []
    vee = []

    dex1 = []
    voey1 = []
    vee1 = []
    for i in range(len(dx)):
        if is_critical(ve[i], ve[i] - rv, k, tp, td, dy, dx[i], voy[i]):
            dex.append(dx[i])
            voey.append(voy[i])
            vee.append(ve[i])
        else:
            dex1.append(dx[i])
            voey1.append(voy[i])
            vee1.append(ve[i])

    axs.scatter3D(dex, voey, vee, c='red', s=70)
    axs.scatter3D(dex1, voey1, vee1, c='green', s=70)

    plt.show()

    figure = plt.figure(figsize=(30, 30))
    # 使用mcmc采样
    # 在求随机数的时候需要转换回来，之后我觉得可以把单位统一一下。。
    vy_dx_min = Function('../parameters/eyv_dis_min.txt')
    vy_dx_max = Function('../parameters/eyv_dis_max.txt')
    ve_dx_min = Function('../parameters/ev_dis_min.txt')
    ve_dx_max = Function('../parameters/ev_dis_max.txt')
    vy_ve_min = Function('../parameters/eyv_ev_min.txt')
    vy_ve_max = Function('../parameters/eyv_ev_max.txt')

    # init first point x:dx, y:voy, z:ve
    # 距离
    x0 = np.random.rand() * (max(dx) - min(dx)) + min(dx)
    y_min = dx_vy_min.get_func(x0, 1)
    y_max = dx_vy_max.get_func(x0, 1)
    y0 = np.random.rand() * (y_max - y_min) + y_min
    z0 = get_random(x0, y0, dx_ve_min, dx_ve_max, vy_ve_min, vy_ve_max)

    sample_x, sample_y, sample_z = \
        mcmc_sample(x0, y0, z0, dx_vy_min, dx_vy_max,
                    vy_dx_min, vy_dx_max,
                    dx_ve_min, dx_ve_max,
                    ve_dx_min, ve_dx_max,
                    vy_ve_min, vy_ve_max,
                    ve_vy_min, ve_vy_max, 5000)

    sample_g = []
    sample_r = []
    sample_z = np.array(sample_z) / 3.6
    sample_y = np.array(sample_y) / 3.6
    for i in range(len(sample_x)):
        if is_critical(sample_z[i], sample_z[i] - rv, k, tp, td, dy, sample_x[i], sample_y[i]):
            sample_r.append([sample_x[i], sample_y[i], sample_z[i]])
        else:
            sample_g.append([sample_x[i], sample_y[i], sample_z[i]])

    # 绘制背景
    axs = Axes3D(figure)
    axs.scatter3D([d[0] for d in sample_g], [d[1] for d in sample_g], [d[2] for d in sample_g], c='green', s=20,
                  alpha=0.5)
    axs.scatter3D([d[0] for d in sample_r], [d[1] for d in sample_r], [d[2] for d in sample_r], c='red', s=20,
                  alpha=0.5)

    axs.set_xlabel('距离', fontdict={'size': 30})
    axs.set_ylabel('切向速度', fontdict={'size': 30})
    axs.set_zlabel('本车速度', fontdict={'size': 30})
    plt.show()

    # 写入文件
    with open('../scene/scenario-safe.csv', 'a+', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'ego_speed', 'obj_speed_x', 'distance_x', 'distance_y', 'obj_speed_y'])
        for index, item in enumerate(sample_g):
            writer.writerow([str(index), str(item[2]), str(item[2] + rv), str(item[0]), str(dy), str(item[1])])
    with open('../scene/scenario-dangerous.csv', 'a+', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'ego_speed', 'obj_speed_x', 'distance_x', 'distance_y', 'obj_speed_y'])
        for index, item in enumerate(sample_r):
            writer.writerow([str(index), str(item[2]), str(item[2] + rv), str(item[0]), str(dy), str(item[1])])


def draw_back2(ve, vo, max_x, max_y):
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
    plt.scatter(good_point_x, good_point_y, c='lightgreen', s=10, alpha=0.6)
    plt.scatter(error_x, error_y, c='lightcoral', s=10, alpha=0.6)

    # plt.show()


def is_critical(ve, vo, k, tp, td, dy, dx, vy):
    ve_ = ve + 0.5 * k * td * td
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


def is_border(m, i, j, k):
    v = m[i][j][k]
    il = m.shape[0]
    jl = m.shape[1]
    kl = m.shape[2]
    if (i + 1 < il and m[i + 1][j][k] != v) or (j + 1 < jl and m[i][j + 1][k] != v) or (
            k + 1 < kl and m[i][j][k + 1] != v) or (i - 1 >= 0 and m[i - 1][j][k] != v) or (
            j - 1 >= 0 and m[i][j - 1][k] != v) or (k - 1 >= 0 and m[i][j][k - 1] != v):
        return True
    return False


def check(func_min, func_max, x, y):
    a = func_min.get_func(x, 1)
    b = func_max.get_func(x, 1)
    return a <= y <= b


def mcmc_sample(x0, y0, z0, fxy_min, fxy_max,
                fyx_min, fyx_max,
                fxz_min, fxz_max,
                fzx_min, fzx_max,
                fyz_min, fyz_max,
                fzy_min, fzy_max,
                n=1000):
    # 马尔可夫链收敛阈值，具体多少收敛我也不知道，貌似需要验证？？？
    step = 30
    x = []
    y = []
    z = []
    for i in range(n):
        for j in range(step):
            x0 = get_random(y0, z0, fyx_min, fyx_max, fzx_min, fzx_max)
            y0 = get_random(x0, z0, fxy_min, fxy_max, fzy_min, fzy_max)
            z0 = get_random(x0, y0, fxz_min, fxz_max, fyz_min, fyz_max)
        x.append(x0)
        y.append(y0)
        z.append(z0)
    return x, y, z


def get_random(x, y, fxz_min, fxz_max, fyz_min, fyz_max):
    z_min_x = fxz_min.get_func(x, 1)
    z_max_x = fxz_max.get_func(x, 1)
    z_min_y = fyz_min.get_func(y, 1)
    z_max_y = fyz_max.get_func(y, 1)
    z_min = max(z_min_x, z_min_y, fxz_min.y_min)
    z_max = min(z_max_x, z_max_y, fxz_max.y_max)

    return np.random.rand() * (z_max - z_min) + z_min
