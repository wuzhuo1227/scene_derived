# 场景衍生算法说明
目录结构
```
.
├── README.md
├── data  保存数据的文件
│   ├── ScenariosLabeling2tianda.csv
│   ├── ScenariosLabeling2tianda.xlsx
│   ├── nds-sync-line-14.csv
│   ├── nds-sync-line-16.csv
│   ├── nds-sync-object-14.csv
│   ├── nds-sync-object-16.csv
│   ├── nds-sync-vehicle-14.csv
│   └── nds-sync-vehicle-16.csv
├── parameters 生成的参数文件，其中包含4种线性拟合的方程参数
│   ├── objv_obja_max.txt 目标车速度-目标车加速度-上界函数
│   ├── objv_obja_min.txt 目标车速度-目标车加速度-下界函数
│   ├── real_distance_max.txt 相对速度-距离-上界函数
│   ├── real_distance_min.txt 相对速度-距离-下界函数
│   ├── speed_a_max.txt 本车速度-本车加速度-上界函数
│   ├── speed_a_min.txt 本车速度-本车加速度-下界函数
│   ├── speed_distance_max.txt 速度-距离-上界函数
│   ├── speed_distance_min.txt 速度-距离-下界函数
│   ├── speed_objv_max.txt 速度-目标车速度-上界函数
│   └── speed_objv_min.txt 速度-目标车速度-下界函数
├── scene 生成的场景数据
│   ├── obj.csv 目标车属性
│   └── vehicle.csv 本车属性
└── src
    ├── config 参数配置类
    │   └── parameters.py
    ├── core
    │   ├── act.py  动作类
    │   ├── cor.py
    │   ├── curve_fit.py 线性拟合方法类
    │   ├── data_extraction.py 
    │   ├── dis_speed.py
    │   ├── generate_data.py
    │   ├── generate_main.py 数据生成类
    │   ├── get_boundary.py 
    │   ├── obj.py 目标实体类
    │   ├── read_data.py 数据处理类，包括了读取数据、处理数据以及拟合数据的过程
    │   ├── three_d.py 
    │   └── vehicle.py 本车类
    └── main.py 
```

使用方法：
```python
# main.py
# 输入数据参数
groups = [Group(obj_path='../data/nds-sync-object-14.csv',
                vehicle_path='../data/nds-sync-vehicle-14.csv', session_id='20190623-14-53-38'),
          Group(obj_path='../data/nds-sync-object-16.csv',
                vehicle_path='../data/nds-sync-vehicle-16.csv', session_id='20190623-16-33-14')]
config = Config(file_groups=groups, label_path='../data/ScenariosLabeling2tianda.csv',
                o_position='前', additional_description='变道超车', encoding='ISO-8859-1')
file_util = FileUtil(config)
# parameters is stored in parameters folder
file_util.get_data()
```

上述方法调用结束后会在parameters文件夹下面生成参数文件，接着调用`generate_main`文件，会在scene中生成相关的场景参数文件。
具体流程参见代码中的注释。