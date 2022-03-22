# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:16:25 2020

@author: winhl
modify 2022-1-6
"""

import pandas as pd
import json

work_dir = "D:/__E__/支部/积分"
#n0 = "2021s1p9"
n0 = "2021.01-12.xuexi.cn" #2022-1-6

with open(f"{work_dir}/{n0}.json", "r", encoding="utf-8") as f:
    fr = f.read()
    j1 = json.loads(fr)
    l_str = j1.get("data_str")
    j2 = json.loads(l_str)
    dict_str = j2.get("dataList")["data"]
    print(type(dict_str))
    # df = pd.read_json(dict_str, orient="records")
    df = pd.DataFrame(data=dict_str)
    print(df)
    df.to_csv(f"{work_dir}/{n0}.csv")


"""
from pandas import json_normalize
import json
data=open("F:/支部/XXQG/202009third_20200930.json",encoding="utf-8").read()
user_dic = json.loads(data)
data_list = user_dic["data"]["list"]
df = json_normalize(data_list)
print(df)
df.to_csv("09.csv")
"""
