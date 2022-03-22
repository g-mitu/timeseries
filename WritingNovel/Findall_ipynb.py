# 读取json文件内容,返回字典格式
import json
import os

root = 'C:/Users/zyhly/Downloads/handson-ml2-master/'
items = os.listdir(root)
for item in items:
    t = os.path.join(root, item)
    if os.path.isdir(t):
        for file in os.listdir(t):
            if os.path.splitext(file)[1] == '.ipynb':  # 分割文件名和文件扩展名，并且扩展名为'ipynb'
                file = os.path.join(t, file)  # 同样要加上路径
    elif os.path.isfile(t):                         # 如果是文件，则直接判断扩展名
        if os.path.splitext(t)[1] == '.ipynb':
            #
            new = os.path.splitext(item)[0]
            m = []
            with open(t, 'r', encoding='utf8')as fp:
                json_data = json.load(fp)
                n = json_data.get('cells')
                for i in range(0, len(n)):
                    if n[i].get('cell_type') == 'code':
                        m.append("".join(n[i].get('source')))
            print("".join(str(i) for i in m))
            py_code = "\r\n".join(str(i) for i in m)

            with open(root + 'py/' + new + '.txt', "w", encoding='utf-8') as f:
                f.write(py_code)
