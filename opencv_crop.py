import cv2
import glob
import os
import numpy as np

i = 0
def crop(img, outdir):
    img = cv2.imread(img) #读入图片
    cropped = img[206:430, 252:476]  # 裁剪坐标为[y0:y1, x0:x1]
    # cv2.imwrite('5.jpg', cropped)
    cv2.imwrite("./caijian/{}.jpg".format(i), cropped) #裁剪并存储在指定文件夹中

def convertjpg(jpgfile,outdir,width=128,height=128):  
    src = cv2.imread(jpgfile, cv2.IMREAD_ANYCOLOR)    
    try:
        dst = cv2.resize(src, (width,height), interpolation=cv2.INTER_CUBIC) 
        cv2.imwrite(os.path.join(outdir,os.path.basename(jpgfile)), dst)
    except Exception as e:
        print(e)

def rotate_bound(image, angle):
  # grab the dimensions of the image and then determine the
  # center
  (h, w) = image.shape[:2]
  (cX, cY) = (w // 2, h // 2)
  
  # grab the rotation matrix (applying the negative of the
  # angle to rotate clockwise), then grab the sine and cosine
  # (i.e., the rotation components of the matrix)
  M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
  cos = np.abs(M[0, 0])
  sin = np.abs(M[0, 1])
  
  # compute the new bounding dimensions of the image
  nW = int((h * sin) + (w * cos))
  nH = int((h * cos) + (w * sin))
  
  # adjust the rotation matrix to take into account translation
  M[0, 2] += (nW / 2) - cX
  M[1, 2] += (nH / 2) - cY
  
  # perform the actual rotation and return the image
  return cv2.warpAffine(image, M, (nW, nH))


for jpgfile in glob.glob(r'C:\Users\x\Desktop\kk\*.jpg'):
    convertjpg(jpgfile,r'C:\Users\x\Desktop\re') 
for img in glob.glob("./plam/*.jpg"): #对需要裁剪的图片的文件夹循环读取
    crop(img,"./caijian")
    i = i+1
