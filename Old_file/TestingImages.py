from picamera import PiCamera
from time import sleep
camera = PiCamera()

camera.resolution = (1280,720)
camera.framerate=30
camera.rotation = 180
#frame1 = Frame(1280,720,10)

camera.start_preview()
for i in range(1,100,1):
	camera.capture("TestingImage/Image"+str(i)+".jpg")
	print("sleeping")
	sleep(1)
	print("wakeup")
# 
# data = frame1.get_data(array,0) #select the data    
# edges = ef(50,5, 6,data) #calculate the Boundary
# print(edges.BND)

    #Covert eges.BND to the x-y coordinates
# allPoints = np.array([frame1.fline[i][int(edges.BND[int(i)-1])]for i in frame1.fline.keys()])
# print(allPoints)


# plt.gray()
# plt.imshow(array)
# plt.plot(allPoints[:,0],allPoints[:,1],'b.')
# plt.show()
