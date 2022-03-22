import json

m=[]
with open('xxx.json', 'r',
          encoding='utf8')as fp:
    json_data = json.load(fp)
    n = json_data.get('cells')
    for i in range(0, len(n)):
        if n[i].get('cell_type') == 'code':
            # n[i].get('source') 返回[]形式的数组
            m.append("".join(n[i].get('source')))
    #    print("\r\n".join(str(i) for i in m))
print("".join(str(i) for i in m))
# print('这是文件中的json数据：', m)
# print('这是读取到文件数据的数据类型：', type(m))
py_code = "\r\n".join(str(i) for i in m)
with open("yyy.txt", "w", encoding='utf-8') as f:
    f.write(py_code)
