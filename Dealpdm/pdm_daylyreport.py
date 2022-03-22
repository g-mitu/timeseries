import os
import pandas as pd
from xml.sax import ContentHandler, parse 
# Reference https://goo.gl/KaOBG3
class ExcelHandler(ContentHandler):
    def __init__(self):
      self.chars = [  ]
      self.cells = [  ]
      self.rows = [  ]
      self.tables = [  ]
    def characters(self, content):
        self.chars.append(content)
    def startElement(self, name, atts):
        if name=="Cell":
            self.chars = [  ]
        elif name=="Row":
            self.cells=[  ]
        elif name=="Table":
            self.rows = [  ]
    def endElement(self, name):
        if name=="Cell":
            self.cells.append(''.join(self.chars))
        elif name=="Row":
            self.rows.append(self.cells)
        elif name=="Table":
            self.tables.append(self.rows)

# excelHandler = ExcelHandler()
# parse('C:/Users/winhl/Downloads/杭州07外在质量检测日报表.xls', excelHandler)#文件名
# df1 = pd.DataFrame(excelHandler.tables[0][4:len(excelHandler.rows)-6])


data_res = None   #定义一个列表，用来存放读取的文件
#wpath="C:/Users/winhl/Downloads/test_file"
wpath="C:/Users/hcf/Downloads/test_file"
path_list=os.listdir(wpath)
#path_list.sort() #对读取的路径进行排序
for filename in path_list:
    if(filename[-3:]=='xls'): 
        file=os.path.join(wpath,filename)
        excelHandler = ExcelHandler()
        parse(file, excelHandler)#文件名
        df1 = pd.DataFrame(excelHandler.tables[0][4:len(excelHandler.rows)-6])
        data_res = pd.concat([data_res,df1],axis=0,ignore_index=True)

col_split=pd.DataFrame((x.split('/') for x in data_res[0]),index=data_res.index,columns=['name0','m'])
#
df = pd.merge(data_res,col_split,right_index=True,left_index=True)
#
#df = pd.merge(df,(df['m'].str.split(';',expand = True)),how = 'left',left_index = True,right_index = True)
df[['m1','m2','m3','m4','m5']] = df['m'].str.split(';',expand = True)
df.loc[:,'name0'].value_counts() #这一列统计频次

data0=pd.concat([df['name0'], df[33]], axis = 1) 
data1=None
for m in ('m1','m2','m3','m4','m5'):
    temp = pd.concat([df[m], df[33]], axis = 1,ignore_index=True)
    data1 =pd.concat([data1,temp],axis =0)

outputfile = os.path.join(wpath,'output.xlsx') #保存结果的文件名
data_res.to_excel(outputfile)
p0file = os.path.join(wpath,'p0.xlsx') #保存结果的文件名
data0.to_excel(p0file)
p1file = os.path.join(wpath,'p1.xlsx') #保存结果的文件名
(data1.sort_index()).to_excel(p1file)
##########################NULL
#import statistics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline# Reading in the data

train.isnull().sum()
data0[0].value_counts()##paihao
data1[0].value_counts()#jitai
data0[0].value_counts(normalize=True)

def extend_plot(data): #自定义作图函数
  import matplotlib.pyplot as plt
  plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
  plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
  plt.rcParams['figure.figsize'] = (8.0,8.0) #用来正常显示负号
  plt.rcParams['image.interpolation']='nearest' #set style
  plt.rcParams['savefig.dpi'] = 300 #图片像素
  plt.rcParams['figure.dpi'] = 300 #分辨率
  p = data.plot(kind='kde', linewidth = 2, subplots = True, sharex = False)

  plt.legend()
  plt.tight_layout()
  return plt

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import font_manager


# 使用数据透视表
score_pivot = data0.pivot_table(data0, values='Price', index='Region', aggfunc='count').reset_index().sort_values(ascending=False,by='Price')
f, ax = plt.subplots(figsize=(12,6))
# 画柱形图
bar = plt.bar(region_pivot['Region'].values,region_pivot['Price'].values, color='dodgerblue')
bar[0].set_color('green')
# 给条形图添加数据标注
for x, y in enumerate(region_pivot['Price'].values):
    plt.text(x-0.4, y+500, "%s" %y)
#删除所有边框
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
# ax.set(title='重庆各区域二手房总价', xlabel='地区', ylabel='总价')
plt.tick_params(labelsize=14)
plt.xlabel('地区', font1)
plt.ylabel('总价', font1)
plt.title('重庆各区域二手房总价', font1)
f.savefig('1_1.png', bbox_inches='tight')


my_font = font_manager.FontProperties(fname="C:\Windows\Fonts\simfang.ttf")
dp0 = data0[pd.notnull(data0["name0"])].groupby(by="name0").count().iloc[:,0]
plt.figure(figsize=(20,8),dpi=300)
_x = dp0.index
_y = dp0.values
plt.bar(list(range(len(_x))),_y,color="green")
plt.xticks(list(range(len(_x)))[::10],_x[::10].astype(int),rotation=45)
plt.xlabel("牌号",fontproperties=my_font)
plt.ylabel("抽样数量",fontproperties=my_font)
plt.title("不同牌号的数量（样本：）",fontproperties=my_font)
plt.show()



pic_output = 'C:/Users/winhl/Downloads/test_file/pd_' #概率密度图文件名前缀
  density_plot(data0[u'name0']).savefig(u'%s%s.png' %(pic_output, 0))

data0['name0'].hist(bins=50)
plt.show()