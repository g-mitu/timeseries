# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:16:25 2020

@author: winhl
"""
# n0 = "F:/支部/XXQG/p202009_d20200930.json"
import pandas as pd
import json
n0 = "D:/__E__/支部/积分/2020年1-6月学习强国积分.json"
n1 = "D:/__E__/支部/积分/2020年1-6月学习强国积分.csv"
with open(n0, "r", encoding="utf-8") as f:
    fr = f.read()     #string
    data_j = json.loads(fr) #dict
    temp = data_j.get("data_str") #string, 没有key: value形式，故为string
    data_list = json.loads(temp) #dict
    print(type(data_list))
    temp = data_list.get("dataList")#dict

    detail_info= data_list.get("dataList").get('data') #list
    json_data = json.dumps(detail_info)
    df = pd.read_json(json_data, orient="records")
    print(df)
    df.to_csv(n1)
