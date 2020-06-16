# coding=utf-8
import pandas as pd
from scipy import stats
import numpy as np

df_coverage = pd.read_csv('data/change_lane.csv')
print("spearman")
print(df_coverage.corr('spearman'))

speed = df_coverage['speed'].values.tolist()
distance = df_coverage['distance'].values.tolist()

z1 = np.polyfit(distance, speed, 1) # 用3次多项式拟合
p1 = np.poly1d(z1)
print(p1) # 在屏幕上打印拟合多项式

z1 = np.polyfit(speed, distance, 1) # 用3次多项式拟合
p1 = np.poly1d(z1)
print(p1) # 在屏幕上打印拟合多项式



# p = df_coverage['p'].values.tolist()
# errorRate = df_coverage['errorRate'].values.tolist()
#
# # lsc = df_coverage['lsc'].values.tolist()
# # dsc = df_coverage['dsc'].values.tolist()
# topk = df_coverage['topk'].values.tolist()
# nc = df_coverage['nc'].values.tolist()
#
# nbc = df_coverage['nbc'].values.tolist()
# snac = df_coverage['snac'].values.tolist()
# kmnc = df_coverage['kmnc'].values.tolist()
#
# print("  ")

# corr,p = stats.spearmanr(p,lsc)
# print("probability of adv-lsc", "corr为:", corr, "p值为:", p)
#
# p = df_coverage['p'].values.tolist()
# corr,p = stats.spearmanr(p,dsc)
# print("probability of adv-dsc", "corr为:", corr, "p值为:", p)
#
# print("  ")
#
#
# errorRate = df_coverage['errorRate'].values.tolist()
# corr,p = stats.spearmanr(errorRate,lsc)
# print("error rate-lsc", "corr为:", corr, "p值为:", p)
#
# errorRate = df_coverage['errorRate'].values.tolist()
# corr,p = stats.spearmanr(errorRate,dsc)
# print("error rate-dsc", "corr为:", corr, "p值为:", p)

# p = df_coverage['p'].values.tolist()
# corr,p = stats.spearmanr(p,topk)
# print("probability of adv-topk", "corr为:", corr, "p值为:", p)
#
# p = df_coverage['p'].values.tolist()
# corr,p = stats.spearmanr(p,nc)
# print("probability of adv-neuron coverage", "corr为:", corr, "p值为:", p)
#
# p = df_coverage['p'].values.tolist()
# corr,p = stats.spearmanr(p,nbc)
# print("probability of adv-neuron boundary coverage", "corr为:", corr, "p值为:", p)
#
# p = df_coverage['p'].values.tolist()
# corr,p = stats.spearmanr(p,snac)
# print("probability of adv-strong neuron activation coverage", "corr为:", corr, "p值为:", p)
#
# p = df_coverage['p'].values.tolist()
# corr,p = stats.spearmanr(p,kmnc)
# print("probability of adv-kmnc", "corr为:", corr, "p值为:", p)
