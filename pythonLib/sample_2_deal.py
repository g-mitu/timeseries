#4. 数据分析代码.涉及的功能：读取数据，增加计算字段，group by ，merge( left join)， index (set & reset)， 输出数据（CSV & excel）。

import pandas as pd
import time
import csv
start = time.perf_counter() #开始计时time.clock has been deprecated in Python 3.3 and will be removed from Python 3.8: use time.perf_counter or time.process_time instead
with open('C:/Users/winhl/pd_sum.csv','w',encoding='gbk', newline='\n') as csvfile: #为汇总的输出，建立一个CSV文件，并包含表头字段明。
    writer = csv.writer(csvfile)
    writer.writerow(['date','area','order_type','qty','revenue'])     #先写入columns_name
    
reader = pd.read_csv('C:/Users/winhl/sample_data.csv', encoding='gbk',sep=',',iterator=True) #分块（每100万行）进行数据汇总, 并循环写入csv中    
i=0 
while True:
    try:
        start2 = time.perf_counter()#每次循环开始时间          # 计时  
        df = reader.get_chunk(1000000)# 从csv文件迭代读取        
        
        mini_sum=df.groupby(['date','area','order_type']).sum()        #按date, area, order_type 进行汇总
        mini_sum.to_csv('C:/Users/winhl/pd_sum.csv',mode='a',header=False)        #汇总结果写入CSV文件，'header=False' 避免重复写入表头。        

        i=i+1
        end2 = time.perf_counter()        #每次循环结束时间
        print('{} 秒: completed {} rows'.format(end2 - start2, i * 1000000))
    except StopIteration:
        print("Iteration is successfully stopped.")        #循环结束退出        
        break

df=pd.read_csv('C:/Users/winhl/pd_sum.csv', encoding='gbk',sep=',')
df=df.groupby(['date','area','order_type']).sum()
df=df.reset_index()  					#pandas汇总时，会根据groupby的字段建立multi_index, 需要重置index。
df['date']=pd.to_datetime(df['date']) 	#将date列 设置为日期类型
df['avg']=df['revenue']/df['qty']		#增加一个计算字段 avg 平均客单价
df_sub=df[['date','area','qty']].groupby(['date','area']).sum().add_prefix('sum_')		#建立一个新DataFrame, 用于后面的left join 计算各个order_type的占比
df_merge=pd.merge(df, df_sub, how='outer', left_on=['date','area'], right_index=True)	#相当于SQL的left join
df_merge['type_qty%']=df_merge['qty']/df_merge['sum_qty']								#增加计算字段
df_merge=df_merge.set_index('date')
output=pd.ExcelWriter('C:/Users/winhl/output_xls.xlsx')
df_merge.to_excel(output,'sheet1',encoding='gbk')
output.save()							#最终结果输出到excel
end = time.perf_counter()						#最终使用时间计时
print('final:{} 秒'.format(end - start))

#################
#笔记本电脑循环每次计算100万行用时 0.83， 总用时85.1秒。
#Thinkpad E450 SSD硬盘 i5 8G内存的笔记本电脑。
#运行时，CUP占用率笔记本30%， 总内存占用约6GB
################################################################
#0.817601222058812 秒: completed 92000000 rows
#0.8092709856398557 秒: completed 93000000 rows
#0.8277913177203118 秒: completed 94000000 rows
#0.8203788228361191 秒: completed 95000000 rows
#0.8211909342874009 秒: completed 96000000 rows
#0.8238487924599838 秒: completed 97000000 rows
#0.825806156394961 秒: completed 98000000 rows
#0.8143844225134984 秒: completed 99000000 rows
#0.8465947555305036 秒: completed 100000000 rows
#Iteration is stopped.
#final85.11640178604648 秒
################################################################
#
#原文链接：https://blog.csdn.net/jambone/article/details/78769421