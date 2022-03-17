import cv2 as cv
import numpy as np

# OpenCV提供了两个转换函数cv2.warpAffine和cv2.warpPerspective，可以使用它们进行各种转换。
# cv2.warpAffine采用2x3变换矩阵，而cv2.warpPerspective采用3x3变换矩阵作为输入。
# 对shrinking，优选的interpolation方法：cv2.INTER_AREA该方法可以避免波纹的出现
# def shrinking:
img = cv.imread("messi5.jpg")
res = cv.resize(img, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
# 对zooming，优选的interpolation方法：cv2.INTER_CUBIC和cv2.INTER_LINEAR(默认)
# def zooming:
height, width = img.shape[:2]
res = cv.resize(img, (2 * width, 2 * height), interpolation=cv.INTER_CUBIC)

# 图像平移，按（100,50）平移
# def moving:
img = cv.imread("img.jpg", 0)
rows, cols = img.shape

M = np.float32([[1, 0, 100], [0, 1, 50]])
dst = cv.warpAffine(img, M, (cols, rows))

cv.imshow("img", img)
cv.imshow("dst", dst)
cv.waitKey(0)
cv.destroyAllWindows()

# 将图像相对于中心旋转90度而不进行任何缩放
img = cv.imread("img.jpg", 0)
rows, cols = img.shape

# cols-1 and rows-1 are the coordinate limits.
M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), 90, 1)
dst = cv.warpAffine(img, M, (cols, rows))
cv.imshow("img", img)
cv.imshow("dst", dst)
cv.waitKey(0)
cv.destroyAllWindows()

# 仿射变换中，原始图像中的所有平行线仍将在输出图像中平行。
# 为了找到变换矩阵，我们需要输入图像中的三个点及其在输出图像中的相应位置。
# 然后cv.getAffineTransform将创建一个2x3矩阵，该矩阵将传递给cv.warpAffine。
img = cv.imread("img5.jpg")
rows, cols, ch = img.shape

pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

M = cv.getAffineTransform(pts1, pts2)
dst = cv.warpAffine(img, M, (cols, rows))

# 透视变换，需要一个3x3变换矩阵。 即使在转换之后，直线仍将保持笔直.
# 要找到此变换矩阵，输入图像上需要4个点，输出图像上需要相应的点.
# 在这4个点中，其中3个不应该共线. 然后可以通过函数cv2.getPerspectiveTransform找到变换矩阵.
# 然后将cv2.warpPerspective应用于此3x3变换矩阵。
img = cv.imread("img6.jpg")
rows, cols, ch = img.shape

pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

M = cv.getPerspectiveTransform(pts1, pts2)
dst = cv.warpPerspective(img, M, (300, 300))
