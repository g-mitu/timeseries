# 成作日期&#xff1a;2021年7月28日
# 以此程序热烈祝贺中国共产党成立100周年&#xff01;
import turtle  # 导入头文件

turtle.fillcolor("red")
turtle.pencolor("red")

turtle.up()
turtle.goto(-300, 300)
turtle.down()

turtle.begin_fill()
for i in range(2):
    turtle.forward(600)
    turtle.right(90)
    turtle.forward(400)
    turtle.right(90)
turtle.end_fill()


turtle.fillcolor("yellow")  # 选定颜色
turtle.pencolor("yellow")


turtle.up()
turtle.goto(10, 220)
turtle.seth(225)
turtle.down()

turtle.begin_fill()
turtle.fd(125)
turtle.right(90)
turtle.fd(50)
turtle.right(90)
turtle.fd(100)
turtle.right(90)
turtle.circle(25, 90)
turtle.end_fill()

turtle.up()
turtle.goto(-40, 190)
turtle.seth(-45)
turtle.down()

turtle.begin_fill()
for i in range(2):
    turtle.forward(200)
    turtle.right(90)
    turtle.forward(30)
    turtle.right(90)
turtle.end_fill()


turtle.up()
turtle.goto(-100, 100)
turtle.seth(-50)
turtle.down()

turtle.begin_fill()
turtle.circle(100, 180)
turtle.fd(20)
turtle.right(157)
turtle.circle(-115, 190)
turtle.left(90)
turtle.fd(20)
turtle.right(90)
turtle.fd(20)
turtle.right(90)
turtle.fd(20)
turtle.left(80)
turtle.fd(30)
turtle.end_fill()

turtle.up()
turtle.goto(-90, 50)
turtle.down()

turtle.begin_fill()
turtle.circle(20)
turtle.end_fill()


ts = turtle.getscreen()
ts.getcanvas().postscript(file="liandaoflag.eps")

turtle.hideturtle()  # 隐藏小海龟
# 维持面板
turtle.done()
