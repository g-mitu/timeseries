import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""字典形式导入数据"""
x1 = {'Measure_1': [28.4,28.9,29.0,28.4,28.6], 
      'Measure_2': [28.4,29.0,29.1,28.5,28.6], 
      'Measure_3': [28.4,29.0,29.1,28.5,28.6]}   # A测定员
x2 = {'Measure_1': [28.5,28.8,29.0,28.5,28.6], 
      'Measure_2': [28.4,28.9,29.0,28.5,28.6], 
      'Measure_3': [28.4,28.8,29.0,28.5,28.6]}   # B测定员
x3 = {'Measure_1': [28.4,28.9,28.9,28.4,28.6], 
      'Measure_2': [28.5,28.9,28.9,28.5,28.7], 
      'Measure_3': [28.5,28.9,29.0,28.4,28.7]}   # C测定员


"""数据转换成DataFrame存储方便画图"""
df1 = pd.DataFrame(x1)
x1_bar = df1.mean().mean()
R1 = (df1.max(axis=1) - df1.min(axis=1)).sum()/5
df1['sample_no'] = ['#'+str(i) for i in range(1,6)]
df1['researcher'] = 'A'

df2 = pd.DataFrame(x2)
x2_bar = df2.mean().mean()
R2 = (df2.max(axis=1) - df2.min(axis=1)).sum()/5
df2['sample_no'] = ['#'+str(i) for i in range(1,6)]
df2['researcher'] = 'B'

df3 = pd.DataFrame(x3)
x3_bar = df3.mean().mean()
R3 = (df3.max(axis=1) - df3.min(axis=1)).sum()/5
df3['sample_no'] = ['#'+str(i) for i in range(1,6)]
df3['researcher'] = 'C'

df = pd.concat([df1,df2,df3],ignore_index=True)     # ABC测定员3组数据连接在同一张表
"""
    Measure_1  Measure_2  Measure_3 sample_no researcher
0        28.4       28.4       28.4        #1          A
1        28.9       29.0       29.0        #2          A
2        29.0       29.1       29.1        #3          A
3        28.4       28.5       28.5        #4          A
"""

"""X-bar Chart"""
A2 = 1.023
xbarbar = (x1_bar+x2_bar+x3_bar)/3
rbar = (R1+R2+R3)/3
ucl = xbarbar + A2 * rbar
lcl = xbarbar - A2 * rbar
print(df1.mean())
print(rbar,ucl,lcl)

grouped = df.groupby('researcher')    # 按照researcher来分组
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(16,4), sharey=True)     # 定义包含1行3列子图
fig.suptitle('Xbar Chart', fontsize=18, y=0)

for (key, ax) in zip(grouped.groups.keys(), axes.flatten()):
    df_group = grouped.get_group(key)[['Measure_1','Measure_2','Measure_3']].mean(axis=1)
    # print(key) #A\B\C
    # print(df_group)
    df_group.index = range(1,6)     # 取样本编号1,2,3,4,5作为x轴
    df_group.plot(ax=ax, xticks=df_group.index, title=key, label='sample', style='go-', linewidth=2)    # sample
    ax.plot(range(1,6),xbarbar*np.ones(5),'k',label=r'$\bar\bar{x}$')    # xbar
    ax.plot(range(1,6),ucl*np.ones(5), label='UCL')      # ucl
    ax.plot(range(1,6),lcl*np.ones(5), label='LCL')      # lcl
    ax.legend()
    ax.grid(False)     # 隐藏网格
plt.show()