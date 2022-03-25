import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import *
from pandas.plotting import scatter_matrix

# def Scatter plot matrix画图：矩阵图:
def matrixplot(df1):
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
    #sample: df = DataFrame(randn(1000, 4), columns=['a', 'b', 'c', 'd'])
    df = df1.drop(columns=["Date","状态"])
    pd.plotting.scatter_matrix(df, figsize=(12, 8))
    #scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.show()

# def 时间对齐：
def align(a,df_temp,x,cname,dfname):
    res_t = pd.DataFrame()
    for i in range(0, x):
        j = df_temp.iloc[:, [2 * i, 2 * i + 1]]
        k = pd.merge(a, j, left_on=a.iloc[:, 0], right_on=j.iloc[:, 0], how="left")
        res_t = pd.concat([res_t, k], ignore_index=True, axis=1)
        print(res_t.head())
    print(res_t.info())
    # def 去掉重复的时间列:
    x = list(range(3, res_t.shape[1] + 1, 4))
    # 增加第一个时间列序号
    x.insert(0, 0)
    df = res_t.iloc[:, x]
    df.columns = cname
    # 输出到xlsx文件
    df.to_excel(f"{workdir}/baseline_"+dfname+"_ok.xlsx")
    return df
    
    
# def 分割,时间resample：
def resampletime(df1):
    # 以datetime形式将字符串拆分为日期和时间
    date2 = pd.to_datetime(df1["Date"], errors="coerce")  # 方便人查看
    df7 = df1.copy()  
    df6 = df7.drop[["状态"]]
    df6['Hour'] = date2.dt.hour  #按照时间分类
    df5 = df6.set_index("Date", drop=False) #时间索引，同时保留
    df4 = df5.sort_index(ascending=True)
    print("Line 40#", df4.head())
    a = df4.tail(1)                                #保留最后一行，pd.concat([df.head(1), df.tail(1)])
    t = df4.resample('H', on='Date').min() #按小时重新采样，取最左边一个（小）值,.max.sum()return NEW dataframe
    df3 = pd.concat([t, a])                        #最后一行补上
    df2 = df3.diff()
    df = df2.fillna(0)  #
    return df
    
    
# def 停机时间：
def stopT(df):
    # 以datetime形式将字符串拆分为日期和时间
    date2 = pd.to_datetime(df["Date"], errors="coerce")  # 方便人查看
    # ERROR: A value is trying to be set on a copy of a slice from a DataFrame. Try using .loc[row_indexer,col_indexer] = value instead
    df = df.copy()  
    df["Date2"] = date2.dt.date  # 方便人查看
    df["Time"] = date2.dt.time  # 方便人查看
    df["stime"] = date2.apply(lambda t: t.value // 10 ** 9)  # 转化为unix时间戳最小单位是秒s
    
    df.set_index("Date", inplace=True)
    df = df.sort_index(ascending=True)
    print("Line 40#", df.head())
    # returning dataframe with salary between above values
    df["bool_stop"] = df["车速"].between(0, 1000 / 3, inclusive="both")
    df1 = df.loc[df["bool_stop"] == False]  # 这里的False一定不能用引号
    df2 = df1["stime"]
    print(type(df2))  # class 'pandas.core.series.Series'
    df2 = df2.diff()
    df2 = df2.fillna(0)  #
    return df2
    
    
    
# def 换班，默认按天分析：
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
    
    
    
# def 停机统计：
def stopPlot(df2,str):
    # between_time() got an unexpected keyword argument 'inclusive'
    print("Line 70#", df2.head())
    # df2 = df2[df2>2]
    print("L72#", df2[df2 > 2].value_counts())
    df2.to_csv(f"{workdir}/"+str+".csv")
    
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
    plt.subplot(211)
    #每天第一个数据进行消除
    df2[df2 >= 6*3600] = 2
    df2.plot(x_compat=True) #X轴为时间时的良好展示
    # plt.show()
    plt.subplot(212)
    df2[(df2 > 2)].value_counts().sort_index().plot(kind="bar")
    plt.show()
    
    
# def LDS统计、画图：
def ldsPlot(df,str):
    df = df.copy()  
    df.set_index("Date", inplace=True)
    df = df.sort_index(ascending=True)
    df2 = df["LDS空头"]
    print(type(df2))  # class 'pandas.core.series.Series'
    df2 = df2.diff()
    df2 = df2.fillna(0)  #
    print("L72#", df2.value_counts())
    df2.to_csv(f"{workdir}/"+str+"_lds.csv")
    
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
    plt.subplot(211)
    #每天第一个数据进行消除，换班会产生负值，班中有异常重置为0的数据
    df2[df2 <= -110] = 0
    df2.plot(x_compat=True) #X轴为时间时的良好展示
    # plt.show()
    plt.subplot(212)
    #消除负值及0值，仅统计大于0的剔除数
    df2[(df2 > 0)].value_counts().sort_index().plot(kind="bar")

    plt.show()
    
    
# def LDS剔除对比画图，x轴为2s-index：
def sameY(df1,df2):
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
# concat axis=1合并为1个df，可以通过'x_compat'直接绘制2条线
#    with pd.plotting.plot_params.use('x_compat', True): #方法一
#        df['A01'].plot(color="b", style=".-", legend=True)
#        df['A02'].plot(color="r", style="-", legend=True)
    df_f1 = df1["LDS空头"]
    df_f2 = df2["LDS空头"]
    df_f1.plot(color="b", style=".-", legend=True, label='A01-LDS空头')
    df_f2.plot(color="r", style="-", legend=True, label='A02-LDS空头')
    plt.title("A01 vs A02 LDS空头对比")
    plt.xlabel("2s-index-Date")
    plt.ylabel("PackageValue")
    plt.show()

#def 状态图，把一张DataFrame5列（子图）画在一张图：
def subplotXY(df,sty="-",pt=None):
#SyntaxError: non-default argument follows default argument
#    df1 = df.drop(columns=['状态'])
#    df1 = df1.set_index('Date') #result:set_index方法默认将创建一个新的 DataFrame
    df1 = df.drop(columns=["Date","状态"])
    df1.plot(subplots=True, figsize=(6, 6),style=sty); #根据传参设置形状
    plt.legend(loc='best')
    plt.title(pt) #result：通过pt传参设置标题
    plt.xlabel("2s-index-Date")
    plt.ylabel("Value")
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

#----------------BEGIN
program_begin = time()
workdir = r"D:\vs_projects\datas"
# 读入HDF5数据：
data_store = pd.HDFStore('processed_data.h5')
df_a01_1418 = data_store['df_a01_1418']
df_a02_1418 = data_store['df_a02_1418']
data_store.close()
#调用stopT
df2 = stopT(df_a01_1418)   #return 单一停机时间差

program_finish = time()
print("用时：", program_finish - program_begin)
#----------------画图区
#调用停机时间画图stopPlot     #return plot折线和柱形
stopPlot(df2,"a01")

#调用ldsPlot
ldsPlot(df_a01_1418,"a01")

#调用对比图
sameY(df_a01_1418,df_a02_1418)

#调用状态图
subplotXY(df_a01_1418,".")
#---------------------
#单独分析A02
#数据，天、班
df3 = shiftsplit(df_a02_1418,None,"2022-03-18")
#5联图
subplotXY(df3,".","A02状态")
#矩阵图
#matrixplot(df_a02_1418)
#关联图，点图
relationplot(df_a02_1418)
