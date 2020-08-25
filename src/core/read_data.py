import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.core.curve_fit import polynomial_fit
from src.core.curve_fit import draw
from src.core.math_parameter import MathParameter


class FileUtil:
    def __init__(self, config):
        self.config = config
        self.label = pd.read_csv(config.label_path)

    '''
    根据输入的路径读取信息，拟合数据并生成相关拟合参数
    '''

    def get_data(self):
        # 本车速度
        speed = []
        # 本车加速度
        a = []
        # 目标车速度
        obj_speed = []
        # 目标车加速度
        obj_a = []
        # 车头时距
        thw = []
        # 相对速度
        relative_speed = []
        for file_group in self.config.file_groups:
            # 读取数据
            df_object = pd.read_csv(file_group.obj_path, encoding=self.config.encoding)
            df_vehicle = pd.read_csv(file_group.vehicle_path, encoding=self.config.encoding)

            # 读取标注数据，要保证session_id的一致性
            c_label = self.label[(self.label.Session == file_group.session_id)
                                 & (self.label.AdditionalDescription == self.config.additional_description)
                                 & (self.label.OPosition == self.config.o_position)]
            for i, row in c_label.iterrows():
                # 获取起始时间
                start_time = row['StartTime']
                end_time = row['EndTime']
                new_id = row['NewID']
                speed.extend(df_vehicle[(df_vehicle.Time == start_time + 1)]['Vehicle Speed[KPH]'].values)
                a.extend(df_vehicle[(df_vehicle.Time == start_time + 1)]['Acceleration-x[m/s2].1'].values)
                obj_speed.extend(
                    df_object[(df_object.Time == start_time + 1) & (df_object.PublicID == new_id)]['VXAbs'].values)
                obj_a.extend(
                    df_object[(df_object.Time == start_time + 1) & (df_object.PublicID == new_id)]['AXAbs'].values)
                thw.extend(df_object[(df_object.Time == start_time + 1) & (df_object.PublicID == new_id)]['THW'].values)
                if len(speed) != len(obj_speed):
                    speed.pop()
        # 获取相对速度
        relative_speed = [speed[i] - obj_speed[i] for i in range(len(speed))]
        # 预处理数据
        speed = np.array(speed).astype(np.float64)
        a = np.array(a).astype(np.float64)
        obj_speed = np.array(obj_speed).astype(np.float64)
        obj_a = np.array(obj_a).astype(np.float64)
        thw = np.array(thw).astype(np.float64)
        relative_speed = np.array(relative_speed).astype(np.float64)

        print(f'数据读取完毕，共记{speed.shape[0]}条数据')

        # 删除包含 na 的数据行
        del_pos = []
        for n in range(speed.shape[0]):
            if thw[n] == 'na':
                del_pos.append(n)

        speed = np.delete(speed, del_pos, axis=0)
        a = np.delete(a, del_pos, axis=0)
        obj_speed = np.delete(obj_speed, del_pos, axis=0)
        obj_a = np.delete(obj_a, del_pos, axis=0)
        thw = np.delete(thw, del_pos, axis=0)
        distance = thw * speed
        # 计算速度的最大最小区间
        s_max = int(np.max(speed) + 1)
        s_min = int(np.min(speed) - 1)

        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1

        # 将本车速度分区
        speed1 = []
        obj_speed1 = []
        relative_speed1 = []

        a_par = []
        obj_speed_par = []
        obj_a_par = []
        distance_par = []
        distance_relative_par = []

        # 获取每个区域内的最大最小值，遍历区间比拆分区间大一
        # 本车速度相关性分析
        # 本车速度->本车加速度、目标车速度、距离
        for i in range(6):
            ran_speed = np.where((speed > s_min + i * step) & (speed < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                speed1.append(s_min + i * step + step / 2)
                a_par.append(MathParameter(a[ran_speed]))
                obj_speed_par.append(MathParameter(obj_speed[ran_speed]))
                distance_par.append(MathParameter(distance[ran_speed]))
        # 目标车速度相关性分析
        # 目标车速度->目标车加速度
        s_max = int(np.max(obj_speed) + 1)
        s_min = int(np.min(obj_speed) - 1)
        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1
        for i in range(6):
            ran_speed = np.where((obj_speed > s_min + i * step) & (obj_speed < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 1:
                obj_speed1.append(s_min + i * step + step / 2)
                obj_a_par.append(MathParameter(obj_a[ran_speed]))
        # 相对速度相关性分析
        # 相对速度->距离
        s_max = int(np.max(relative_speed) + 1)
        s_min = int(np.min(relative_speed) - 1)
        step = int((s_max - s_min) / 5) + 1
        for i in range(6):
            ran_speed = np.where((relative_speed > s_min + i * step) & (relative_speed < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                relative_speed1.append(s_min + i * step + step / 2)
                distance_relative_par.append(MathParameter(distance[ran_speed]))

        # speed1 = np.array(speed1).reshape(-1, 1)
        # obj_speed1 = np.array(obj_speed1).reshape(-1, 1)
        # relative_speed1 = np.array(relative_speed1).reshape(-1, 1)

        # 以下是数据拟合部分以及画图部分
        # 设置颜色和多项式的阶数
        degrees = [1]
        colors = ['b']
        font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15, }
        # 本车速度，本车加速度
        draw(speed, a, speed1, a_par, degrees, colors, '../parameters/speed_a', 'ego-v', 'ego-a')
        # 本车速度，目标车速度
        draw(speed, obj_speed, speed1, obj_speed_par, degrees, colors, '../parameters/speed_objv', 'ego-v', 'obj-v')

        # 本车速度，距离
        draw(speed, distance, speed1, distance_par, degrees, colors, '../parameters/speed_distance', 'ego-v',
             'distance')
        # 目标车速度，目标车加速度
        draw(obj_speed, obj_a, obj_speed1, obj_a_par, degrees, colors, '../parameters/objv_obja', 'obj-v', 'obj-a')
        # 相对速度, 距离
        draw(relative_speed, distance, relative_speed1, distance_relative_par, degrees, colors,
             '../parameters/relativespeed_distance', 'relative-v', 'distance')

    def generate_point(self):
        # 变道超车，并返回原车道的情景
        lst1 = []
        # 变道超车，在对应时间内为返回原车道的场景
        lst2 = []
        for file_group in self.config.file_groups:
            # 读取数据
            df_vehicle = pd.read_csv(file_group.vehicle_path, encoding=self.config.encoding)

            # 读取标注数据，要保证session_id的一致性
            c_label = self.label[(self.label.Session == file_group.session_id)
                                 & (self.label.AdditionalDescription == self.config.additional_description)
                                 & (self.label.OPosition == self.config.o_position)]
            lst = []
            # 获取所有的场景开始和结束的时间，并去重
            for i, row in c_label.iterrows():
                lst.append((row['PStartTime'], row['PEndTime']))
            lst = list(set(lst))
            for time_range in lst:
                # 获取时间和加速度
                t = df_vehicle[(df_vehicle.Time >= time_range[0])
                                & (df_vehicle.Time < time_range[1])]['Time'].values
                a = df_vehicle[(df_vehicle.Time >= time_range[0])
                                & (df_vehicle.Time < time_range[1])]['Acceleration-y[m/s2]'].values
                t = np.array(t).astype(np.float64)
                a = np.array(a).astype(np.float64)
                max_a = max(abs(a))
                # 将时间转化成从0开始的序列
                t -= min(t)
                max_t = max(t)
                # 使用4阶多项式函数拟合曲线（选取4阶的原因是尝试多组数据后，4阶的拟合效果最好）
                f0 = np.polyfit(t, a, 4)
                f = np.poly1d(f0)
                # 加速度的二阶导数为距离，常数为0
                d = f.integ(2)
                # 求出y的绝对值的最大值对应的x点
                yvals = d(np.arange(0, max(t), 0.001))
                max_y_t = max(yvals)
                min_y_t = min(yvals)
                # 计算y值的最大值
                max_y = -1
                if abs(max_y_t) > abs(min_y_t):
                    max_y = max_y_t
                else:
                    max_y = min_y_t
                # 计算对应的x值，通过roots求解
                max_x = -1
                for item in (d - max_y).roots:
                    if item.imag == 0 and 0 <= item.real <= max_t:
                        max_x = item.real
                if max_x == -1:
                    continue
                # 判断 x 是否处于整个场景时间节点的中间40%，即最终变回了原车道的场景
                if max_x >= max_t * 0.3 and max_x >= max_t * 0.7:
                    lst1.append((max_x, max_a, max_t))
                else:
                    lst2.append((max_a, max_t))
        print(len(lst1))
        print(len(lst2))
            # speed.extend(df_vehicle[(df_vehicle.Time == start_time + 1)]['Vehicle Speed[KPH]'].values)
            # print(lst)
