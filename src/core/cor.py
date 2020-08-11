# coding=utf-8
import pandas as pd
from scipy import stats
import numpy as np

df_coverage = pd.read_csv('data/change_lane.csv')
print("spearman")
print(df_coverage.corr('spearman'))

speed = df_coverage['speed'].values.tolist()
distance = df_coverage['distance'].values.tolist()

print("  ")

corr,p = stats.spearmanr(speed,distance)
print("speed-distance", "corr为:", corr, "p值为:", p)

