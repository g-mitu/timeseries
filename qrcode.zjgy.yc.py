# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:16:25 2020

@author: winhl
"""
# vs_projects/datas/qrcode.zjgy.yc
import pandas as pd
import json
n0 = "D:/vs_projects/datas/qrcode.zjgy.yc.json"
n1 = "D:/vs_projects/datas/qrcode.zjgy.yc.csv"
with open(n0, "r", encoding="utf-8") as f:
    fr = f.read()     #string, 取值需要运行一次, load()
    data_j = json.loads(fr) #dict——key: value
    temp = data_j.get("data") #dict——key: value
    temp = data_j.get("data").get("content") #list
    print(type(temp))


    json_data = json.dumps(temp) #取出list中的内容需要运行这行
    df = pd.read_json(json_data, orient="records")
    print(df)
    df.to_csv(n1)
