import pandas as pd

"""
根据某一列合并其他多列为一行
"""
df = pd.DataFrame(
    {
        "id_part": ["a", "b", "c", "d", "e"],
        "pred": [0.1, 0.2, 0.3, 0.4, 0.8],
        "pred_class": ["women", "man", "cat", "dog", "man"],
        "v_id": ["d1", "d2", "d3", "d1", "d3"],
    }
)

o = (
    df.groupby(["v_id"])
    .agg({"pred_class": [", ".join], "pred": lambda x: list(x), "id_part": "first"})
    .reset_index()
)
"""
分组、组内排序
"""
df = pd.DataFrame(
    [["A", 1], ["A", 3], ["A", 2], ["B", 5], ["B", 9]], columns=["name", "score"]
)
print(df)
o1 = df.sort_values(["name", "score"], ascending=[True, False])
o2 = (
    df.groupby("name")
    .apply(lambda x: x.sort_values("score", ascending=False))
    .reset_index(drop=True)
)
print(o1, o2)
"""
把 Series 里的[]列表转换为 DataFrame
"""
df = pd.DataFrame({"列1": ["a", "b", "c"], "列2": [[10, 20], [20, 30], [30, 40]]})
print(df)
df_new = df.列2.apply(pd.Series)
o = pd.concat([df, df_new], axis="columns")
print(o)

