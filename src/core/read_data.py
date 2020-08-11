import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.core.curve_fit import polynomial_fit

class FileUtil:
    def __init__(self, config):
        self.config = config
        self.label = pd.read_csv(config.label_path)

    def get_data(self):
        speed = []
        a = []
        obj_speed = []
        obj_a = []
        thw = []
        for file_group in self.config.file_groups:
            # 读取数据
            df_object = pd.read_csv(file_group.obj_path, encoding=self.config.encoding)
            df_vehicle = pd.read_csv(file_group.vehicle_path, encoding=self.config.encoding)

            c_label = self.label[(self.label.Session == file_group.session_id)
                                 & (self.label.AdditionalDescription == self.config.additional_description)
                                 & (self.label.OPosition == self.config.o_position)]
            for i, row in c_label.iterrows():
                start_time = row['StartTime']
                end_time = row['EndTime']
                new_id = row['NewID']
                speed.extend(df_vehicle[(df_vehicle.Time == start_time + 1)]['Vehicle Speed[KPH]'].values)
                a.extend(df_vehicle[(df_vehicle.Time == start_time + 1)]['Acceleration-x[m/s2].1'].values)
                obj_speed.extend(df_object[(df_object.Time == start_time + 1) & (df_object.PublicID == new_id)]['VXAbs'].values)
                obj_a.extend(df_object[(df_object.Time == start_time + 1) & (df_object.PublicID == new_id)]['AXAbs'].values)
                thw.extend(df_object[(df_object.Time == start_time + 1) & (df_object.PublicID == new_id)]['THW'].values)
                if len(speed) != len(obj_speed):
                    speed.pop()

            # 预处理数据
        speed = np.array(speed)
        a = np.array(a)
        obj_speed = np.array(obj_speed)
        obj_a = np.array(obj_a)
        thw = np.array(thw)
        a = a.astype(np.float64)
        speed = speed.astype(np.float64)
        obj_speed = obj_speed.astype(np.float64)
        obj_a = obj_a.astype(np.float64)

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
        thw = thw.astype(np.float64)

        distance = thw * speed

        s_max = int(np.max(speed) + 1)
        s_min = int(np.min(speed) - 1)

        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1

        # 将本车速度分区
        speed1 = []
        obj_speed1 = []

        a_max = []
        a_min = []
        obj_speed_max = []
        obj_speed_min = []
        obj_a_max = []
        obj_a_min = []
        distance_max = []
        distance_min = []

        # 获取每个区域内的最大最小值，遍历区间比拆分区间大一
        # 本车速度相关性分析
        for i in range(6):
            ran_speed = np.where((speed > s_min + i * step) & (speed < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                speed1.append(s_min + i * step + step / 2)
                a_max.append(a[ran_speed].max())
                a_min.append(a[ran_speed].min())
                obj_speed_max.append(
                    obj_speed[ran_speed].max())
                obj_speed_min.append(
                    obj_speed[ran_speed].min())
                distance_max.append(distance[ran_speed].max())
                distance_min.append(distance[ran_speed].min())


        # 目标车速度相关性分析
        s_max = int(np.max(obj_speed) + 1)
        s_min = int(np.min(obj_speed) - 1)
        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1
        for i in range(6):
            ran_speed = np.where((obj_speed > s_min + i * step) & (obj_speed < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                obj_speed1.append(s_min + i * step + step / 2)
                obj_a_max.append(obj_a[ran_speed].max())
                obj_a_min.append(obj_a[ran_speed].min())

        speed1 = np.array(speed1).reshape(-1, 1)
        obj_speed1 = np.array(obj_speed1).reshape(-1, 1)
        a_max = np.array(a_max).reshape(-1, 1)
        a_min = np.array(a_min).reshape(-1, 1)
        obj_speed_max = np.array(obj_speed_max).reshape(-1, 1)
        obj_speed_min = np.array(obj_speed_min).reshape(-1, 1)
        obj_a_max = np.array(obj_a_max).reshape(-1, 1)
        obj_a_min = np.array(obj_a_min).reshape(-1, 1)
        distance_max = np.array(distance_max).reshape(-1, 1)
        distance_min = np.array(distance_min).reshape(-1, 1)

        # 设置颜色和多项式的阶数
        degrees = [1, 2, 3, 4]
        colors = ['b', 'y', 'g', 'r']
        font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15, }

        # 设置画布大小
        plt.figure(figsize=(20, 10))

        # 速度-加速度
        plt.subplot(121)
        plt.scatter(speed, a, color='black')
        plt.ylabel('a', font)
        plt.xlabel('speed', font)

        plt.subplot(122)
        plt.xlim([min(speed)-5, max(speed)+5])
        polynomial_fit(speed1, a_max, degrees, colors, "../parameters/speed_a_max.txt",
                       ranges_min=min(speed)-1, ranges_max=max(speed)+1)
        polynomial_fit(speed1, a_min, degrees, colors, "../parameters/speed_a_min.txt", 0,
                       ranges_min=min(speed)-1, ranges_max=max(speed)+1)

        plt.scatter(speed1, a_max, color='black', marker='x')
        plt.scatter(speed1, a_min, color='black')
        plt.scatter(speed, a, color='grey')
        plt.ylabel('a', font)
        plt.xlabel('speed', font)

        plt.show()

        plt.figure(figsize=(20, 10))
        # 速度-目标车速度
        plt.subplot(121)
        plt.scatter(speed, obj_speed, color='black')
        plt.ylabel('obj_speed', font)
        plt.xlabel('speed', font)

        plt.subplot(122)
        plt.xlim([min(speed)-5, max(speed)+5])

        polynomial_fit(speed1, obj_speed_max, degrees, colors, "../parameters/speed_objv_max.txt",
                       ranges_min=min(speed)-1, ranges_max=max(speed)+1)
        polynomial_fit(speed1, obj_speed_min, degrees, colors, "../parameters/speed_objv_min.txt", 0,
                       ranges_min=min(speed)-1, ranges_max=max(speed)+1)

        plt.scatter(speed1, obj_speed_max, color='black', marker='x')
        plt.scatter(speed1, obj_speed_min, color='black')
        plt.scatter(speed, obj_speed, color='gray')
        plt.ylabel('obj_speed', font)
        plt.xlabel('speed', font)

        plt.show()

        # 设置画布大小
        plt.figure(figsize=(20, 10))
        # 速度-相对距离
        plt.subplot(121)
        plt.scatter(speed, distance, color='black')
        plt.ylabel('distance', font)
        plt.xlabel('speed', font)

        plt.subplot(122)
        plt.xlim([min(speed)-5, max(speed)+5])
        polynomial_fit(speed1, distance_max, degrees, colors, "../parameters/speed_distance_max.txt.txt",
                       ranges_min=min(speed)-1, ranges_max=max(speed)+1)
        polynomial_fit(speed1, distance_min, degrees, colors, "../parameters/speed_distance_min.txt.txt", 0,
                       ranges_min=min(speed)-1, ranges_max=max(speed)+1)
        #
        #
        plt.scatter(speed1, distance_max, color='black', marker='x')
        plt.scatter(speed1, distance_min, color='black')

        plt.scatter(speed, distance, color='grey')

        # plt.scatter(speed, distance,  color='black')
        plt.ylabel('distance', font)
        plt.xlabel('speed', font)

        plt.show()
        plt.figure(figsize=(20, 10))

        # 目标车速度-目标车加速度
        plt.subplot(121)
        plt.scatter(obj_speed, obj_a, color='black')
        plt.ylabel('obj_a', font)
        plt.xlabel('obj_speed', font)

        plt.subplot(122)
        plt.xlim([min(obj_speed) - 5, max(obj_speed)+5])
        polynomial_fit(obj_speed1, obj_a_max, degrees, colors, "../parameters/objv_obja_max.txt",
                       ranges_min=min(obj_speed) - 1, ranges_max=max(obj_speed)+1)
        polynomial_fit(obj_speed1, obj_a_min, degrees, colors, "../parameters/objv_obja_min.txt", 0,
                       ranges_min=min(obj_speed) - 1, ranges_max=max(obj_speed)+1)

        plt.scatter(obj_speed1, obj_a_max, color='red', marker='x')
        plt.scatter(obj_speed1, obj_a_min, color='red')
        plt.scatter(obj_speed, obj_a, color='grey')

        # plt.scatter(speed, obj_a,  color='black')
        plt.ylabel('obj_a', font)
        plt.xlabel('obj_speed', font)

        plt.show()
