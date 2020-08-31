import numpy as np


class MathParameter:
    def __init__(self, lst):
        if len(lst) == 1:
            mean = lst[0]
            var = 0
            u = 0
        else:
            mean = np.mean(lst)
            var = np.var(lst)
            u = np.std(lst, ddof=1)
        # 平均值 µ
        self.mean = mean
        # 最大值
        self.max = lst.max()
        # 最小值
        self.min = lst.min()
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

