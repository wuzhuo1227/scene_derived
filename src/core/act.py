# coding=utf-8
import csv
import os


# 动作序列表
class Act:

    def __init__(self):
        self.scene_id = ""
        self.car_id = 1
        self.action = "向右变道"
        self.begin_time = 0
        self.duration_time = 6
        self.target_speed = 0

    def write_to_csv(self):
        flag = os.path.exists('../../scene/action.csv')
        f = open('../../scene/action.csv', 'a+', encoding='utf-8-sig')
        writer = csv.writer(f)
        if not flag:
            writer.writerow(['scene_id', 'car_id', 'action', 'begin_time', 'duration_time', 'target_speed'])
        data = [(self.scene_id, str(self.car_id), self.action, str(self.begin_time), str(self.duration_time),
                 str(self.target_speed))]
        writer.writerows(data)
        f.close()
