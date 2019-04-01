import cv2

# videoCapture
# videoCapture=cv2.VideoCapture("E:\\images\\video.mp4")
# fps=videoCapture.get(cv2.CAP_PROP_FPS)
# size=(int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# print(fps)
# print(size)
# videoWriter=cv2.VideoWriter("E:\\images\\videoCapture.mp4",cv2.VideoWriter_fourcc("X","V","I","D"),fps,size)
# success,frame=videoCapture.read();
# while success:
# 	videoWriter.write(frame)
# 	success,frame=videoCapture.read()

# cameraCapture
# cameraCapture=cv2.VideoCapture(0)
# fps=30
# size=(int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# cameraWriter=cv2.VideoWriter("E:\\images\\cameraCapture.mp4",cv2.VideoWriter_fourcc("X","V","I","D"),fps,size)
# success,frame=cameraCapture.read();
# numFramesRemaining=10*fps-1
# while success and numFramesRemaining>0:
# 	cameraWriter.write(frame)
# 	success,frame=cameraCapture.read()
# 	numFramesRemaining-=1
# cameraCapture.release()

# live photos
clicked=False
def onMouse(event,x,y,flags,param):
	global clicked
	if event == cv2.EVENT_LBUTTONUP:
		clicked=True
		print("mouse left button up!")
cameraCapture=cv2.VideoCapture(0)
cv2.namedWindow("MyFace")
cv2.setMouseCallback("MyFace",onMouse)
print("Showing camera captures.Click window or press any key to stop it.")
success,frame=cameraCapture.read();
t=float(cv2.getCPUTickCount())
while success and cv2.waitKey(1)==-1 and not clicked:
	t=(float(cv2.getTickCount())-t)/cv2.getTickFrequency()
	fps=1.0/t
	cv2.flip(frame,1,frame)
	cv2.putText(frame,"FPS:"+str(fps),(20,20),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0))
	cv2.imshow("MyFace",frame)
	success,frame=cameraCapture.read()
cv2.destroyWindow("MyFace")
cameraCapture.release()
print("camera has released.")

