#生产模拟数据，我们先模拟一个一亿行的数据
import csv
import pandas as pd
import numpy as np


date= ['2019-11-01', '2019-11-02','2019-11-03','2019-11-04','2019-11-05','2019-11-06','2019-11-07']#设置日期数据，为后面的np.random.choice引用
area= ['河北', '山东', '湖南','河南','江苏','浙江','上海']
order_type =[0, 1, 2, 3, 4 ,5 ,6 ,7 ,8, 9]

col1=np.random.choice(date, 1000000, p=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.1])#随机抽样100万次，各个日常出现的概率是P。
col2=np.random.choice(area, 1000000, p=[0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1])
col3=np.random.choice(order_type, 1000000, p=[0.05, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05])
col4=np.random.choice(100, 1000000)
col5=np.random.choice(10000, 1000000)

df = pd.DataFrame({'date':col1, 'area':col2, 'order_type':col3, 'qty':col4, 'revenue':col5}) #合并各个numpy生产的随机数据成为Pandas的DataFrame
df=df.set_index('date')
with open('C:/Users/winhl/sample_data.csv','w', newline='\n') as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerow(['date','area','order_type','qty','revenue']) #先写入columns_name

for i in range(100):#为了减少内存占用，没有直接在上面生成1亿行数据，先生产100万，然后循环100次。
    i=i+1
    df.to_csv ('C:/Users/winhl/sample_data.csv', encoding='gbk', header=False, mode='a')
    print(i*1000000)

