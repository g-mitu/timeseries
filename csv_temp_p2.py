# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 13:28:22 2019

@author: winhl
"""


data = data_sd
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
outputfile = 'C:/Users/winhl/Downloads/kongtiao/tmp/type_cpysgjk_sd_data.csv'
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

pic_output = 'C:/Users/winhl/Downloads/kongtiao/tmp/pd_cpysgjk_sd_100w_' #概率密度图文件名前缀
for i in range(k):
  density_plot(data[r[u'聚类类别']==i]).savefig(u'%s%s.png' %(pic_output, i))