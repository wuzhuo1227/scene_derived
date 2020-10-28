import csv

from src.config.parameters import Config
from src.config.parameters import Group
from src.core.read_data import FileUtil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from src.core.curve_fit import polynomial_fit
from scipy import signal
import os
from src.config.parameters import Function

if __name__ == '__main__':
    # f_min = Function('../parameters/dis_evy_min.txt')
    # f_max = Function('../parameters/ev_dis_max.txt')
    # exit(0)
    # x_l = np.arange(0.1, 10, 0.1)
    # y_l = np.arange(0.1, 10, 0.1)
    # z_l = np.arange(0.1, 10, 0.1)
    # x_list = []
    # y_list = []
    # z_list = []
    # m = np.ones((len(x_l), len(y_l), len(z_l)))
    # for i in range(len(x_l)):
    #     for j in range(len(y_l)):
    #         for k in range(len(z_l)):
    #             m[i][j][j] = 1
    # print(m.shape)
    #
    # # figure = plt.figure(figsize=(30, 20))
    # # axs = Axes3D(figure)
    # # axs.scatter3D(x_list, y_list, z_list, cmap='Blues', alpha=0.6)
    # # # axs.scatter3D(error_x, error_y, good_point_z, c='lightcoral', s=10,  alpha=0.6)
    # # plt.show()
    # exit(0)

    # test()
    # exit(0)
    # Folder_Path = r'/Users/liebes/Downloads/temp'  # 要拼接的文件夹及其完整路径，注意不要包含中文
    # SaveFile_Path = r'/Users/liebes/Downloads/temp'  # 拼接后要保存的文件路径
    # SaveFile_Name = r'all.csv'  # 合并后要保存的文件名
    #
    # # 修改当前工作目录
    # os.chdir(Folder_Path)
    # # 将该文件夹下的所有文件名存入一个列表
    # file_list = os.listdir()
    #
    # # 读取第一个CSV文件并包含表头
    # df = pd.read_csv(Folder_Path + '/' + file_list[0])  # 编码默认UTF-8，若乱码自行更改
    #
    # # 将读取的第一个CSV文件写入合并后的文件保存
    # df.to_csv(SaveFile_Path + '/' + SaveFile_Name, encoding="utf_8_sig", index=False)
    #
    # # 循环遍历列表中各个CSV文件名，并追加到合并后的文件
    # for i in range(1, len(file_list)):
    #     df = pd.read_csv(Folder_Path + '/' + file_list[i])
    #     df.to_csv(SaveFile_Path + '/' + SaveFile_Name, encoding="utf_8_sig", index=False, header=False, mode='a+')
    # exit(0)
    # data = pd.read_csv('/Users/liebes/project/laboratory/scene_derived/data/t_nds_obj_first_2.csv', encoding='utf-8')
    # data[u'c_session'] = data[u'c_session'].astype(str)
    # data[u'c_session'] = data[u'c_session'].apply(lambda x: x.strip())
    # data.to_csv('/Users/liebes/project/laboratory/scene_derived/data/t_nds_obj_first_2.csv', index=False, encoding='utf-8')
    # exit(0)

    # vehicle = pd.read_csv('/Users/liebes/project/laboratory/scene_derived/data/t_nds_vehicle_first_2.csv',
    #                       encoding='UTF-8')
    # obj = pd.read_csv('/Users/liebes/project/laboratory/scene_derived/data/t_nds_obj_first_2.csv',
    #                       encoding='UTF-8')
    # lst = obj[(obj.n_publicid == 248) & (obj.c_session == '20190617-10-53-49')]
    # # lst = vehicle[(vehicle.c_session == '20190617-10-53-49') & (vehicle.c_time < 17.4) & (vehicle.c_time > 11.1)]
    # print(lst['c_time'])
    # exit(0)

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
    groups = [
        Group(obj_path='../data/t_nds_obj_first_2.csv',
              vehicle_path='../data/t_nds_vehicle_first_2.csv')
    ]
    config = Config(file_groups=groups, label_path='../data/t_high_way_scenario_2.csv',
                    o_position='左前', additional_description='循线', encoding='UTF-8')

    file_util = FileUtil(config)

    # parameters is stored in parameters folder
    file_util.get_data(use_cache=True)

    # file_util.generate_point()
