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
