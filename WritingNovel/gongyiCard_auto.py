import datetime
import os
import xlrd
from mailmerge import MailMerge


def Exceldate(dates):  # 定义转化日期戳的函数,dates为日期戳
    delta = datetime.timedelta(days=dates)
    # 将1899-12-30转化为可以计算的时间格式并加上要转化的日期戳
    today = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta
    return datetime.datetime.strftime(today, '%Y-%m-%d')  # 制定输出日期的格式


# 生成Word文档存储目录
path_base_name = r'C:/Users/zyhly/Documents/VBAForm/'
# 遍历当前目录下的所有文档，读取类型为Excel文件

# 打开Excel文件
xl = xlrd.open_workbook(os.path.join(path_base_name, "工艺卡数据库.xlsx"))
print(xl.sheet_names())
# 读取第1个表
table = xl.sheet_by_name(xl.sheet_names()[0])
# 获取表中行数
## nrows = table.nrows
# for i in range(nrows):  # 循环逐行打印  ;;被22、23行替换
nrows = [28]
for i in nrows:  # 循环逐行打印
    if i > 0:  # 第一行为表头，不作为填充数据
        print(str(int(table.row_values(i)[2])) +
              "年工杭" +
              "  " +
              str(table.row_values(i)[3]) +
              "  " +
              str(table.row_values(i)[4]) +
              "  " +
              str(table.row_values(i)[5]))
        if(i % 2) == 0:
            doc = MailMerge(
                r'C:/Users/zyhly/Documents/VBAForm/m包装工艺卡.docx')  # 打开模板文件
        # 以下为填充模板中对应的域，
            doc.merge(year=str(table.row_values(i)[2]).replace(".0", ""),
                      number=str(table.row_values(i)[3]).replace(".0", ""),
                      name=str(table.row_values(i)[4]),
                      machine=str(table.row_values(i)[5]),
                      hsize=str(table.row_values(i)[8]),
                      hspec=str(table.row_values(i)[9]),
                      hbar=str(table.row_values(i)[10]).replace(".0", ""),
                      tsize=str(table.row_values(i)[11]),
                      tspec=str(table.row_values(i)[12]),
                      tbar=str(table.row_values(i)[13]).replace(".0", ""),
                      xsize=str(table.row_values(i)[14]),
                      xspec=str(table.row_values(i)[15]),
                      xbar=str(table.row_values(i)[16]).replace(".0", ""),
                      material=str(table.row_values(i)[17]),
                      technology=str(table.row_values(i)[18]),
                      classA=str(table.row_values(i)[19]),
                      classB=str(table.row_values(i)[20]),
                      pub_day=Exceldate(table.row_values(i)[6]),
                      imp_day=Exceldate(table.row_values(i)[7])
                      )
        else:
            doc = MailMerge(
                r'C:/Users/zyhly/Documents/VBAForm/m卷接工艺卡.docx')  # 打开模板文件
            # 以下为填充模板中对应的域，
            doc.merge(year=str(table.row_values(i)[2]).replace(".0", ""),
                      number=str(table.row_values(i)[3]).replace(".0", ""),
                      name=str(table.row_values(i)[4]),
                      machine=str(table.row_values(i)[5]),
                      circumference=str(table.row_values(i)[8]),
                      length=str(table.row_values(i)[9]),
                      weight=str(table.row_values(i)[10]),
                      drawRes=str(table.row_values(i)[11]),
                      moisture=str(table.row_values(i)[12]),
                      eta=str(table.row_values(i)[13]).replace(".0", ""),
                      material=str(table.row_values(i)[17]),
                      technology=str(table.row_values(i)[18]),
                      classA=str(table.row_values(i)[19]),
                      classB=str(table.row_values(i)[20]),
                      pub_day=Exceldate(table.row_values(i)[6]),
                      imp_day=Exceldate(table.row_values(i)[7])
                      )
        # 使用文件名，学校，班级生成文件夹，并把学生按学校，班级进行分类存储
        word_name = table.row_values(i)[0] + '工艺卡_' + table.row_values(i)[4] + str(int(table.row_values(i)[2])) + '_' + str(
            int(table.row_values(i)[3])) + '_' + str(table.row_values(i)[5]).replace("/", "_") + '.docx'
        print("正在保存 " + word_name + " 到 " + path_base_name)
        doc.write(path_base_name + word_name)
        print("保存成功\n")
        if doc is None:
            doc.close()
        token = MailMerge(
            r'C:/Users/zyhly/Documents/VBAForm/m发放登记表.docx')  # 打开模板文件
        # 以下为填充模板中对应的域，
        token.merge(year=str(table.row_values(i)[2]).replace(".0", ""),
                    number=str(table.row_values(i)[3]).replace(".0", ""),
                    name=str(table.row_values(i)[4]),
                    worksec=str(table.row_values(i)[0]),
                    num=str(int(table.row_values(i)[1])),
                    s=str(int(table.row_values(i)[1] + 3)),
                    sum=str(int(table.row_values(i)[1] + 4))
                    )
        # 使用文件名，学校，班级生成文件夹，并把学生按学校，班级进行分类存储
        token_name = table.row_values(
            i)[0] + str(int(table.row_values(i)[2])) + '_' + str(int(table.row_values(i)[3])) + '登记表.docx'
        print("正在保存 " + token_name + " 到 " + path_base_name)
        token.write(path_base_name + token_name)
        print("保存成功\n")
        if token is None:
            token.close()
