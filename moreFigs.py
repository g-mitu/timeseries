import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(
    np.random.randn(1000, 4),
    index=pd.date_range("3/1/2022", periods=1000),
    columns=list("ABCD"),
)
df = df.cumsum()
with pd.plotting.plot_params.use("x_compat", True):  # 方法一
    df.A.plot(color="r")
    df.B.plot(color="g")
    df.C.plot(color="b")
plt.show()


df = pd.DataFrame(np.random.rand(50, 4), columns=["a", "b", "c", "d"])
ax = df.plot.scatter(x="a", y="b", color="DarkBlue", label="Group 1")
df.plot.scatter(x="c", y="d", color="Red", label="Group 2", ax=ax, s=100)
# 方法二ax，s控制点的大小
plt.show()
