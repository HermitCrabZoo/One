import cv2
import numpy as np
from scipy import ndimage
#核各权重加起来等于0得到边缘检测核,等于1为锐化核
kernel_3x3=np.array([[-1,-1,-1],
					 [-1,8,-1],
					 [-1,-1,-1]])

kernel_5x5=np.array([[-1,-1,-1,-1,-1],
					 [-1,1,2,1,-1],
					 [-1,2,4,2,-1],
					 [-1,1,2,1,-1],
					 [-1,-1,-1,-1,-1]])

img=cv2.imread("e:\\images\\faces\\1face_1.jpeg",0)#原始颜色空间：-1，灰度图：0，BGR：1
k3=ndimage.convolve(img,kernel_3x3)
k5=ndimage.convolve(img,kernel_5x5)
blurred=cv2.GaussianBlur(img,(11,11),0)
g_hpf=img-blurred

cv2.imshow("3x3",k3)
cv2.imshow("5x5",k5)
cv2.imshow("g_hpf",g_hpf)
cv2.waitKey()
cv2.destroyAllWindows()