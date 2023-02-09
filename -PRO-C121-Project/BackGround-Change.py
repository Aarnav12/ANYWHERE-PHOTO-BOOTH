import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0)

# loading the mountain image
mountain = cv2.imread('Road-To-Mountains-Hd-Wallpaper.jpg')
mountain = cv2.resize(mountain, (640, 480))

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0

#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Flipping the background
bg = np.flip(bg, axis=1)

#Reading the captured frame until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    #Flipping the image for consistency
    img = np.flip(img, axis=1)

    #Converting image to hsv format
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower_red=np.array([0,120,255])
    upper_red=np.array([10,255,255])

    mask_1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])

    mask_2=cv2.inRange(hsv,lower_red,upper_red)

    mask=mask_1+mask_2
   #mask_1 area containing red cloth
    mask_1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))
    
    #mask_2 area not containing red cloth
    mask_2 = cv2.bitwise_not(mask_1)

    res_1 = cv2.bitwise_and(img,img,mask = mask_2)

    res_2 = cv2.bitwise_and(bg,mountain,mask = mask_1)
    
    res = cv2.addWeighted(res_1, 1, res_2, 1, gamma = 0)

    #Generating the final output
    
    output_file.write(res)
    #Displaying the output to the user
    cv2.imshow("magic", res)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()

