# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 09:01:38 2018
@author: FanXiaoLei
"""
import pandas as pd

 
df=pd.read_json('C:/Users/10.154.190.152/Desktop/新建文本文档 (2).txt',orient='split')
df.to_excel('pandas处理json.xlsx',index=False)
