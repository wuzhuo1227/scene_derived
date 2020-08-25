import numpy as np


class MathParameter:
    def __init__(self, list):
        mean = np.mean(list)
        var = np.var(list)
        u = np.std(list, ddof=1)
        # 平均值 µ
        self.mean = mean
        # 最大值
        self.max = list.max()
        # 最小值
        self.min = list.min()
        # 方差 µ²
        self.var = var
        # 标准差 µ
        self.std = u
        # 标准上界 µ + 3𝛔
        self.max_std = mean + 3 * u
        # 标准下界 µ - 3𝛔
        self.min_std = mean - 3 * u

    def __str__(self):
        return '[%f,%f,%f,%f,%f,%f,%f]' % (self.mean, self.max, self.min,
                                           self.var, self.std, self.max_std, self.min_std)

    def __repr__(self):
        return self.__str__()

