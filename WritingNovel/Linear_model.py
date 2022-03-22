# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# matplotlib画图中中文显示会有问题，需要这两行设置默认字体

plt.xlabel('n')
plt.ylabel('Time/ns')
plt.xlim(xmax=30, xmin=5)
plt.ylim(ymax=50, ymin=5)
# 画两条（0-9）的坐标轴并设置轴标签x，y
data1 = [8.28, 10.76, 12.88, 13.2, 15.08, 15.6, 17.64, 19.0, 21.08, 20.82,
         22.52, 24.8, 23.6, 27.86, 29.72, 32.38, 32.14, 37.68, 35.6, 36.44,
         35.96, 38.6, 39.52, 40.7, 42.74, 44.52]
data2 = [9.7, 11.8, 13.48, 15.78, 15.36, 17.84, 18.64, 19.76, 21.96, 22.42,
         24.48, 31.08, 29.8, 31.26, 32.8, 36.24, 35.46, 39.0, 35.58, 41.64,
         41.42, 42.44, 44.46, 45.22, 46.06, 47.44]
plt.title("约瑟夫问题的两种解法时间分析")

x1 = np.arange(5, 31, 1)
y1 = np.array(data1)
y2 = np.array(data2)
# 线性拟合
p1 = np.polyfit(x1, y1, 1)
ry1 = np.polyval(p1, x1)
p2 = np.polyfit(x1, y2, 1)
ry2 = np.polyval(p2, x1)

colors1 = '#fab1a0'  # 点的颜色
colors2 = '#0984e3'
area = np.pi * 4 ** 2  # 点面积
# 画散点图
plt.plot(x1, ry1, colors1, label='数组_拟合曲线')
plt.plot(x1, ry2, colors2, label='链表_拟合曲线')
plt.scatter(x1, y1, s=area, c=colors1, alpha=0.8, label='循环数组')
plt.scatter(x1, y2, s=area, c=colors2, alpha=0.8, label='循环链表')
# plt.plot([5, 30], [8.9, 46], linewidth='1', color='#000000')
plt.legend()
# plt.grid('True')
plt.savefig('1.png', dpi=300)
plt.show()

df = pd.DataFrame(columns=['人数n'],data = x1)
df['CArray_time'] = data1
df['CList_time'] = data2
print(df)
print('')
print(df.corr('pearson'))

