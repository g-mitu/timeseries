import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ts = pd.Series(
    np.random.randn(1000), index=pd.date_range("3/1/2022", periods=1000)
)  # 月/日/年
#     ts = ts.cumsum()
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))
df = df.cumsum()
print(df)
# 图1：其中A图用左Y轴标注，B图用右Y轴标注，二者共用一个X轴
df.A.plot()  # 对A列作图，同理可对行做图
df.B.plot(secondary_y=True, style="g")  # 设置第二个y轴（右y轴）
# 图2
ax = df.plot(
    secondary_y=["A", "B"]
)  # 定义column A B使用右Y轴。ax（axes）可以理解为子图，也可以理解成对黑板进行切分，每一个板块就是一个axes
#     ax = df.plot(secondary_y=['A', 'B'], mark_right=False)#上一行默认图列会显示（right）, mark_right=False即关闭显示
ax.set_ylabel("CD scale")
ax.right_ax.set_ylabel("AB scale")
ax.legend(loc="upper left")  # 设置图例的位置
ax.right_ax.legend(loc="upper right")
#     ax.legend(loc='1')
#     plt.legend(loc='2')zhem
# 展示
plt.show()
