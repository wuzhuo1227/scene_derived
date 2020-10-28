import numpy as np

from src.core.curve_fit import draw
from src.core.math_parameter import MathParameter
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from src.config.parameters import Function


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
    draw_back(20, ve, dx, voy, figure)

    # for rv in range(10, 41, 10):
    #     for ve in range(60, 19, -10):
    #         index += 1
    #         plt.subplot(4, 5, index)
    #         if ve - rv <= 0:
    #             continue
    #         draw_back(ve, ve - rv, max(dx), max(voy))
    #         draw(dx, voy, dx_cluster, voy_par, degrees, colors, '../parameters/dx_voy', 'dx', 'voy')
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
    dx_list = np.arange(0.1, max(dx), 1)
    vy_list = np.arange(0.1, max(voy), 0.1)
    ve_list = np.arange(0.1, max(ve), 1)

    m = np.ones((len(dx_list), len(vy_list), len(ve_list)))
    bm = np.ones((len(dx_list), len(vy_list), len(ve_list)))

    total = 0
    illegal = 0
    real_num = 0
    critical_num = 0
    real_critical_num = 0
    real_safe_num = 0

    dx_vy_min = Function('/Users/liebes/project/laboratory/scene_derived/parameters/dis_eyv_min.txt')
    dx_vy_max = Function('/Users/liebes/project/laboratory/scene_derived/parameters/dis_eyv_max.txt')
    dx_ve_min = Function('/Users/liebes/project/laboratory/scene_derived/parameters/dis_ev_min.txt')
    dx_ve_max = Function('/Users/liebes/project/laboratory/scene_derived/parameters/dis_ev_max.txt')
    ve_vy_min = Function('/Users/liebes/project/laboratory/scene_derived/parameters/ev_eyv_min.txt')
    ve_vy_max = Function('/Users/liebes/project/laboratory/scene_derived/parameters/ev_eyv_max.txt')
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
    axs.scatter3D(x, y, z, c='lightgreen', s=15, alpha=0.5)
    axs.scatter3D(ex, ey, ez, c='lightcoral', s=15, alpha=1)

    # axs.scatter3D(bx, by, bz, c='black', s=20, alpha=1.0)
    # axs.scatter3D(ill_x, ill_y, ill_z, c='black', s=15, alpha=0.4)
    axs.set_xlabel('本车速度')
    axs.set_ylabel('切向速度')
    axs.set_zlabel('距离')

    axs.scatter3D(dx, voy, ve, c='grey')


    # plt.show()


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
