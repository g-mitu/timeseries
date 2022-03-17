"""
	绘制五星红旗(Five-Starred Red Flag)
	@Author: Notus(hehe_xiao@qq.com)
	@Create: 2019-02-18
	@Update: 2019-02-19
	@Version: 1.0
	
	国旗数据分析：(参照下方参考图片)
	1. 最小单元格 A 的大小设为(长*宽，下同)：10*10
	2. 左上角1/4矩形B被分成：15*10个A, 尺寸为 150 * 100
	3. 国旗矩形C大小为:300 * 200(为3:2的比例)
	4. 若向下为正，向右为正。大五角星相对国旗左上角(0,0)坐标为(x, y): (50, 50)
	5. 4个小五角星从上至下分别为：(100, 20), (120, 40), (120, 70), (100, 90)
	6. 五角星每个角36度
	

	国旗数据参考图片（国旗黑线图）：https://gss2.bdstatic.com/-fo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign=dc24ea3a11d5ad6ebef46cb8e0a252be/78310a55b319ebc4b97aa7678826cffc1f1716c9.jpg
	
"""

import turtle
from math import *

# 绘制五角星, 默认为正五角星(一个顶点朝正北方)
# 五角星每个顶角的角度为 180/5 = 36度 或 pi/5
# (x, y): 五角星中心点坐标
# size: 中心到顶点的长度, 即外接圆的半径
# angle 旋转角度, 正五角星正北顶点 turtle.left 方式旋转到被绘制五角星的角度
def draw5star(x=0, y=0, size=100, angle=0, fillcolor="yellow", pencolor="yellow"):
    turtle.speed(0)
    turtle.shape("blank")
    turtle.color(pencolor, fillcolor)
    turtle.penup()

    # 定位到中心点正北方顶点(angle为0时的正北方)
    turtle.goto(x, y)
    turtle.setheading(90)
    turtle.left(angle)
    turtle.forward(size)
    turtle.right(180 - 36 / 2)

    turtle.pendown()

    # 一条直线上的两个顶点的距离
    distance = 2 * size * cos(pi / 10)

    # 开始绘制，对于 angle 为 0 的, 从正北方顶点开始
    turtle.begin_fill()
    for i in range(5):
        turtle.forward(distance)
        turtle.right(144)
    turtle.end_fill()


# 画矩形
# (x,y) 矩形左上角坐标
def drawrectangle(x=0, y=0, height=100, width=100, fillcolor="red", pencolor="black"):
    turtle.speed(0)
    turtle.shape("blank")
    turtle.color(pencolor, fillcolor)
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(0)
    turtle.pensize(2)
    turtle.pendown()

    turtle.begin_fill()
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(height)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(height)
    turtle.end_fill()


# 画辅助线，方便判断
# (x,y) 国旗中心点坐标
# mag 国旗放大倍数
def drawsubline(x=0, y=0, mag=1):
    # 国旗尺寸
    width = 300 * mag
    height = 200 * mag

    # 画中心十字
    turtle.speed(0)
    turtle.shape("blank")
    turtle.pencolor("black")
    turtle.penup()
    turtle.goto(x + width / 2, y)
    turtle.setheading(180)
    turtle.pensize(2)
    turtle.pendown()
    turtle.forward(width)
    turtle.penup()
    turtle.goto(x, y - height / 2)
    turtle.setheading(90)
    turtle.pendown()
    turtle.forward(height)

    # 画小方格的横线
    for i in range(1, 10):
        # 横线
        turtle.penup()
        turtle.goto(x, y + height / 2 - i * 10 * mag)
        turtle.setheading(180)
        turtle.pendown()
        turtle.forward(width / 2)

    # 画小方格的竖线
    for i in range(1, 15):
        turtle.penup()
        turtle.goto(x - width / 2 + i * 10 * mag, y)
        turtle.setheading(90)
        turtle.pendown()
        turtle.forward(height / 2)

    # 计算国旗矩形左上角坐标
    r_x = x - width / 2
    r_y = y + height / 2

    # 画大五角星外接圆，圆绘制起始点为圆最右侧切点
    turtle.penup()
    turtle.goto(r_x + 80 * mag, r_y - 50 * mag)
    turtle.pendown()
    turtle.circle(30 * mag)

    # 画4个小五角星外接圆，从上至下 (110, 20), (130, 40), (130, 70), (110, 90)
    turtle.penup()
    turtle.goto(r_x + 110 * mag, r_y - 20 * mag)
    turtle.pendown()
    turtle.circle(10 * mag)

    turtle.penup()
    turtle.goto(r_x + 130 * mag, r_y - 40 * mag)
    turtle.pendown()
    turtle.circle(10 * mag)

    turtle.penup()
    turtle.goto(r_x + 130 * mag, r_y - 70 * mag)
    turtle.pendown()
    turtle.circle(10 * mag)

    turtle.penup()
    turtle.goto(r_x + 110 * mag, r_y - 90 * mag)
    turtle.pendown()
    turtle.circle(10 * mag)

    # 画4个小星到大星中心的连线
    turtle.penup()
    turtle.goto(r_x + 100 * mag, r_y - 20 * mag)
    turtle.pendown()
    turtle.goto(r_x + 50 * mag, r_y - 50 * mag)

    turtle.penup()
    turtle.goto(r_x + 120 * mag, r_y - 40 * mag)
    turtle.pendown()
    turtle.goto(r_x + 50 * mag, r_y - 50 * mag)

    turtle.penup()
    turtle.goto(r_x + 120 * mag, r_y - 70 * mag)
    turtle.pendown()
    turtle.goto(r_x + 50 * mag, r_y - 50 * mag)

    turtle.penup()
    turtle.goto(r_x + 100 * mag, r_y - 90 * mag)
    turtle.pendown()
    turtle.goto(r_x + 50 * mag, r_y - 50 * mag)


# 绘制五星红旗
# (x, y) 红旗中心点坐标， 默认为(0,0)，即标准模式turtle绘图的中心起点。
# mag: 放大倍数, maganification
def drawflag(x=0, y=0, mag=1):
    # 国旗尺寸
    width = 300 * mag
    height = 200 * mag

    # 计算国旗矩形左上角坐标
    r_x = x - width / 2
    r_y = y + height / 2
    # 画国旗矩形
    drawrectangle(x=r_x, y=r_y, height=height, width=width)

    # 画最大的五角星
    draw5star(x=r_x + 50 * mag, y=r_y - 50 * mag, size=30 * mag)
    # draw5star(x=r_x+50*mag, y=r_y-50*mag, size=30*mag)

    # 从上至下画4颗小五角星, 中心：(100, 20), (120, 40), (120, 70), (100, 90)
    l_size = 10 * mag
    draw5star(
        x=r_x + 100 * mag,
        y=r_y - 20 * mag,
        size=l_size,
        angle=180 - atan(5 / 3) / pi * 180,
    )
    draw5star(
        x=r_x + 120 * mag,
        y=r_y - 40 * mag,
        size=l_size,
        angle=180 - atan(7 / 1) / pi * 180,
    )
    draw5star(
        x=r_x + 120 * mag,
        y=r_y - 70 * mag,
        size=l_size,
        angle=90 - atan(2 / 7) / pi * 180,
    )
    draw5star(
        x=r_x + 100 * mag,
        y=r_y - 90 * mag,
        size=l_size,
        angle=90 - atan(4 / 5) / pi * 180,
    )


if __name__ == "__main__":
    # turtle.screensize(canvwidth=None, canvheight=None, bg=None)，参数分别对应画布的宽(单位像素), 高, 背景颜色。
    # 如：turtle.screensize(1000,800, "red")
    turtle.screensize()  # 返回默认大小(500, 400)
    #    turtle.setup(width=0.5, height=0.75, startx=None, starty=None)
    # 参数：width, height: 输入宽和高为整数时, 表示像素; 为小数时, 表示占据电脑屏幕的比例，(startx, starty): 这一坐标表示矩形窗口左上角顶点的位置, 如果为空,则窗口位于屏幕中心。
    # 如：turtle.setup(width=0.6,height=0.6)
    turtle.setup(width=1.0, height=1.0, startx=0, starty=0)
    drawflag(mag=10)
    # drawsubline(mag=2.5)
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file="chi5starsflag.eps")

    input()

