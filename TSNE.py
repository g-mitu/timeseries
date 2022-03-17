# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 21:00:23 2019

@author: winhl
"""


# 使用TSNE进行数据降维并展示聚类结果
from sklearn.manifold import TSNE
tsne = TSNE()
tsne.fit_transform(data_zs)  # 进行数据降维
# tsne.embedding_可以获得降维后的数据
print('tsne.embedding_: \n', tsne.embedding_)
tsn = pd.DataFrame(tsne.embedding_, index=data.index)  # 转换数据格式
print('tsne: \n', tsne)

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 不同类别用不同颜色和样式绘图
color_style = ['r.', 'go', 'b*']
for i in range(k):
    d = tsn[output_data[u'聚类类别'] == i]
    # dataframe格式的数据经过切片之后可以通过d[i]来得到第i列数据
    plt.plot(d[0], d[1], color_style[i], label='聚类' + str(i+1))
plt.legend()
plt.show()
