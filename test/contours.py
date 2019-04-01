import cv2
import numpy as np

#轮廓检测
def findSquare():
	img = np.zeros((200, 200), dtype=np.uint8)
	img[50:150, 50:150] = 255

	ret, thresh = cv2.threshold(img, 127, 255, 0)
	# 该函数会修改原图像，建议传入原图像的拷贝img.copy(),若只想得到最外面的轮廓需将cv2.RETR_TREE改为cv2.RETR_EXTERNAL
	# 返回值：修改后的图像、轮廓，层次
	image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	img = cv2.drawContours(color, contours, -1, (0, 255, 0), 2)
	cv2.imshow("contours", img)
	cv2.waitKey()
	cv2.destroyAllWindows()

#详细的轮廓检测
def finds():
	img = cv2.pyrDown(cv2.imread("E:\\images\\shotcut.png",cv2.IMREAD_UNCHANGED))

	ret,thresh=cv2.threshold(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY),127,255,cv2.THRESH_BINARY)
	image,contours,hier=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


	for c in contours:
		#find bounding box coordinates
		x,y,w,h = cv2.boundingRect(c)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		#find minimum area
		rect = cv2.minAreaRect(c)
		#calculate coordinates of the minimum area rectangle
		box = cv2.boxPoints(rect)
		#normalize coordinates to integers
		box = np.int0(box)
		#draw contours
		cv2.drawContours(img,[box],0,(0,0,255),3)

		#calculate center and radius of minimum enclosing circle
		(x,y),radius=cv2.minEnclosingCircle(c)
		#cast to integers
		center=(int(x),int(y))
		radius= int (radius)
		#draw the circle
		img=cv2.circle(img,center,radius,(0,255,0),2)
	cv2.drawContours(img,contours,-1,(255,0,0),1)
	cv2.imshow("contours",img)
	cv2.waitKey()
	cv2.destroyAllWindows()


#直线检测
def houghLine():
	img=cv2.imread("E:\\images\\Cameo\\minCapture.png")
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges=cv2.Canny(gray,50,120)
	minLineLength=20
	maxLineGap=5
	lines=cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=minLineLength,maxLineGap=maxLineGap)
	print(len(lines))
	for line in lines:
		x1, y1, x2, y2=line[0]
		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
	cv2.imshow("edges", edges)
	cv2.imshow("lines", img)
	cv2.waitKey()
	cv2.destroyAllWindows()


#圆检测
def houghCircle():
	planets = cv2.imread("E:\\images\\eightPlanet.jpg")
	gray = cv2.cvtColor(planets, cv2.COLOR_BGR2GRAY)
	img=cv2.medianBlur(gray,5)
	cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

	circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=0,maxRadius=0)
	for i in circles[0,:]:
		#draw the outer circle
		cv2.circle(planets,(i[0],i[1]),i[2],(0,255,0),2)
		# draw the center of the circle
		cv2.circle(planets, (i[0], i[1]), 2, (0, 0, 255), 3)

	cv2.imshow("circles", planets)
	cv2.waitKey()
	cv2.destroyAllWindows()


if __name__=="__main__":
	# findSquare()
	# finds()
	# houghLine()
	houghCircle()