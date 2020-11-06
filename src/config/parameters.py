import numpy as np


class Config:
    def __init__(self, file_groups, label_path, c_behavior='', o_position='', additional_description='',
                 encoding='ISO-8859-1'):
        self.file_groups = file_groups
        self.additional_description = additional_description
        self.o_position = o_position
        self.c_behavior = c_behavior
        self.label_path = label_path
        self.encoding = encoding


class Group:
    def __init__(self, obj_path, vehicle_path):
        self.vehicle_path = vehicle_path
        self.obj_path = obj_path
        # self.session_id = session_id


class Function:
    def __init__(self):
        self.pars = []
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

    def __init__(self, file_path):
        self.pars = []
        self.load_file(file_path)

    def load_file(self, file_path):
        with open(file_path) as file:
            for line in file:
                p = line.split('|')[0]
                m = line.split('|')[1]
                self.pars.append(p.split(':')[1].split(','))
                ms = m.split(',')
                self.x_min = float(ms[0]) * 1.2
                self.x_max = float(ms[1]) * 1.2
                self.y_min = float(ms[2]) * 1.2
                self.y_max = float(ms[3]) * 1.2

    def get_func(self, x, degree):
        parameters = self.pars[degree - 1]
        parameters = np.array(parameters).astype(np.float64)
        if degree == 1:
            return parameters[0] * x + parameters[1]
        elif degree == 2:
            return parameters[0] * x * x + parameters[1] * x + parameters[2]
        elif degree == 3:
            return parameters[0] * x * x * x + parameters[1] * x * x + parameters[2] * x + parameters[3]
        elif degree == 4:
            return parameters[0] * x * x * x * x + parameters[1] * x * x * x + \
                   parameters[2] * x * x + parameters[3] * x + parameters[4]
        else:
            return x

    def get_rev_func(self):
        parameters = self.pars[0]
        parameters = np.array(parameters).astype(np.float64)
        parameters[1] = -parameters[1] / parameters[0]
        parameters[0] = 1.0 / parameters[0]

        res = Function()
        res.pars.append(parameters)

        return res

    def check(self, x, y):
        return (self.x_min <= x <= self.x_max) and (self.y_min <= y <= self.y_max)
