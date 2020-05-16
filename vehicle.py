import csv


class Vehicle:

    def __init__(self):
        self.car_id = 1
        self.scene_id = ""
        self.type = "小型汽车"
        self.color = "黑"
        self.speed = 0
        self.acceleration = 0
        self.lane = 2
        self.yaw = 0
        self.action = "向右变道"
        self.turn_light_state = "右转灯亮"
        self.light_state = "未照明"
        self.brake_light_state = "不亮"
        self.xml = ""


    def write_to_csv(self):
        f = open('vehicle1.csv', 'a+', encoding='utf-8-sig')
        writer = csv.writer(f)
        # writer.writerow(['car_id', 'scene_id', 'type', 'color', 'speed', 'acceleration', 'lane', 'yaw', 'action',
        #                  'turn_light_state', 'light_state', 'brake_light_state', 'xml'])
        data = [(str(self.car_id), self.scene_id, self.type, self.color, str(self.speed), str(self.acceleration), str(self.lane),
                str(self.yaw), self.action, self.turn_light_state, self.light_state, self.brake_light_state, self.xml)]
        writer.writerows(data)
        f.close()
        