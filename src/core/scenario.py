import numpy as np

"""
变道场景
"""


class LaneChangeScenario:
    def __init__(self, ego_list, obj_list, start_time, end_time, obj_id):
        # 本车
        self.ego_car = EgoCar()
        # 目标车
        self.obj_car = ObjCar()

        ego = ego_list[ego_list.Time == start_time + 1]
        obj = obj_list[(obj_list.Time == start_time + 1) & (obj_list.PublicID == obj_id)]

        self.ego_car.velocity_x = np.float64(ego['Vehicle Speed[KPH]'].values[0])

        self.ego_car.acceleration_x = np.float64(ego['Acceleration-x[m/s2].1'].values[0])
        self.ego_car.acceleration_y = np.float64(ego['Acceleration-y[m/s2].1'].values[0])
        self.obj_car.velocity_x = np.float64(obj['VXAbs'].values[0])
        self.obj_car.velocity_y = np.float64(obj['VYAbs'].values[0])
        self.obj_car.acceleration_x = np.float64(obj['AXAbs'].values[0])
        self.obj_car.acceleration_y = np.float64(obj['AYAbs'].values[0])
        self.obj_car.displacement_x = np.float64(obj['PosX'].values[0])
        self.obj_car.displacement_y = np.float64(obj['PosY'].values[0])
        self.obj_car.relative_velocity_x = np.float64(obj['VXRel'].values[0])
        self.obj_car.relative_velocity_y = np.float64(obj['VYRel'].values[0])
        # 本车的y向速度由目标车的y向速度得到
        self.ego_car.velocity_y = -self.obj_car.velocity_y

        # 获取偏移量最大位置的时间
        ego = ego_list[(start_time <= ego_list.Time) & (ego_list.Time < end_time)]
        obj = obj_list[
            (start_time <= obj_list.Time) & (obj_list.Time < end_time) & (obj_list.PublicID == obj_id)]
        y_dis = np.array(obj['PosY'].values).astype(np.float64)
        y_a = np.array(ego['Acceleration-y[m/s2].1'].values).astype(np.float64)
        time = np.array(ego['Time'].values).astype(np.float64)
        _, self.max_acceleration_y = self.get_max_value(y_a)
        ii, self.max_displacement_y = self.get_max_value(y_dis)
        self.change_time = time[ii] - min(time)

    def check_nan(self):
        return self.ego_car.check_nan() & self.obj_car.check_nan() & (self.max_displacement_y != 'na') & (
                    self.max_acceleration_y != 'na') & (self.change_time != 'na')

    @staticmethod
    def get_max_value(lst):
        mi = min(lst)
        ma = max(lst)
        if abs(mi) > abs(ma):
            return np.argmin(lst), mi
        else:
            return np.argmax(lst), ma


class EgoCar:
    def __init__(self):
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0

    def check_nan(self):
        if self.velocity_x == 'na':
            return False
        if self.velocity_y == 'na':
            return False
        if self.acceleration_x == 'na':
            return False
        if self.acceleration_y == 'na':
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
        if self.velocity_x == 'na':
            return False
        if self.velocity_y == 'na':
            return False
        if self.acceleration_x == 'na':
            return False
        if self.acceleration_y == 'na':
            return False
        if self.displacement_x == 'na':
            return False
        if self.displacement_y == 'na':
            return False
        if self.relative_velocity_x == 'na':
            return False
        if self.relative_velocity_y == 'na':
            return False
        return True
