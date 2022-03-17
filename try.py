import itertools
import pandas as pd

df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "a", "b"], "data1": range(7)})
print(df1)
df2 = pd.DataFrame({"key": ["a", "b", "d"], "data2": range(3)})
print(df2)
a = pd.merge(df1, df2)
print(a)
b = pd.concat([df1, df2])
print(b)
left = pd.DataFrame({"key1": ["fool", "bar"], "lval": [1, 2]})
right = pd.DataFrame({"key2": ["fool", "bar"], "rval": [4, 5]})
c = pd.merge(left, right, left_on="key1", right_on="key2")
print(c)

df_mask = pd.DataFrame(
    {"AAA": [True] * 4, "BBB": [False] * 4, "CCC": [True, False] * 2}
)  # 这种生成df的方式很新颖


def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    print(type(rows))
    print(data_dict.keys())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())


df = expand_grid(
    {"height": [60, 70], "weight": [100, 140, 180], "sex": ["Male", "Female"]}
)
print(df)

