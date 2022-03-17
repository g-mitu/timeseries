import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import *

program_begin = time()
a_0 = pd.DataFrame(pd.date_range("2022-2-14 6:40:02", "2022-2-15 23:59:58", freq="2S"))
a_1 = pd.DataFrame(pd.date_range("2022-2-16 6:40:02", "2022-2-17 23:59:58", freq="2S"))
a_2 = pd.DataFrame(pd.date_range("2022-2-18 6:40:02", "2022-2-18 23:59:58", freq="2S"))
a = pd.concat([a_0, a_1, a_2], ignore_index=True, names="t")
workdir = r"C:\Users\zyhly\Downloads\mydata"
df_temp = pd.read_excel(f"{workdir}/b08主机数据.xlsx", index_col=None)
p_0 = df_temp.iloc[:, [0, 1]]
p_1 = df_temp.iloc[:, [2, 3]]
p_2 = df_temp.iloc[:, [4, 5]]
p_3 = df_temp.iloc[:, [6, 7]]
p_4 = df_temp.iloc[:, [8, 9]]

res_t0 = pd.merge(a, p_0, left_on=a.iloc[:, 0], right_on=p_0.iloc[:, 0], how="left")
res_t1 = pd.merge(a, p_1, left_on=a.iloc[:, 0], right_on=p_1.iloc[:, 0], how="left")
res_t2 = pd.merge(a, p_2, left_on=a.iloc[:, 0], right_on=p_2.iloc[:, 0], how="left")
res_t3 = pd.merge(a, p_3, left_on=a.iloc[:, 0], right_on=p_3.iloc[:, 0], how="left")
res_t4 = pd.merge(a, p_4, left_on=a.iloc[:, 0], right_on=p_4.iloc[:, 0], how="left")

res_t = pd.concat([res_t0, res_t1, res_t2, res_t3, res_t4], axis=1)
df = res_t.iloc[:, [0, 3, 7, 11, 15, 19]]
print("L28#", df.info())
df.columns = ["Date", "车速", "产量", "剔除", "停机次", "停机秒"]
print("L30#", df.head())

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
df2.plot()
# plt.show()
plt.subplot(212)
df2[df2 > 2].value_counts().sort_index().plot(kind="bar")
plt.show()
