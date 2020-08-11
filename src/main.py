from src.config.parameters import Config
from src.config.parameters import Group
from src.core.read_data import FileUtil

if __name__ == '__main__':
    groups = [Group(obj_path='../data/nds-sync-object-14.csv',
                    vehicle_path='../data/nds-sync-vehicle-14.csv', session_id='20190623-14-53-38'),
              Group(obj_path='../data/nds-sync-object-16.csv',
                    vehicle_path='../data/nds-sync-vehicle-16.csv', session_id='20190623-16-33-14')]
    config = Config(file_groups=groups, label_path='../data/ScenariosLabeling2tianda.csv',
                    o_position='前', additional_description='变道超车', encoding='ISO-8859-1')

    file_util = FileUtil(config)

    # parameters is stored in parameters folder
    file_util.get_data()


