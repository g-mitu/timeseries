import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import *

program_begin = time()
# a=pd.DataFrame(pd.date_range("2022-2-14 0:0:02","2022-2-15 23:59:58",freq='2S'))
workdir = r"C:\Users\zyhly\Downloads\mydata"
df = pd.read_excel(f"{workdir}/a03_data.xlsx", index_col=None)
# 以datetime形式将字符串拆分为日期和时间
date2 = pd.to_datetime(df["Date"], errors="coerce")  # 方便人查看
df["Date2"] = date2.dt.date  # 方便人查看
df["Time"] = date2.dt.time  # 方便人查看
df["stime"] = date2.apply(lambda t: t.value // 10 ** 9)  # 转化为unix时间戳最小单位是秒s

df.set_index("Date", inplace=True)
df = df.sort_index(ascending=True)
print("Line 17#", df.head())

df["bool_stop"] = df["车速"].between(0, 1000 / 3, inclusive="both")
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
df1 = df1.loc["2022-02-14"]
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
print("Line 47#", df2.head())
# df2 = df2[df2>2]
print(df2[df2 > 2].value_counts())
df2.to_excel(f"{workdir}/01.xlsx")

program_finish = time()
print("用时：", program_finish - program_begin)
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
plt.subplot(211)
df2.plot()
# plt.show()
plt.subplot(212)
df2[df2 > 2].value_counts().sort_index().plot(kind="bar")
plt.show()
