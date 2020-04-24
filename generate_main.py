import vehicle
import obj
import numpy as np

def meet_slow_car(s_id):
    v1 = vehicle.Vehicle()
    o1 = obj.Object()

    v1.scene_id = "循线行驶遇慢车_" + str(s_id)
    o1.scene_id = "循线行驶遇慢车_" + str(s_id)

    speed1 = np.random.randint(low=100, high=120)
    speed2 = np.random.randint(low=60, high=speed1)

    v1.speed = speed1
    o1.speed = speed2

    v1.write_to_csv()
    o1.write_to_csv()

def change_lane():
    v1 = vehicle.Vehicle()
    o1 = obj.Object()

    speed1 = np.random.randint(low=100, high=120)
    speed2 = np.random.randint(low=60, high=speed1)

    v1.speed = speed1
    o1.speed = speed2

    v1.yaw = np.random.randint(low=-20, high=20)

    v1.write_to_csv()
    o1.write_to_csv()

def follow_road(s_id):
    v1 = vehicle.Vehicle()
    o1 = obj.Object()

    v1.scene_id = "循线跟车_" + str(s_id)
    o1.scene_id = "循线跟车_" + str(s_id)

    distance = np.random.randint(low=180, high=300)

    o1.y_position = distance

    v1.speed = distance / 3  #安全速度的临界点
    o1.speed = np.random.randint(low=60, high=120)

    v1.write_to_csv()
    o1.write_to_csv()




if __name__=="__main__":
    for i in range(10):
        # meet_slow_car(i)
        follow_road(i)
