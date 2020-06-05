import csv


class Act:

    def __init__(self):
        self.scene_id = ""
        self.car_id = 1
        self.action = "向右变道"
        self.begin_time = 0
        self.duration_time = 6
        self.target_speed = 0

    def write_to_csv(self):
        f = open('action1.csv', 'a+', encoding='utf-8-sig')
        writer = csv.writer(f)
        # writer.writerow(['car_id', 'scene_id', 'type', 'color', 'speed', 'acceleration', 'lane', 'yaw', 'action',
        #                  'turn_light_state', 'light_state', 'brake_light_state', 'xml'])
        data = [(self.scene_id, str(self.car_id), self.action, str(self.begin_time), str(self.duration_time), str(self.target_speed))]
        writer.writerows(data)
        f.close()