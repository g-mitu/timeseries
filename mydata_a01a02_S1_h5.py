import pandas as pd
from time import *


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
    
    
#----------------BEGIN
program_begin = time()
workdir = r"D:\vs_projects\datas"
# def 需要的间隔2s时间序列
a14 = pd.DataFrame(pd.date_range("2022-3-14 6:40:02", "2022-3-14 23:59:58", freq="2S"))
a15 = pd.DataFrame(pd.date_range("2022-3-15 6:40:02", "2022-3-15 23:59:58", freq="2S"))
a16 = pd.DataFrame(pd.date_range("2022-3-16 6:40:02", "2022-3-16 23:59:58", freq="2S"))
a17 = pd.DataFrame(pd.date_range("2022-3-17 6:40:02", "2022-3-17 23:59:58", freq="2S"))
a18 = pd.DataFrame(pd.date_range("2022-3-18 6:40:02", "2022-3-18 23:59:58", freq="2S"))
a= pd.concat([a14,a15,a16,a17,a18])

df_a01_1415 = pd.read_excel(f"{workdir}/a01-1415.xlsx", index_col=None)
df_a01_1617 = pd.read_excel(f"{workdir}/a01-1617.xlsx", index_col=None)
df_a01_18   = pd.read_excel(f"{workdir}/a01-18.xlsx", index_col=None)
df_a02_1415 = pd.read_excel(f"{workdir}/a02-1415.xlsx", index_col=None)
df_a02_1617 = pd.read_excel(f"{workdir}/a02-1617.xlsx", index_col=None)
df_a02_18   = pd.read_excel(f"{workdir}/a02-18.xlsx", index_col=None)
df_a01 = pd.concat([df_a01_1415,df_a01_1617,df_a01_18], ignore_index=True, axis=0)
df_a02 = pd.concat([df_a02_1415,df_a02_1617,df_a02_18], ignore_index=True, axis=0)

##调用函数align()
cname = ["Date","车速","产量","剔除","停次","LDS空头","状态"]
df_a01_1418 = align(a,df_a01,6,cname,"a01")
df_a02_1418 = align(a,df_a02,6,cname,"a02")
# show sth
print("L51#", df_a02_1418.head())
#临时存储为hdf5
data_store = pd.HDFStore('processed_data.h5')
#key->df_a01_1418,存放数据表
data_store['df_a01_1418'] = df_a01_1418
data_store['df_a02_1418'] = df_a02_1418
data_store.close()

# 读取HDF5数据表
# data_store = pd.HDFStore('processed_data.h5')
# df_a01_1418 = data_store['df_a01_1418']
# df_a02_1418 = data_store['df_a02_1418']
# data_store.close()
#----------------END
program_finish = time()
print("用时：", program_finish - program_begin) #用时： 117.95483446121216
