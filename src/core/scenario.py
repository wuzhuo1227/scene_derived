import math

import numpy as np

"""
变道场景
"""


class LaneChangeScenario:
    def __init__(self, ego_list, obj_list, start_time, end_time, obj_id, session_id):
        # 本车
        self.ego_car = EgoCar()
        # 目标车
        self.obj_car = ObjCar()
        self.max_acceleration_y = 'na'
        self.max_displacement_y = 'na'
        self.change_time = 'na'
        ego = ego_list[(ego_list.c_time == start_time + 1) & (ego_list.c_session == session_id)]
        obj = obj_list[
            (obj_list.c_time == start_time + 1) & (obj_list.n_publicid == obj_id) & (obj_list.c_session == session_id)]

        # ego1 = ego_list[ego_list.c_session == session_id]
        # obj1 = obj_list[obj_list.c_session == session_id]

        # if ego1.size > 0 or obj1.size > 0:
        #     print("hhhh")

        # if ego.size > 0:
        #     print(f'st:{start_time}, et:{end_time}, oi:{obj_id}, si:{session_id}\n')
        #     print(ego)

        if (ego.size > 0) & (obj.size > 0):
            # print(ego)
            # print(obj)
            pass
        else:
            print(f'st:{start_time}, et:{end_time}, oi:{obj_id}, si:{session_id} has no data, {start_time + 1}\n')
            return

        # print(ego['n_vehiclespeed'])
        self.ego_car.velocity_x = np.float64(ego['n_vehiclespeed'].values[0])

        self.ego_car.acceleration_x = np.float64(ego['n_accelerationx'].values[0])
        self.ego_car.acceleration_y = np.float64(ego['n_accelerationy'].values[0])

        self.obj_car.velocity_x = np.float64(obj['n_vxabs'].values[0])
        self.obj_car.velocity_y = np.float64(obj['n_vyabs'].values[0])
        self.obj_car.acceleration_x = np.float64(obj['n_axabs'].values[0])
        self.obj_car.acceleration_y = np.float64(obj['n_ayabs'].values[0])
        self.obj_car.displacement_x = np.float64(obj['n_posx'].values[0])
        if self.obj_car.displacement_x > 200:
            self.obj_car.displacement_x = 'na'
        self.obj_car.displacement_y = np.float64(obj['n_posy'].values[0])
        self.obj_car.relative_velocity_x = np.float64(obj['n_vxrel'].values[0])
        self.obj_car.relative_velocity_y = np.float64(obj['n_vyrel'].values[0])
        # 本车的y向速度由目标车的y向速度得到
        self.ego_car.velocity_y = -self.obj_car.velocity_y

        # 获取偏移量最大位置的时间
        ego = ego_list[(start_time <= ego_list.c_time) & (ego_list.c_time < end_time)]
        obj = obj_list[
            (start_time <= obj_list.c_time) & (obj_list.c_time < end_time) & (obj_list.n_publicid == obj_id)]
        y_dis = np.array(obj['n_posy'].values).astype(np.float64)
        y_a = np.array(ego['n_accelerationy'].values).astype(np.float64)
        time = np.array(ego['c_time'].values).astype(np.float64)
        if len(y_a) > 0 and len(y_dis) > 0:
            _, self.max_acceleration_y = self.get_max_value(y_a)
            ii, self.max_displacement_y = self.get_max_value(y_dis)
            self.change_time = time[ii] - min(time)

    def check_nan(self):
        return self.ego_car.check_nan() & self.obj_car.check_nan() & (self.max_displacement_y != 'na') & (
                self.max_acceleration_y != 'na') & (self.change_time != 'na')

    @staticmethod
    def get_max_value(lst):
        if len(lst) == 0:
            return -1, 'na'
        else:
            mi = min(lst)
            ma = max(lst)
            if abs(mi) > abs(ma):
                return np.argmin(lst), mi
            else:
                return np.argmax(lst), ma

    def is_critical(self):
        if self.obj_car.velocity_x >= self.ego_car.velocity_x:
            return True
        tp = 1.15
        t0 = 0.6
        td = tp + t0
        x = -1
        a = -0.85 * 0.8
        # 匀变减速运动，加速度的变化，da/dt
        k = a / t0 * 3.6
        dy0 = 1.6
        # 本车减速到与目标车一样速度的时间
        tx = -1
        # 在tx下，目标车的纵向位移
        dy1 = -1
        # 对应到匀变减速的过程
        if self.obj_car.velocity_x >= self.ego_car.velocity_x + 0.5 * k * t0 * t0:
            tx = np.sqrt(2 * (self.obj_car.velocity_x - self.ego_car.velocity_x) / k)
            x = tp * self.ego_car.velocity_x + tx * self.ego_car.velocity_x + 1.0 / 6 * k * tx * tx * tx - (
                    tp + tx) * self.obj_car.velocity_x
            dy1 = (tp + tx) * self.obj_car.velocity_y
        else:
            vex = self.ego_car.velocity_x + 0.5 * k * t0
            tx = (self.obj_car.velocity_x - vex) / a
            x = tp * self.ego_car.velocity_x + self.ego_car.velocity_x * t0 + 1.0 / 6 * k * t0 * t0 * t0 + vex * tx + 0.5 * a * tx * tx - (
                    td + tx) * self.obj_car.velocity_x
            dy1 = (td + tx) * self.obj_car.velocity_y
        # 本车刹车到停止的时间
        tf = (self.ego_car.velocity_x + 0.5 * k * t0 * t0) / (-a) + td
        # 目标车横向位移为
        return self.obj_car.displacement_x > x or dy1 < dy0


class EgoCar:
    def __init__(self):
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0

    def check_nan(self):
        if self.velocity_x == 'na' or np.isnan(self.velocity_x):
            return False
        if self.velocity_y == 'na' or np.isnan(self.velocity_y):
            return False
        if self.acceleration_x == 'na' or np.isnan(self.acceleration_x):
            return False
        if self.acceleration_y == 'na' or np.isnan(self.acceleration_y):
            return False
        return True


class ObjCar:
    def __init__(self):
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0
        self.displacement_x = 0.0
        self.displacement_y = 0.0
        self.relative_velocity_x = 0.0
        self.relative_velocity_y = 0.0

    def check_nan(self):
        if self.velocity_x == 'na' or np.isnan(self.velocity_x):
            return False
        if self.velocity_y == 'na' or np.isnan(self.velocity_y):
            return False
        if self.acceleration_x == 'na' or np.isnan(self.acceleration_x):
            return False
        if self.acceleration_y == 'na' or np.isnan(self.acceleration_y):
            return False
        if self.displacement_x == 'na' or np.isnan(self.displacement_x):
            return False
        if self.displacement_y == 'na' or np.isnan(self.displacement_y):
            return False
        if self.relative_velocity_x == 'na' or np.isnan(self.relative_velocity_x):
            return False
        if self.relative_velocity_y == 'na' or np.isnan(self.relative_velocity_y):
            return False
        return True
