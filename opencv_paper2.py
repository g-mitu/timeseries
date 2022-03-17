import cv2
import numpy as np


def cv_show(imgname, img):
    cv2.imshow(imgname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 按左上，右上，右下，左下排序坐标
def order_points(pts):
    rec = np.zeros((4, 2), dtype="float32")
    # 找出左上，右下
    s = np.sum(pts, axis=1)
    rec[0] = pts[np.argmin(s)]
    rec[2] = pts[np.argmax(s)]
    # 找出右上，左下 （x,y） y-x相差最小最大
    diff = np.diff(pts)
    rec[1] = pts[np.argmin(diff)]
    rec[3] = pts[np.argmax(diff)]
    return rec


# 透视变换后的对应坐标
def four_point_wrap(img, pts):
    rec = order_points(pts)
    tl, tr, br, bl = rec
    # 找到最大的宽和高
    widthA = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    widthB = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width = max(int(widthB), int(widthA))
    lengthA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    lengthB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    length = max(int(lengthA), int(lengthB))
    print("width:{},length:{}".format(width, length))
    # width,length都减去100，完整的图像才会显示出来，小了的话会显示不完整，这一部分笔者也有点困惑
    dst = np.array(
        [(0, 0), (width - 100, 0), (width - 100, length - 100), (0, length - 100)],
        dtype="float32",
    )
    M = cv2.getPerspectiveTransform(rec, dst)
    wrap = cv2.warpPerspective(img, M, (width, length))
    return wrap


def resize(img, height=None, width=None, inter=cv2.INTER_AREA):  # cv2.INIER_AREA 插值方法
    dim = None
    (h, w) = img.shape[:2]
    if width is None and height is None:
        return img
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(h)
        dim = (width, int(h * r))
    resized = cv2.resize(img, dim, interpolation=inter)
    return resized


img = cv2.imread("ocrbook.jpg")
print(img.shape)
ratio = img.shape[0] / 500.0
orig = img.copy()
# 等比例缩小
img = resize(orig, height=400)
# 转化成灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv_show('gray',gray)
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
kernel1 = np.ones([3, 3])
# 锐度处理 对于此图像，词操作会使噪音点变多，边缘检测效果变差，故舍弃
# dst = cv2.filter2D(gray, -1, kernel=kernel)
# cv_show('dst',dst)
# 高斯模糊
gaussian = cv2.GaussianBlur(gray, (1, 1), 0)
# cv_show('gaussian',gaussian)
# 二值化处理
# thresh = cv2.threshold(gray,20,250,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
# cv_show('thresh',thresh)
kernel = np.ones([3, 3])

# 边缘检测
canny = cv2.Canny(gaussian, 120, 200)
cv_show("canny", canny)
# 膨胀操作 使细小的未连接的边缘连接起来，使得图像有封闭区域
dilate = cv2.morphologyEx(canny, cv2.MORPH_DILATE, kernel1, iterations=2)
cv_show("dilate", dilate)
# 腐蚀
erode = cv2.morphologyEx(dilate, cv2.MORPH_ERODE, kernel1)
cv_show("erode", erode)
# 轮廓检测
cnts = cv2.findContours(erode, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
# 按轮廓面积升序排列
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4]
for cnt in cnts:
    perix = cv2.arcLength(cnt, True)
    print(perix)
    approx = cv2.approxPolyDP(cnt, 0.03 * perix, True)
    print("len(approx): ", len(approx))
    # 找到矩形
    if len(approx) == 4:
        screen = approx
        break
cv2.drawContours(img, [screen], -1, (0, 25, 155), 2)
cv_show("cnts", img)
screen = screen.reshape(4, 2) * ratio
print(screen)
# 透视变换
wraped = four_point_wrap(orig, screen)
cv_show("wrapwd", wraped)
