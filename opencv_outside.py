import cv2 as cv


src = cv.imread("./demo.jpg")
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
cv.imshow("src", src)
K = cv.waitKey(0)
if K == 27:  # 若键入ESC后退出
    cv.destroyAllWindows()  # 销毁我们创建的所有窗口
elif K == ord("s"):  # 若键入s后执行以下代码
    cv.imwrite("D:/study/opencvpython/picture/messigray.png", gray)  # 保存图片至‘地址'
    cv.destroyALLWindows()
gray = cv.GaussianBlur(gray, (5, 5), 0)
edges = cv.Canny(gray, 70, 210)
cv.imshow("edged", edges)
K = cv.waitKey(0)
if K == 27:  # 若键入ESC后退出
    cv.destroyAllWindows()  # 销毁我们创建的所有窗口
# 轮廓检测
# 下面就是检测图像轮廓具体位置的代码了：
contours, hierarchy = cv.findContours(
    edges.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE
)
print(f"轮廓数量：{len(contours)}")
"""
在 cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE) 中，第二个参数使用的是 cv.RETR_LIST，该参数值表示检测所有轮廓，不建立等级关系，彼此独立。如果只想获取轮廓边缘信息,不关心是否嵌套在另一个轮廓之内，使用该参数值即可。
第三个参数使用的是 cv.CHAIN_APPROX_SIMPLE，表示压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需 4 个点来保存轮廓信息，这也是为了后面便于计算。
观察上图，可以发现最外侧的边缘面积是最大的，所以依据面积进行排序，依据其他值也可以，获取面积最大的轮廓。
"""
contours = sorted(contours, key=cv.contourArea, reverse=True)[:3]
# 对轮廓进行简单绘制，获得下图效果。
cv.drawContours(src, contours, -1, (0, 0, 255), 2)
K = cv.waitKey(0)
if K == 27:  # 若键入ESC后退出
    cv.destroyAllWindows()  # 销毁我们创建的所有窗口
# 遍历轮廓，计算轮廓近似,先看代码：
# 遍历轮廓

for c in contours:
    # 计算轮廓近似
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.02 * peri, True)
# 一个新的函数 cv.arcLength，该函数的原型如下：retval = cv2.arcLength(curve, closed)
# 该函数用于计算轮廓的周长。
# 下面的 cv.approxPolyDP 函数原型如下：approxCurve = cv2.approxPolyDP(curve, epsilon, closed[, approxCurve])
# 函数参数如下：curve：源图像的某个轮廓；
# epsilon：距离值，表示多边形的轮廓接近实际轮廓的程度，值越小，越精确；
# closed：轮廓是否闭合。
# 最重要的参数就是 epsilon 简单记忆为：该值越小，得到的多边形角点越多，轮廓越接近实际轮廓，该参数是一个准确度参数。
# 该函数返回值为轮廓近似多边形的角点。
# 绘制轮廓
# 最后判断，当上文返回的角点为 4 的时候，提取轮廓，代码如下：
# 遍历轮廓

for c in contours:
    # 计算轮廓近似
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.02 * peri, True)
    # 当恰好是 4 个角点的时候，获取轮廓。
    if len(approx) == 4:
        screen_cnt = approx
    break

# 结果显示
cv.drawContours(src, [screen_cnt], -1, (0, 0, 255), 2)
K = cv.waitKey(0)
if K == 27:  # 若键入ESC后退出
    cv.destroyAllWindows()  # 销毁我们创建的所有窗口
# 更换图片，进行再次轮廓检测，注意修改轮廓近似部分代码即可。
# 遍历轮廓

for c in contours:
    # 计算轮廓近似
    approx = cv.approxPolyDP(c, 30, True)
    if len(approx) == 4:
        screen_cnt = approx
    break
