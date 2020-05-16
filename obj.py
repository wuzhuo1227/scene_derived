import csv


class Object:

    def __init__(self):
        self.scene_id = ""
        self.parti_id = 2
        self.type = "小型汽车"
        self.speed = 0
        self.acceleration = 0
        self.y_position = 200
        self.x_position = 0
        self.yaw = 0
        self.parti_action = "循线行驶"
        self.xml = ""
        self.lane = 2


    def write_to_csv(self):
        f = open('obj1.csv', 'a+', encoding='utf-8-sig')
        writer = csv.writer(f)
        # writer.writerow(['scene_id', 'parti_id', 'type', 'speed', 'acceleration', 'y_position', 'x_position',
        #                  'yaw', 'parti_action', 'xml', 'lane'])
        data = [(self.scene_id, str(self.parti_id), self.type, str(self.speed), str(self.acceleration),
                str(self.y_position), str(self.x_position), str(self.yaw), self.parti_action, self.xml, str(self.lane))]
        writer.writerows(data)
        f.close()