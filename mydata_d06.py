import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import *

# from pandas.plotting import scatter_matrix

# program_begin = time()
# def 需要的间隔2s时间序列
a = pd.DataFrame(pd.date_range("2022-2-14 6:45:02", "2022-2-14 15:30:00", freq="2S"))

workdir = r"D:\vs_projects\datas"
df_temp = pd.read_excel(f"{workdir}/d06主机数据.xlsx", index_col=None)

# def 时间对齐：
res_t = pd.DataFrame()
for i in range(0, 21):
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

# 定义各列的标题名
# ------------------------------------------------------------
df.columns = ["Date",'速度','利用率','运行时间','主机停机次','产量','剔除','3轮剔除','6轮剔除','8轮剔除','空头剔除','生产时间','理论产量','损失产量','辅机车速','辅机产量','辅机剔除','CH好烟','CH坏烟','CH手剔','辅机利用率','辅机停机次']
# ------------------------------------------------------------
print("L35#", df.head())
# 输出到xlsx文件
df.to_excel(f"{workdir}/baseline_d06_ok.xlsx")

#画图演示
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
'''
# 画图：矩阵图
pd.plotting.scatter_matrix(df, figsize=(12, 8))
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
plt.show()
# 画图：一图双线
df_f1 = df["辅机产量"]
df_f2 = df["CT好烟"]
# 可以通过DataFrame的plot()方法直接绘制 # color指定线条的颜色 # style指定线条的样式 # legend指定是否使用标识区分
df_f1.plot(x=df["Date"], color="b", style=".-", legend=True)
df_f2.plot(x=df["Date"], color="r", style="-", legend=True)
plt.title("辅机产量 VS CT好烟")
plt.xlabel("Date")
plt.ylabel("Value")
plt.show()

# 画图2：一图双线
df_f1 = df["辅机剔除"]
df_f2 = df["CT剔除"]
# 可以通过DataFrame的plot()方法直接绘制 # color指定线条的颜色 # style指定线条的样式 # legend指定是否使用标识区分
df_f1.plot(color="b", style=".-", legend=True)
df_f2.plot(color="r", style="-", legend=True)
plt.title("辅机剔除 VS CT剔除")
plt.xlabel("Date")
plt.ylabel("Value")
plt.show()
'''
# 画图2：一图双线
df_f1 = df["产量"]
df_f2 = df["辅机产量"]
# 可以通过DataFrame的plot()方法直接绘制 # color指定线条的颜色 # style指定线条的样式 # legend指定是否使用标识区分
df_f1.plot(x=df["Date"], color="b", style=".-", legend=True)
df_f2.plot(x=df["Date"], color="r", style="-", legend=True)
plt.title("主机产量 VS CT好烟")
plt.xlabel("Date")
plt.ylabel("Value")
plt.show()

# 画图3：剔线
df_f1 = df[["Date","剔除"]]
#df_f2 = df['3轮剔除']
#df_f3 = df['6轮剔除']
#df_f4 = df['8轮剔除']
#df_f5 = df['空头剔除']
# 可以通过DataFrame的plot()方法直接绘制 # color指定线条的颜色 # style指定线条的样式 # legend指定是否使用标识区分
df_f1.plot(x="Date", color="b", style=".-", legend=True)
#df_f2.plot( color="g", style=".", legend=True)
#df_f3.plot( color="r", style="-", legend=True)
#df_f4.plot( color="c", style="o", legend=True)
#df_f5.plot( color="m", style="D", legend=True)
#(df_f2+df_f3+df_f4).plot( color="y", style="x", legend=True)
plt.title("主机剔除")
plt.xlabel("Date")
plt.ylabel("Value")
plt.show()
'''
df.plot(subplots=True, figsize=(6, 6));
df.plot(subplots=True, layout=(2, 3), figsize=(6, 6), sharex=False);

'''
'''
# 以datetime形式将字符串拆分为日期和时间
date2 = pd.to_datetime(df["Date"], errors="coerce")  # 方便人查看
df = (
    df.copy()
)  # A value is trying to be set on a copy of a slice from a DataFrame. Try using .loc[row_indexer,col_indexer] = value instead
df["Date2"] = date2.dt.date  # 方便人查看
df["Time"] = date2.dt.time  # 方便人查看
df["stime"] = date2.apply(lambda t: t.value // 10 ** 9)  # 转化为unix时间戳最小单位是秒s

df.set_index("Date", inplace=True)
df = df.sort_index(ascending=True)
print("Line 40#", df.head())

df["bool_stop"] = df["车速"].between(0, 500 / 3, inclusive="both")
# returning dataframe with salary between above values

# making a bool series
start_time = datetime.datetime.strptime("6:50:00", "%H:%M:%S").time()
end_time = datetime.datetime.strptime("15:29:59", "%H:%M:%S").time()
start_time2 = datetime.datetime.strptime("15:30:00", "%H:%M:%S").time()
end_time2 = datetime.datetime.strptime("23:59:59", "%H:%M:%S").time()
locs_morning = df.index.indexer_between_time(start_time, end_time)  # 返回的是符合条件的数据的行号
locs_afternoon = df.index.indexer_between_time(start_time2, end_time2)  # 返回的是符合条件的数据的行号

# df1 = df.iloc[locs_morning]  # 早班
df1 = df.iloc[locs_afternoon]  # 中班
df1 = df1.loc["2022-02-18"]
df1.to_excel(f"{workdir}/baseline.xlsx")

df1 = df1.loc[df1["bool_stop"] == False]  # 这里的False一定不能用引号
df2 = df1["stime"]
print(type(df2))  # class 'pandas.core.series.Series'
df2 = df2.diff()
df2 = df2.fillna(0)  #
"""
ser_diff = df3.index.to_series().diff()
df3["ser_diff"] = ser_diff.dt.seconds.div(60, fill_value=0)
# df3["总秒数"] = df3.index.to_series().diff().dt.total_seconds()
"""

# between_time() got an unexpected keyword argument 'inclusive'
print("Line 70#", df2.head())
# df2 = df2[df2>2]
print("L72#", df2[df2 > 2].value_counts())
df2.to_csv(f"{workdir}/b08.csv")

program_finish = time()
print("用时：", program_finish - program_begin)
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
plt.subplot(211)
df2.plot(x_compat=True) #X轴为时间时的良好展示
# plt.show()
plt.subplot(212)
df2[df2 > 2].value_counts().sort_index().plot(kind="bar")
plt.show()
'''
'''
The following format string characters are accepted to control
the line style or marker:

================    ===============================
character           description
================    ===============================
``'-'``             solid line style
``'--'``            dashed line style
``'-.'``            dash-dot line style
``':'``             dotted line style
``'.'``             point marker
``','``             pixel marker
``'o'``             circle marker
``'v'``             triangle_down marker
``'^'``             triangle_up marker
``'<'``             triangle_left marker
``'>'``             triangle_right marker
``'1'``             tri_down marker
``'2'``             tri_up marker
``'3'``             tri_left marker
``'4'``             tri_right marker
``'s'``             square marker
``'p'``             pentagon marker
``'*'``             star marker
``'h'``             hexagon1 marker
``'H'``             hexagon2 marker
``'+'``             plus marker
``'x'``             x marker
``'D'``             diamond marker
``'d'``             thin_diamond marker
``'|'``             vline marker
``'_'``             hline marker
================    ===============================

The following color abbreviations are supported:

==========  ========
character   color
==========  ========
'b'         blue
'g'         green
'r'         red
'c'         cyan
'm'         magenta
'y'         yellow
'k'         black
'w'         white
==========  ========
'''