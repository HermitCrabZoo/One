import numpy as np
import cv2
import os

img = np.zeros((3, 3), dtype=np.uint8)
# print(img)
bgrImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
# print(bgrImg)
# print(img.shape)
# print(bgrImg.shape)

# image=cv2.imread("E:\\images\\dist1.png")
# cv2.imwrite("E:\\images\\dist1.jpg",image)

randomByteArray=bytearray(os.urandom(120000))
flatNumpyArray=np.array(randomByteArray)
grayImage=flatNumpyArray.reshape(300,400)
bgrImage=flatNumpyArray.reshape(100,400,3)
# 更高效
# grayImage=np.random.randint(0,256,120000).reshape(300,400)
# bgrImage=np.random.randint(0,256,120000).reshape(100,400,3)
# print(randomByteArray)
# print(flatNumpyArray)
# print(grayImage)
# print(bgrImage)
# cv2.imwrite("E:\\images\\gray.png",grayImage)
# cv2.imwrite("E:\\images\\bgr.png",bgrImage)

img=cv2.imread("E:\\images\\videoV.png")
img[:,:,1]=0
img[:,:,2]=0
img[0,0]=[255,255,255]
print(img.item(1,1,2))
img.itemset((1,1,0),255)
cv2.imshow("test1",img)
cv2.waitKey()
