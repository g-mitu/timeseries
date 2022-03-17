# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 22:40:30 2019
掺配叶丝高架库.csv  cpysgjk
@author: winhl
"""


#-*- coding: utf-8 -*-PART I
#使用K-Means算法聚类消费行为特征数据

import pandas as pd
import numpy as np

#参数初始化
inputfile = 'C:/Users/winhl/Downloads/kongtiao/掺配叶丝高架库.csv' #80w销量及其他属性数据
#/////////////1.Excel格式的一次性导入
#data = pd.read_excel(inputfile, index_col = '时间',nrows=100000,usecols=[0,2,4,6,8,10,12,14,16,18]) #读取数据

#//////////////2.CSV一次性全部导入
#reader = pd.read_csv(inputfile, iterator=True,encoding='gbk') #读取数据
#try:
#    data = reader.get_chunk(100000)
#except StopIteration:
#    print("Iteration is unsucess, stopped")
###///////////
#///////////////3.CSV分块导入，避免内存占用太多

na_vals = ["\\N"," ","","NULL"]
reader = pd.read_csv(inputfile,iterator=True, encoding='gbk',keep_default_na=True,na_values=na_vals)
loop = True
chunkSize = 100000
chunks = []
while loop:
    try:
        chunk = reader.get_chunk(chunkSize)
        chunks.append(chunk)
    except StopIteration:
        loop = False
        print ("Iteration is stopped.")
        
data = pd.concat(chunks, ignore_index=True)
#//////////////////////描述统计
print(data.describe())
print (data.isnull().sum())
data.set_index(['时间'],inplace=True)
data.drop(['设备','湿度平均值','温度平均值'],axis=1,inplace = True)
#////////////////////处理空行、空列
#data.dropna(axis=0,inplace=True)##行包含NAN值
#data.dropna(axis=1,inplace=True)##列包含NAN值
#data.fillna(0,inplace=True)##为空值填充0
#data.dropna(how='all',inplace=True) ##删除行、列均为NAN值
#data=data[data.notnull()]

#data = data[(data!="NaN") & (data>10)]
dict = {x:np.float32 for x in data.columns}
for x in data.columns:
    data[x] = data[x].astype(np.float32)##datetime64,float型就有float16、float32和float64
#data.iloc[:,(1,3,5,7)]

#///////////////一分为2
columns = data.columns.values.tolist()  # 获取列名列表，注意values，tolist的使用
col_wendu = []  # 存储包含‘线索’字段的列名
for i in columns:
    if '温度' in i:
        col_wendu.append(i)
col_shidu = [] # 存储包含‘浏览’字段的列名
for i in columns:
    if '湿度' in i:
        col_shidu.append(i)
data_wd = data[col_wendu]  # 根据列名取列
data_sd = data[col_shidu]

#/////////////
data = data_wd
data_zs = 1.0*(data - data.mean())/data.std() #数据标准化


k = 3 #聚类的类别
iteration = 500 #聚类最大循环次数
from sklearn.cluster import KMeans
model = KMeans(n_clusters = k, n_jobs = 4, max_iter = iteration) #分为k类，并发数4
model.fit(data_zs) #开始聚类

#简单打印结果
r1 = pd.Series(model.labels_).value_counts() #统计各个类别的数目
r2 = pd.DataFrame(model.cluster_centers_) #找出聚类中心
r = pd.concat([r2, r1], axis = 1) #横向连接（0是纵向），得到聚类中心对应的类别下的数目
r.columns = list(data.columns) + [u'类别数目'] #重命名表头
print(r)

#详细输出原始数据及其类别
#outputfile = 'C:/Users/winhl/Downloads/kongtiao/tmp/cdq_data_type.xlsx' #保存结果的文件名
outputfile = 'C:/Users/winhl/Downloads/kongtiao/tmp/type_cpysgjk_wd_data.csv'
r = pd.concat([data, pd.Series(model.labels_, index = data.index)], axis = 1)  #详细输出每个样本对应的类别
r.columns = list(data.columns) + [u'聚类类别'] #重命名表头
#r.to_excel(outputfile)#保存xlsx结果
r.to_csv(outputfile) #保存CSV结果
print('write was done')

def density_plot(data): #自定义作图函数
  import matplotlib.pyplot as plt
  plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
  plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
  plt.rcParams['figure.figsize'] = (8.0,8.0) #用来正常显示负号
  plt.rcParams['image.interpolation']='nearest' #set style
  plt.rcParams['savefig.dpi'] = 300 #图片像素
  plt.rcParams['figure.dpi'] = 300 #分辨率
  p = data.plot(kind='kde', linewidth = 2, subplots = True, sharex = False)
  [p[i].set_ylabel(u'密度') for i in range(data.shape[1])]
  plt.legend()

  plt.tight_layout()
  return plt

pic_output = 'C:/Users/winhl/Downloads/kongtiao/tmp/pd_cpysgjk_wd_80w_' #概率密度图文件名前缀
for i in range(k):
  density_plot(data[r[u'聚类类别']==i]).savefig(u'%s%s.png' %(pic_output, i))