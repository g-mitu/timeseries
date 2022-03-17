import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

#
img = cv.imread(r'Lena.png')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
t1, rst1 = cv.threshold(imgray,127,255,cv.THRESH_BINARY) # 二值化阈值处理。大于127的像素点会被处理为255，其余处理为0
t2, rst2 = cv.threshold(imgray,127,255,cv.THRESH_BINARY_INV) # 反二值化阈值处理。灰度值大于127的像素点处理为0，其余为255
t3, rst3 = cv.threshold(imgray,127,255,cv.THRESH_TRUNC) # 截断阈值化处理。大于127的像素点处理为127，其余保持不变
t4, rst4 = cv.threshold(imgray,127,255,cv.THRESH_TOZERO_INV) # 超阈值零处理。大于127的像素点处理为0，其余保持不变
t5, rst5 = cv.threshold(imgray,127,255,cv.THRESH_TOZERO) # 低阈值零处理。大于127的像素点保持不变，其余处理为0
titles = ['Original','BINARY','BINARY_INV','TRUNC','TOZERO_INV','TOZERO']
images = [imgray,rst1,rst2,rst3,rst4,rst5]
for i in range(6):
    plt.subplot(2,3,i+1), plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()

##自适应阈值处理
# 对于色彩不均衡的图像来说，只使用一个阈值，无法得到较理想的阈值分割结果。自适应阈值处理通过计算每个像素点周围临近的加权平均值获得阈值，能够更好的处理由光照变化带来影响的图像。
# 阈值处理方法须为 cv2.THRESH_BINARY 或 cv2.THRESH_BINARY_INV
# 自适应方法有 cv2.ADAPTIVE_THRESH_MEAN_C 和 cv2.ADAPTIVE_THRESH_GAUSSIAN_C 。前者领域所有像素点的权重值一致；后者与邻域各个像素点到中心点的距离有关，通过高斯方程获得各点的权重。
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

img = cv.imread(r'exc.png')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
t, rst = cv.threshold(imgray,127,255,cv.THRESH_BINARY)
athdMEAN = cv.adaptiveThreshold(imgray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,5,3)
athdGAUS = cv.adaptiveThreshold(imgray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,5,3)
titles = ['Original','Glbal Thresholding(v=127)','AdaptiveMean','AdaptiveGaussian']
images = [imgray,rst,athdMEAN,athdGAUS]
for i in range(4):
    plt.subplot(2,2,i+1)
    plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()

##Otsu处理（大津法）
# #不能观察出最合适的阈值，Otsu处理能够根据图像给出最佳的分割阈值。
import numpy as np
import cv2 as cv

img = np.zeros((5,5),dtype=np.uint8)
img[0:2,0:5] = 123
img[2:5,0:5] = 126
print('img=\n', img)
t1, thd = cv.threshold(img,127,255,cv.THRESH_BINARY)
t2, otsu = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
print('thd=\n', thd)
print('otsu=\n', otsu)