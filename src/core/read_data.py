import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.core.curve_fit import polynomial_fit
from src.core.curve_fit import draw
from src.core.math_parameter import MathParameter
from src.core.scenario import LaneChangeScenario
from src.core.critical_scenario import generate as generate_critical
import pickle

class FileUtil:
    def __init__(self, config):
        self.config = config
        self.label = pd.read_csv(config.label_path)

    '''
    根据输入的路径读取信息，拟合数据并生成相关拟合参数
    '''

    def get_data(self, use_cache=True):
        # 场景列表
        scenario_list = []
        # 读取缓存
        if use_cache:
            with open('scenario', 'rb') as f:
                scenario_list = pickle.load(f)
            print('load data from cache')
        else:
            for file_group in self.config.file_groups:
                # 读取数据
                df_object = pd.read_csv(file_group.obj_path, encoding=self.config.encoding)
                df_vehicle = pd.read_csv(file_group.vehicle_path, encoding=self.config.encoding)

                # 读取标注数据，要保证session_id的一致性
                c_label = self.label[(
                                             ((self.label.c_oposition == '左前') & (self.label.c_obehavior == '向右变道'))
                                             | ((self.label.c_oposition == '右前') & (self.label.c_obehavior == '向左变道'))
                                             | ((self.label.c_oposition == '左前') & (self.label.c_obehavior == '变道向右'))
                                             | ((self.label.c_oposition == '右前') & (self.label.c_obehavior == '变道向左'))
                                     )
                                     & (self.label.c_sensor_type == 'A')]
                for i, row in c_label.iterrows():
                    # 获取起始时间
                    start_time = round(row['c_p_starttime'], 1)
                    end_time = round(row['c_p_endtime'], 1)
                    new_id = row['c_newid']
                    session_id = row['c_session'].strip()
                    scenario = LaneChangeScenario(df_vehicle, df_object, start_time, end_time, new_id, session_id)
                    if scenario.check_nan():
                        scenario_list.append(scenario)
            print(f'数据读取完毕，共记{len(scenario_list)}条数据')
            # 缓存
            with open('scenario', 'wb') as f:
                pickle.dump(scenario_list, f)
        #
        print(str(scenario_list))

        ego_v = np.array([t.ego_car.velocity_x for t in scenario_list])
        ego_y_v = np.array([np.abs(t.ego_car.velocity_y) for t in scenario_list])
        distance = np.array([np.abs(t.obj_car.displacement_x) for t in scenario_list])
        relative_v = np.array([t.obj_car.relative_velocity_x for t in scenario_list])

        ego_a = np.array([t.ego_car.acceleration_x for t in scenario_list])
        obj_v = np.array([t.obj_car.velocity_x for t in scenario_list])
        obj_a = np.array([t.obj_car.acceleration_x for t in scenario_list])

        # 最开始做的版本，采用本车速度去拟合其他属性
        # self.fit2(ego_v, ego_a, obj_v, obj_a, distance, relative_v)
        # 之后提出的新需求，两两曲线拟合
        # self.fit(ego_v, ego_y_v, distance, relative_v)
        #
        # time = np.array([t.change_time for t in scenario_list])
        # self.fit_time(time, ego_v, distance, relative_v)
        # 危险场景
        generate_critical(scenario_list=scenario_list)


    def generate_point(self):
        # 变道超车，并返回原车道的情景
        lst1 = []
        # 变道超车，在对应时间内未返回原车道的场景
        lst2 = []
        for file_group in self.config.file_groups:
            # 读取数据
            df_vehicle = pd.read_csv(file_group.vehicle_path, encoding=self.config.encoding)
            df_object = pd.read_csv(file_group.obj_path, encoding=self.config.encoding)
            # 读取标注数据，要保证session_id的一致性
            c_label = self.label[(self.label.Session == file_group.session_id)
                                 & (self.label.AdditionalDescription == self.config.additional_description)
                                 & (self.label.OPosition == self.config.o_position)
                                 & (self.label.SensorType == 'A')
                                 & (self.label.OBehavior == '循线')]
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

    '''
        四个维度两两拟合
    '''

    def fit(self, ego_v, ego_y_v, distance, relative_v):
        # 计算速度的最大最小区间
        s_max = int(np.max(ego_v) + 1)
        s_min = int(np.min(ego_v) - 1)

        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1
        # 将本车速度分区
        ego_v_cluster = []

        # 本车速度-相对速度 ego-v relative-v
        ev_rv_par = []
        # 本车速度-距离 ego-v distance
        ev_dis_par = []
        # 本车速度-本车横向速度 ego-v ego-y-v
        ev_eyv_par = []

        # 获取每个区域内的最大最小值，遍历区间比拆分区间大一
        for i in range(6):
            ran_speed = np.where((ego_v > s_min + i * step) & (ego_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                ego_v_cluster.append(s_min + i * step + step / 2)
                ev_rv_par.append(MathParameter(relative_v[ran_speed]))
                ev_dis_par.append(MathParameter(distance[ran_speed]))
                ev_eyv_par.append(MathParameter(ego_y_v[ran_speed]))

        # 计算速度的最大最小区间
        s_max = int(np.max(relative_v) + 1)
        s_min = int(np.min(relative_v) - 1)

        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1

        relative_v_cluster = []

        # 相对速度-本车速度 relative-v ego-v
        rv_ev_par = []
        # 相对速度-距离 relative-v distance
        rv_dis_par = []
        # 相对速度-本车横向速度 relative-v ego-y-v
        rv_eyv_par = []

        # 获取每个区域内的最大最小值，遍历区间比拆分区间大一
        for i in range(6):
            ran_speed = np.where((relative_v > s_min + i * step) & (relative_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                relative_v_cluster.append(s_min + i * step + step / 2)
                rv_ev_par.append(MathParameter(ego_v[ran_speed]))
                rv_dis_par.append(MathParameter(distance[ran_speed]))
                rv_eyv_par.append(MathParameter(ego_y_v[ran_speed]))

        # 计算速度的最大最小区间
        s_max = int(np.max(distance) + 1)
        s_min = int(np.min(distance) - 1)

        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1

        distance_cluster = []

        # 距离-本车速度 distance ego-v
        dis_ev_par = []
        # 距离-相对速度 distance relative-v
        dis_rv_par = []
        # 距离-本车横向速度 distance ego-y-v
        dis_eyv_par = []

        # 获取每个区域内的最大最小值，遍历区间比拆分区间大一
        for i in range(6):
            ran_speed = np.where((distance > s_min + i * step) & (distance < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                distance_cluster.append(s_min + i * step + step / 2)
                dis_ev_par.append(MathParameter(ego_v[ran_speed]))
                dis_rv_par.append(MathParameter(relative_v[ran_speed]))
                dis_eyv_par.append(MathParameter(ego_y_v[ran_speed]))

        # 计算速度的最大最小区间
        s_max = int(np.max(ego_y_v) + 1)
        s_min = int(np.min(ego_y_v) - 1)

        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1

        ego_y_v_cluster = []
        # 本车横向速度-本车速度 ego-y-v ego-v
        eyv_ev_par = []
        # 本车横向速度-相对速度 ego-y-v relative-v
        eyv_rv_par = []
        # 本车横向速度-距离 ego-y-v distance
        eyv_dis_par = []

        # 获取每个区域内的最大最小值，遍历区间比拆分区间大一
        for i in range(6):
            ran_speed = np.where((ego_y_v > s_min + i * step) & (ego_y_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                ego_y_v_cluster.append(s_min + i * step + step / 2)
                eyv_ev_par.append(MathParameter(ego_v[ran_speed]))
                eyv_rv_par.append(MathParameter(relative_v[ran_speed]))
                eyv_dis_par.append(MathParameter(distance[ran_speed]))

        # 以下是数据拟合部分以及画图部分
        # 设置颜色和多项式的阶数
        degrees = [1]
        colors = ['b']
        font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15, }
        plt.figure(figsize=(20, 20))
        plt.subplot(4, 4, 1)
        plt.subplot(4, 4, 2)
        draw(ego_v, relative_v, ego_v_cluster, ev_rv_par, degrees, colors, '../parameters/ev_rv', 'ego-v', 'relative_v')
        plt.subplot(443)
        draw(ego_v, distance, ego_v_cluster, ev_dis_par, degrees, colors, '../parameters/ev_dis', 'ego-v', 'distance')
        plt.subplot(444)
        draw(ego_v, ego_y_v, ego_v_cluster, ev_eyv_par, degrees, colors, '../parameters/ev_eyv', 'ego-v', 'ego-y-v')

        plt.subplot(445)
        draw(relative_v, ego_v, relative_v_cluster, rv_ev_par, degrees, colors, '../parameters/rv_ev', 'relative_v',
             'ego-v')
        plt.subplot(447)
        draw(relative_v, distance, relative_v_cluster, rv_dis_par, degrees, colors, '../parameters/rv_dis',
             'relative_v', 'distance')
        plt.subplot(448)
        draw(relative_v, ego_y_v, relative_v_cluster, rv_eyv_par, degrees, colors, '../parameters/rv_e_y_v',
             'relative_v', 'ego-y-v')

        plt.subplot(449)
        draw(distance, ego_v, distance_cluster, dis_ev_par, degrees, colors, '../parameters/dis_ev', 'distance',
             'ego-v')
        plt.subplot(4, 4, 10)
        draw(distance, relative_v, distance_cluster, dis_rv_par, degrees, colors, '../parameters/dis_rv', 'distance',
             'relative_v')
        plt.subplot(4, 4, 12)
        draw(distance, ego_y_v, distance_cluster, dis_eyv_par, degrees, colors, '../parameters/dis_eyv', 'distance',
             'ego_y_v')

        plt.subplot(4, 4, 13)
        draw(ego_y_v, ego_v, ego_y_v_cluster, eyv_ev_par, degrees, colors, '../parameters/eyv_ev', 'ego_y_v', 'ego-v')
        plt.subplot(4, 4, 14)
        draw(ego_y_v, relative_v, ego_y_v_cluster, eyv_rv_par, degrees, colors, '../parameters/eyv_rv', 'ego_y_v',
             'relative_v')
        plt.subplot(4, 4, 15)
        draw(ego_y_v, distance, ego_y_v_cluster, eyv_dis_par, degrees, colors, '../parameters/eyv_dis', 'ego_y_v',
             'distance')
        plt.show()
        return

    @staticmethod
    def fit2(ego_v, ego_a, obj_v, obj_a, distance, relative_v):
        # 计算速度的最大最小区间
        s_max = int(np.max(ego_v) + 1)
        s_min = int(np.min(ego_v) - 1)

        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1

        # 将本车速度分区
        speed_cluster = []
        obj_speed_cluster = []
        relative_speed_cluster = []
        distance_cluster = []
        y_speed_cluster = []

        a_par = []
        obj_speed_par = []
        obj_a_par = []
        distance_par = []
        distance_relative_par = []

        # 获取每个区域内的最大最小值，遍历区间比拆分区间大一
        # 本车速度相关性分析
        # 本车速度->本车加速度、目标车速度、距离
        for i in range(6):
            ran_speed = np.where((ego_v > s_min + i * step) & (ego_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                speed_cluster.append(s_min + i * step + step / 2)
                a_par.append(MathParameter(ego_a[ran_speed]))
                obj_speed_par.append(MathParameter(obj_v[ran_speed]))
                distance_par.append(MathParameter(distance[ran_speed]))
        # 目标车速度相关性分析
        # 目标车速度->目标车加速度
        s_max = int(np.max(obj_v) + 1)
        s_min = int(np.min(obj_v) - 1)
        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1
        for i in range(6):
            ran_speed = np.where((obj_v > s_min + i * step) & (obj_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 1:
                obj_speed_cluster.append(s_min + i * step + step / 2)
                obj_a_par.append(MathParameter(obj_a[ran_speed]))
        # 相对速度相关性分析
        # 相对速度->距离
        s_max = int(np.max(relative_v) + 1)
        s_min = int(np.min(relative_v) - 1)
        step = int((s_max - s_min) / 5) + 1
        for i in range(6):
            ran_speed = np.where((relative_v > s_min + i * step) & (relative_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                relative_speed_cluster.append(s_min + i * step + step / 2)
                distance_relative_par.append(MathParameter(distance[ran_speed]))

        # 以下是数据拟合部分以及画图部分
        # 设置颜色和多项式的阶数
        degrees = [1]
        colors = ['b']
        font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15, }
        plt.figure(figsize=(30, 20))
        plt.subplot(2, 3, 1)
        # 本车速度，本车加速度
        draw(ego_v, ego_a, speed_cluster, a_par, degrees, colors, '../parameters/ev_ea', 'ego-v', 'ego-a')
        plt.subplot(2, 3, 2)
        # 本车速度，目标车速度
        draw(ego_v, obj_v, speed_cluster, obj_speed_par, degrees, colors, '../parameters/ev_ov', 'ego-v', 'obj-v')
        plt.subplot(2, 3, 3)
        # 本车速度，距离
        draw(ego_v, distance, speed_cluster, distance_par, degrees, colors, '../parameters/ev_dis', 'ego-v',
             'distance')
        plt.subplot(2, 3, 4)
        # 目标车速度，目标车加速度
        draw(obj_v, obj_a, obj_speed_cluster, obj_a_par, degrees, colors, '../parameters/ov_oa', 'obj-v', 'obj-a')
        plt.subplot(2, 3, 5)
        # 相对速度, 距离
        draw(relative_v, distance, relative_speed_cluster, distance_relative_par, degrees, colors,
             '../parameters/rv_dis', 'relative-v', 'distance')
        plt.show()
        return

    @staticmethod
    def fit_time(time, ego_v, relative_v, displacement):
        ego_v_cluster = []
        relative_v_cluster = []
        displacement_cluster = []

        time_ego_v_par = []
        time_relative_v_par = []
        time_displacement_par = []

        # g = []

        # 计算速度的最大最小区间
        s_max = int(np.max(ego_v) + 1)
        s_min = int(np.min(ego_v) - 1)
        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1
        # 本车速度->变道极值时间
        # g.append(s_min)
        for i in range(6):
            ran_speed = np.where((ego_v > s_min + i * step) & (ego_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                ego_v_cluster.append(s_min + i * step + step / 2)
                time_ego_v_par.append(MathParameter(time[ran_speed]))
                # g.append(s_min + (i + 1) * step)
        # 计算速度的最大最小区间
        s_max = int(np.max(relative_v) + 1)
        s_min = int(np.min(relative_v) - 1)
        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1
        # 本车速度->变道极值时间
        for i in range(6):
            ran_speed = np.where((relative_v > s_min + i * step) & (relative_v < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                relative_v_cluster.append(s_min + i * step + step / 2)
                time_relative_v_par.append(MathParameter(time[ran_speed]))

        # 计算速度的最大最小区间
        s_max = int(np.max(displacement) + 1)
        s_min = int(np.min(displacement) - 1)
        # 当数据量大的时候可以酌情考虑将区间加大，目前设置成5
        step = int((s_max - s_min) / 5) + 1
        # 本车速度->变道极值时间
        for i in range(6):
            ran_speed = np.where((displacement > s_min + i * step) & (displacement < s_min + (i + 1) * step))
            if len(ran_speed[0]) > 0:
                displacement_cluster.append(s_min + i * step + step / 2)
                time_displacement_par.append(MathParameter(time[ran_speed]))

        degrees = [1]
        colors = ['b']
        font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15, }
        plt.figure(figsize=(20, 20))
        # 本车速度-变道时间
        plt.subplot(2, 2, 1)
        draw(ego_v, time, ego_v_cluster, time_ego_v_par, degrees, colors, '../parameters/ev_time', 'ego_v', 'time')
        # for li in g:
        #     plt.vlines(li, -6, 12, colors="c", linestyles="dashed")
        # 相对速度-变道时间
        plt.subplot(2, 2, 2)
        draw(relative_v, time, relative_v_cluster, time_relative_v_par, degrees, colors,
             '../parameters/rv_time', 'relative_v', 'time')

        # 两车距离-变道时间
        plt.subplot(2, 2, 3)
        draw(displacement, time, displacement_cluster, time_displacement_par, degrees, colors, '../parameters/dis_time',
             'displacement', 'time')

        plt.show()
