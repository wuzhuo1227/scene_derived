# scene_derived

## Repository Structure

<pre/>
- act.py
  | 动作序列表
- obj.py
  | 参与者表
- vehicle.py
  | 本车表
- generate_main.py
  | 场景生成代码
- curve_fit.py
  | 曲线拟合功能函数文件
- get_boundary.py
  | 依据本车速度获取目标车速度和纵向距离范围，包含绘图代码
- get_boundary_realSpeed.py
  | 依据相对速度获取纵向距离范围，包含绘图代码
- cor.py
  | 参数间相关性分析
</pre>

## Usage

### Plot the curve between the parameters

```python
python get_boundary.py
```

```python
python get_boundary_realSpeed.py
```