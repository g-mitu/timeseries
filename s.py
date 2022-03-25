import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import *
from pandas.plotting import scatter_matrix

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


# def 分割,时间resample：
def resampletime(df1):
    # 以datetime形式将字符串拆分为日期和时间
    date2 = pd.to_datetime(df1["Date"], errors="coerce")  # 方便人查看
    df6 = df1.copy()  
    df6['Hour'] = date2.dt.hour  #按照时间分类
    df5 = df6.set_index("Date", drop=False) #时间索引，同时保留
    df4 = df5.sort_index(ascending=True)
    print("Line 20#", df4.head())
    a = df4.tail(1)                                #保留最后一行，pd.concat([df.head(1), df.tail(1)])
    t = df4.resample('H', on='Date').min() #按小时重新采样，取最左边一个（小）值,.max.sum()return NEW dataframe
    df4 = pd.concat([t, a])                        #最后一行补上
    df4 = df4.drop(columns=["Date","状态"])
    print(df4.head())
    df2 = df4.diff()
    df = df2.fillna(0)  #
    return df

# def 换班：
def shiftsplit(df1,str,str1):
    # making a bool series
    start_time = datetime.datetime.strptime("6:50:00", "%H:%M:%S").time()
    end_time = datetime.datetime.strptime("15:29:59", "%H:%M:%S").time()
    start_time2 = datetime.datetime.strptime("15:30:00", "%H:%M:%S").time()
    end_time2 = datetime.datetime.strptime("23:59:59", "%H:%M:%S").time()
    df = df1.set_index("Date", drop=False)
    locs_morning = df.index.indexer_between_time(start_time, end_time)  # 返回的是符合条件的数据的行号
    locs_afternoon = df.index.indexer_between_time(start_time2, end_time2)  # 返回的是符合条件的数据的行号
    # df1 = df.iloc[locs_morning]  # 早班
    if str == "morning":
        df1 = df.iloc[locs_morning]  
    elif str == "afternoon":
        df1 = df.iloc[locs_afternoon]
    else:
        df1 = df # 默认：全天
    #df1 = df1.loc["2022-02-18"]
    df1 = df1.loc[str1]
    return  df1

def subplotXY(df,diff,sty="-",pt=None):
#    df1 = df.drop(columns=['状态'])
#    df1 = df1.set_index('Date') #result:set_index方法默认将创建一个新的 DataFrame
    if diff:
        df1 = df.copy()
    else:
        df1 = df.drop(columns=["Date","状态"])
    df1.plot(subplots=True, figsize=(6, 6),style=sty); #根据传参设置形状
    plt.legend(loc='best')
    plt.title(pt) #result：通过pt传参设置标题
    plt.xlabel("2s-index-Date")
    plt.ylabel("Value")
    plt.show()


# def Scatter plot matrix画图：矩阵图:
def matrixplot(df1):
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
    #sample: df = DataFrame(randn(1000, 4), columns=['a', 'b', 'c', 'd'])
    df = df1.drop(columns=["Date","状态"])
    pd.plotting.scatter_matrix(df, figsize=(12, 8))
    #scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.show()
    
#def 散点图，相关关系：(Y=LDS，x1=停机次数，x2=车速，x3=剔除)
def relationplot(df):
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
#数据已经cumsum()
    df1 = df[["车速","LDS空头"]]
    df1.plot(x='车速', y='LDS空头')
    df1.plot.scatter(x="车速", y="LDS空头")
#    df1 = df[["车速","停次","LDS空头"]]
#    ax = df1.plot.scatter(x="车速", y="LDS空头", color="DarkBlue", label="Group 1")
#    df.plot.scatter(x="c", y="d", color="DarkGreen", label="Group 2", ax=ax);
#
    plt.legend(loc='best')
    plt.title("相关性") #result：通过pt传参设置标题
    plt.xlabel("2s-index-Date")
    plt.ylabel("Value")
    plt.show()
    
data_store = pd.HDFStore('processed_data.h5')
#df_a01_1418 = data_store['df_a01_1418']
df_a02_1418 = data_store['df_a02_1418']
data_store.close()
#调用对比图
#单独分析A02
#df3 = shiftsplit(df_a02_1418,None,"2022-03-18")
df3 = shiftsplit(df_a02_1418,"afternoon","2022-03-18")
subplotXY(df3,False,".","A02状态")
#matrixplot(df_a02_1418)
#relationplot(df_a02_1418)
df4 = resampletime(df3)
subplotXY(df4,True,"-","A02状态")
