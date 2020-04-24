from openpyxl import load_workbook

import pandas as pd
from scipy import stats
import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df_object = pd.read_csv('data/nds-sync-object1.csv',encoding="ISO-8859-1")
df_vehicle = pd.read_csv('data/nds-sync-vehicle1.csv',encoding="ISO-8859-1")

workbook = load_workbook(u'data/ScenariosLabeling2tianda.xlsx')    #找到需要xlsx文件的位置
booksheet = workbook.active

AdditionalDescription = booksheet['H']
OPosition = booksheet['L']
CBehavior = booksheet['G']

distance = df_object.loc[:,'RC']
distance = np.array(distance)
print(distance.shape)

rel_speed = df_object.loc[:,'VXRel']
rel_speed = np.array(rel_speed)

na = []
for n in range(distance.shape[0]):
    # print(n)
    if distance[n] == 'na':
        # print(n)
        na.append(n)
        #speed = np.delete(speed, n, axis=0)
        #a = np.delete(a, n, axis=0)

print(len(na))

distance = np.delete(distance,na, axis=0)
rel_speed = np.delete(rel_speed,na, axis=0)
print(distance.shape)
print(np.max(distance))
print(np.min(distance))

distance = distance.astype(np.float64)
rel_speed = rel_speed.astype(np.float64)

rel_speed1 = []
distance1 = []

for i in range(rel_speed.shape[0]):
    if rel_speed[i] > 40 and rel_speed[i] < 60:
        rel_speed1.append(rel_speed[i])
        distance1.append(distance[i])
rel_speed1 = np.array(rel_speed1)
distance1 = np.array(distance1)

# distance1 = distance
# rel_speed1 = rel_speed

distance1 = distance1.reshape(-1,1)
rel_speed1 = rel_speed1.reshape(-1,1)

reg = LinearRegression().fit(rel_speed1, distance1)
print("一元回归方程为:  Y = %.5fX + (%.5f)" % (reg.coef_[0][0], reg.intercept_[0]))
print("R平方为: %s" % reg.score(rel_speed1, distance1))

plt.scatter(rel_speed1, distance1,  color='black')
plt.plot(rel_speed1, reg.predict(rel_speed1), color='red', linewidth=1)
plt.show()