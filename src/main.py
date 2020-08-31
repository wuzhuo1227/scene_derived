from src.config.parameters import Config
from src.config.parameters import Group
from src.core.read_data import FileUtil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.core.curve_fit import polynomial_fit
from scipy import signal
if __name__ == '__main__':
    # df_vehicle = pd.read_csv('../data/nds-sync-vehicle-14.csv')
    # df_vehicle = df_vehicle[(df_vehicle['Time'] <= 141) & (df_vehicle['Time'] >= 133)]
    # time = df_vehicle['Time'].values
    # time -= min(time)
    # a = df_vehicle['Acceleration-y[m/s2]'].values
    # a = np.array(a).astype(np.float64)
    # time = np.array(time).astype(np.float64)
    # plt.figure()
    # f0 = np.polyfit(time, a, 4)
    # f = np.poly1d(f0)
    # # 加速度的二阶导数为距离，常数为0
    # d = f.integ(2)
    # yvals = d(np.arange(0, max(time), 0.001))
    # # print(max(yvals))
    # # print(min(yvals))
    # max_y = max(yvals)
    # min_y = min(yvals)
    # t = -1
    # if abs(max_y) > abs(min_y):
    #     t = max_y
    # else:
    #     t = min_y
    # v = -1
    # for item in (d-t).roots:
    #     if item.imag == 0 and 0 <= item.real <= max(time):
    #         v = item.real
    # # print(yvals)
    # polynomial_fit(time, a, [4], ['b'], 'test.txt', ranges_min=min(time) - 1, ranges_max=max(time) + 1)
    # plt.scatter(time, a)
    # plt.show()
    # exit(0)
    #
    groups = [Group(obj_path='../data/nds-sync-object-14.csv',
                    vehicle_path='../data/nds-sync-vehicle-14.csv', session_id='20190623-14-53-38'),
              Group(obj_path='../data/nds-sync-object-16.csv',
                    vehicle_path='../data/nds-sync-vehicle-16.csv', session_id='20190623-16-33-14')]
    config = Config(file_groups=groups, label_path='../data/ScenariosLabeling2tianda.csv',
                    o_position='前', additional_description='变道超车', encoding='ISO-8859-1')

    file_util = FileUtil(config)

    # parameters is stored in parameters folder
    file_util.get_data()

    # file_util.generate_point()
