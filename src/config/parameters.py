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
    def __init__(self, session_id, obj_path, vehicle_path):
        self.vehicle_path = vehicle_path
        self.obj_path = obj_path
        self.session_id = session_id


class Function:
    def __init__(self, file_path):
        self.pars = []
        self.load_file(file_path)

    def load_file(self, file_path):
        with open(file_path) as file:
            for line in file:
                self.pars.append(line.split(':')[1].split(','))

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
