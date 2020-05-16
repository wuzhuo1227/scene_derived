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

def change_lane(s_id):
    v1 = vehicle.Vehicle()   #本车
    o1 = obj.Object()    #同车道前车

    v1.scene_id = "变道超车_" + str(s_id)
    o1.scene_id = "变道超车_" + str(s_id)

    o_front = obj.Object
    o_behind = obj.Object

    speed1 = np.random.randint(low=100, high=120)
    # speed2 = np.random.randint(low=60, high=speed1)
    speed2 = np.random.randint(low=int(0.36672 * speed1 + 39.70254), high=int(1.06516 * speed1 - 4.39557))

    speed_front = np.random.randint(low=int(0.24520 * speed1 + 49.09775), high=int(0.77443 * speed1 + 27.53149))

    v1.speed = speed1
    o1.speed = speed2

    o_front.speed = speed_front

    # v1.acceleration = np.random.randint(low=int(-0.01841 * speed1 + 0.80386), high=int(-0.00537 * speed1 + 1.06788))
    v1.acceleration = np.random.rand()
    # o1.acceleration = np.random.randint(low=int(0.01389 * speed2 - 1.90969), high=int(0.00480 * speed2 + 0.26186))
    o1.acceleration = np.random.rand()
    # o_front.acceleration = np.random.randint(low=int(0.02159 * speed_front - 2.66915), high=int(0.00365 * speed_front + 0.24057))

    diff_speed_front = speed1 - speed_front

    front_distance_max = (2.46191 * diff_speed_front + 146.14920) if (3.25515 * speed1 - 123.02134) > (2.46191 * diff_speed_front + 146.14920) else (3.25515 * speed1 - 123.02134)
    front_distance_min = (3.33244 * diff_speed_front + 76.22992) if (3.33244 * diff_speed_front + 76.22992) > (-0.09651 * speed1 + 30.96327) else (-0.09651 * speed1 + 30.96327)

    o_front.y_position = np.random.randint(low=int(front_distance_min), high=int(front_distance_max))


    diff_speed = speed1 - speed2
    distance_max = (1.26023 * diff_speed + 184.77116) if (3.63505 * speed1 - 153.45529) > (1.26023 * diff_speed + 184.77116) else (3.63505 * speed1 - 153.45529)
    distance_min = (5.27807 * diff_speed + 24.60874) if (5.27807 * diff_speed + 24.60874) > (-0.13771 * speed1 + 58.23334) else (-0.13771 * speed1 + 58.23334)

    o1.y_position = np.random.randint(low=int(distance_min), high=int(distance_max))
    o1.x_position = np.random.rand()

    v1.yaw = np.random.randint(low=0, high=10)

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
        # follow_road(i)
        change_lane(i)
