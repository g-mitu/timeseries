import numpy as np
import pandas as pd


work_dir = "D:/vs_projects"
data = pd.read_excel(f"{work_dir}/外在缺陷明细报表.xls")  # 读取数据
print(data.head())

d1 = {"A":100,"B":30,"C":10,"D":5}  #"箱"
d2 = {"A":100,"B":30,"C":10,"D":5}  #"条" 
d3 = {"A":200,"B":50,"C":10,"D":5}  #"盒"
d4 = {"A":120,"B":20,"C":8,"D":2}  #"烟支"
d5 = {"A":200,"B":30,"C":10,"D":2}  #"杂项"
d6 = {"C":12,"D":2}  #"物理检测"
d0 = {"箱": d1, "条": d2, "盒": d3, "烟支": d4,"杂项": d5, "物理检测": d6 }
t1 = {'箱':'包装','条':'包装','盒':'包装','烟支':'卷接','杂项':'卷接','物理检测':'卷接'}

def my_func(x,y,w):
    return d0[x][y]*w

data['score'] = data.apply(lambda row: my_func(row['缺陷位置'], row['缺陷等级'],row['缺陷数量']), axis=1)
# 使用apply函数, 如果city字段包含'ing'关键词，则'判断'这一列赋值为1,否则为0
#df['panduan'] = df.city.apply(lambda x: 1 if 'ing' in x else 0)
print(data.head())
print(data.tail(20))
data['gp'] = data['缺陷位置'].apply(lambda x: '包装' if x in ['箱','条','盒']  else '卷接')
data['报检单编号'] = data['报检单编号'].astype(str)
data.to_excel(f"{work_dir}/deal.xlsx", index=False)

#STEP 2
"""
pandas.pivot_table(*data*, *values=None*, *index=None*, *columns=None*, *aggfunc='mean'*, *fill_value=None*, *margins=False*, *dropna=True*, *margins_name='All'*, *observed=False*)

data：dataframe格式数据
values：需要汇总计算的列，可多选==Excel 值
index：行分组键，一般是用于分组的列名或其他分组键，作为结果DataFrame的行索引==Excel 行
columns：列分组键，一般是用于分组的列名或其他分组键，作为结果DataFrame的列索引==Excel 列
aggfunc：聚合函数或函数列表，默认为平均值
fill_value：设定缺失替换值
margins：是否添加行列的总计
dropna：默认为True，如果列的所有值都是NaN，将不作为计算列，False时，被保留
margins_name：汇总行列的名称，默认为All
observed：是否显示观测值
result1 = pd.pivot_table(data,index='洲' , values = ['销售额','利润'] , aggfunc = np.sum)
"""
table = pd.pivot_table(data, values='score', index=['报检单编号', '样品编号'],
                    columns=['gp'], aggfunc=np.sum)
print(table.head())

import matplotlib.pyplot as plt
table.plot.line(figsize=(40, 20))
plt.show()