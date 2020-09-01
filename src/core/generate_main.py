# coding=utf-8
from src.core import act, obj, vehicle
import numpy as np
import pickle
from src.config.parameters import Function


# 循线行驶遇慢车
def meet_slow_car(s_id, num_scene):
    v1 = vehicle.Vehicle()  # 本车
    o1 = obj.Object()  # 目标车

    v1.scene_id = "循线行驶遇慢车_" + str(s_id)
    o1.scene_id = "循线行驶遇慢车_" + str(s_id)

    speed1 = np.random.randint(low=100, high=120)
    speed2 = np.random.randint(low=60, high=speed1)

    v1.speed = speed1
    o1.speed = speed2

    v1.write_to_csv()
    o1.write_to_csv()


'''
变道超车
degree 表示拟合曲线阶数
'''


def change_lane(s_id, degree):
    v1 = vehicle.Vehicle()  # 本车
    o1 = obj.Object()  # 同车道前车
    a1 = act.Act()

    v1.scene_id = o1.scene_id = a1.scene_id = "change_lane" + str(s_id)
    v1.car_id = 'ego' + str(s_id)
    o1.parti_id = 'obj' + str(s_id)
    a1.car_id = v1.car_id

    # o_front = obj.Object
    # o_behind = obj.Object

    # 随机本车速度，拟合目标车速度、纵向距离距离、本车加速度、目标车加速度、变道动作时间

    # 随机本车速度，90 - 110 之间
    v1.speed = 90 + 20 * np.random.rand()

    # 随机目标车速度
    f_min = Function('../../parameters/ev_ov_min.txt')
    f_max = Function('../../parameters/ev_ov_max.txt')

    o1.speed = f_min.get_func(v1.speed, degree) + np.random.rand() * (
            f_max.get_func(v1.speed, degree) - f_min.get_func(v1.speed, degree))

    # 随机距离
    # 速度-距离
    f_min = Function('../../parameters/ev_dis_min.txt')
    f_max = Function('../../parameters/ev_dis_max.txt')
    # 相对速度-距离，取两者的交集
    f_real_min = Function('../../parameters/rv_dis_min.txt')
    f_real_max = Function('../../parameters/rv_dis_max.txt')
    real_speed = abs(o1.speed - v1.speed)

    distance = np.random.randint(
        low=max(f_min.get_func(v1.speed, degree), f_real_min.get_func(real_speed, degree)),
        high=min(f_max.get_func(v1.speed, degree), f_real_max.get_func(real_speed, degree)))

    # 随机本车加速度
    f_min = Function('../../parameters/ev_ea_min.txt')
    f_max = Function('../../parameters/ev_ea_max.txt')

    v1.acceleration = f_min.get_func(v1.speed, degree) + np.random.rand() * (
            f_max.get_func(v1.speed, degree) - f_min.get_func(v1.speed, degree))

    # 随机目标车加速度
    f_min = Function('../../parameters/ov_oa_min.txt')
    f_max = Function('../../parameters/ov_oa_max.txt')
    o1.acceleration = f_min.get_func(o1.speed, degree) + np.random.rand() * (
                f_max.get_func(o1.speed, degree) - f_min.get_func(o1.speed, degree))

    o1.y_position = distance

    # 随机时间
    f_min = Function('../../parameters/ev_time_min.txt')
    f_max = Function('../../parameters/ev_time_max.txt')
    a1.duration_time = f_min.get_func(o1.speed, degree) + np.random.rand() * (
                f_max.get_func(o1.speed, degree) - f_min.get_func(o1.speed, degree))
    a1.begin_time = 0


    # o1.x_position = np.random

    # 写入文件
    v1.write_to_csv()
    o1.write_to_csv()
    a1.write_to_csv()

    # a1 = act.Act()
    # a1.scene_id = "变道超车_" + str(s_id)
    # a1.target_speed = speed1


# 循线跟车
def follow_road(s_id, num_scene):
    v1 = vehicle.Vehicle()
    o1 = obj.Object()

    v1.scene_id = "循线跟车_" + str(s_id)
    o1.scene_id = "循线跟车_" + str(s_id)

    distance = np.random.randint(low=180, high=300)

    o1.y_position = distance

    v1.speed = distance / 3  # 安全速度的临界点
    o1.speed = np.random.randint(low=60, high=120)

    v1.write_to_csv()
    o1.write_to_csv()


if __name__ == "__main__":
    # 需要生成的场景数量
    num_scene = 10
    for i in range(num_scene):
        # meet_slow_car(i)
        # follow_road(i)
        # 生成变道场景，注意选择生成的场景前重新生成相关的参数。
        change_lane(i, 1)
