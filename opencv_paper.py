# 基于python+opencv的图像目标区域自动提取
import math
import cv2 as cv
import numpy as np


def order_points(pts):
    # 一共四个坐标点
    rect = np.zeros((4, 2), dtype="float32")

    # 按顺序找到对应的坐标0123 分别是左上，右上，右下，左下
    # 计算左上，右下
    # numpy.argmax(array, axis) 用于返回一个numpy数组中最大值的索引值
    s = pts.sum(axis=1)  # [2815.2   1224.    2555.712 3902.112]
    print(s)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # 计算右上和左
    # np.diff()  沿着指定轴计算第N维的离散差值  后者-前者
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def point_distance(top_top, top_bottom):
    # box[0] box[1] = width
    # box[1] box[2] = Height
    # 计算输入的w和h的值
    widtH = np.sqrt(
        ((top_top[0] - top_bottom[0]) ** 2) + ((top_top[1] - top_bottom[1]) ** 2)
    )

    return widtH


# 由于手机拍摄的照片像素可能会很高，为了加快处理速度，我们首先将图像转化为灰度图
src = r"C:/Users/zyhly/Downloads/demo_rectangle.jpg"
threshold_thresh = 45  # 45值越小白色区域面积越大
min_contours = 20  # 最小也有100个轮廓吧
epsilon_start = 1.0
min_area = 10
epsilon_step = 1

image = cv.imread(src)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
srcWidth, srcHeight, channels = image.shape
print(srcWidth, srcHeight)
# 2、中值滤波
binary = cv.medianBlur(gray, 7)
# 3、转化为二值图像
ret, binary = cv.threshold(binary, threshold_thresh, 255, cv.THRESH_BINARY)
cv.imwrite("1-threshold.png", binary, [int(cv.IMWRITE_PNG_COMPRESSION), 9])
# S2
# 我们用Canny算子边缘检测，提取轮廓
# canny提取轮廓
binary = cv.Canny(binary, 0, 60, apertureSize=3)
cv.imwrite("3-canny.png", binary, [int(cv.IMWRITE_PNG_COMPRESSION), 9])
# _, contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #opencv3
contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
print("len(contours)=%d" % (len(contours)))


# 提取面积最大的轮廓并用多边形包围
for idx, c in enumerate(contours):
    epsilon = 0.01 * cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, epsilon, True)
    print(
        "idx,epsilon,len(approx),len(c)=%d,%d,%d,%d"
        % (idx, epsilon, len(approx), len(c))
    )
    if len(approx) == 4:
        # for p in approx:
        #    cv.circle(binary,(p[0][0],p[0][1]),8,(255,255,0),thickness=-1)
        approx = approx.reshape((4, 2))
        # 点重排序, [top-left, top-right, bottom-right, bottom-left]
        src_rect = order_points(approx)
        cv.drawContours(image, c, -1, (0, 255, 255), 1)
        cv.line(
            image,
            (src_rect[0][0], src_rect[0][1]),
            (src_rect[1][0], src_rect[1][1]),
            color=(100, 255, 100),
        )
        cv.line(
            image,
            (src_rect[2][0], src_rect[2][1]),
            (src_rect[1][0], src_rect[1][1]),
            color=(100, 255, 100),
        )
        cv.line(
            image,
            (src_rect[2][0], src_rect[2][1]),
            (src_rect[3][0], src_rect[3][1]),
            color=(100, 255, 100),
        )
        cv.line(
            image,
            (src_rect[0][0], src_rect[0][1]),
            (src_rect[3][0], src_rect[3][1]),
            color=(100, 255, 100),
        )
        # 获取最小矩形包络
        rect = cv.minAreaRect(approx)
        # rect = cv.maxAreaRect(approx)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        box = box.reshape(4, 2)
        box = order_points(box)
        print("approx->box")
        print(approx)
        print(src_rect)
        print(box)
        w, h = point_distance(box[0], box[1]), point_distance(box[1], box[2])
        print("w,h=%d,%d" % (w, h))
        dst_rect = np.array(
            [[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype="float32"
        )
        M = cv.getPerspectiveTransform(src_rect, dst_rect)
        warped = cv.warpPerspective(image, M, (w, h))
        cv.imwrite("transfer%d.png" % idx, warped, [int(cv.IMWRITE_PNG_COMPRESSION), 9])
        break
"""
for idx, c in enumerate(contours):
#    if len(c) < min_contours:
#        continue
    #    epsilon = epsilon_start #精度？
    epsilon = 0.01 * cv.arcLength(c, True)
    while True:
        approx = cv.approxPolyDP(c, epsilon, True)
        print("idx,epsilon,len(approx),len(c)=%d,%d,%d,%d" % (idx, epsilon, len(approx),len(c)))
        if len(approx) < 4:
            break
        flag = math.fabs(cv.contourArea(approx))  # 求绝对值的函数
        print("79#", flag)
        if flag > min_area:
            if len(approx) > 4:
                epsilon += epsilon_step
                print("epsilon=%d, count=%d" % (epsilon, len(approx)))
                continue
            else:
                # for p in approx:
                #    cv.circle(binary,(p[0][0],p[0][1]),8,(255,255,0),thickness=-1)
                approx = approx.reshape((4, 2))
                # 点重排序, [top-left, top-right, bottom-right, bottom-left]
                src_rect = order_points(approx)
                cv.drawContours(image, c, -1, (0, 255, 255), 1)
                cv.line(
                    image,
                    (src_rect[0][0], src_rect[0][1]),
                    (src_rect[1][0], src_rect[1][1]),
                    color=(100, 255, 100),
                )
                cv.line(
                    image,
                    (src_rect[2][0], src_rect[2][1]),
                    (src_rect[1][0], src_rect[1][1]),
                    color=(100, 255, 100),
                )
                cv.line(
                    image,
                    (src_rect[2][0], src_rect[2][1]),
                    (src_rect[3][0], src_rect[3][1]),
                    color=(100, 255, 100),
                )
                cv.line(
                    image,
                    (src_rect[0][0], src_rect[0][1]),
                    (src_rect[3][0], src_rect[3][1]),
                    color=(100, 255, 100),
                )
                # 获取最小矩形包络
                rect = cv.minAreaRect(approx)
                # rect = cv.maxAreaRect(approx)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                box = box.reshape(4, 2)
                box = order_points(box)
                print("approx->box")
                print(approx)
                print(src_rect)
                print(box)
                w, h = point_distance(box[0], box[1]), point_distance(box[1], box[2])
                print("w,h=%d,%d" % (w, h))
                dst_rect = np.array(
                    [[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype="float32"
                )
                M = cv.getPerspectiveTransform(src_rect, dst_rect)
                warped = cv.warpPerspective(image, M, (w, h))
                cv.imwrite(
                    "transfer%d.png" % idx, warped, [int(cv.IMWRITE_PNG_COMPRESSION), 9]
                )
                break
"""
