#!/usr/bin/env python3
from __future__ import print_function

#Importing Nescessary Libraries

import roslib
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped

from cv_bridge import CvBridge, CvBridgeError

#Class defined to convert image using Cv_bridge

class image_converter:

  def __init__(self):


    self.bridge = CvBridge()
    print("Topic subscribing..")
    self.image_sub = rospy.Subscriber("/front_cam/camera/image",Image,self.callback)
    print("Topic subscribed...")
  def call(self,loc):
    try:
      file3 = open("contour.txt", "r") 
      a = int(file3.read())
      if(a>=2):
        file1 = open("Pos.txt","a")
        file1.write(str(loc.pose.position.x)+'   '+str(loc.pose.position.y) +"\n")
        file1.close()
        print("Location Reading done ......")
    except:
      print("Target not in sight")
   
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    flag=True
    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 : 
      cv2.circle(cv_image, (50,50), 10, 255)

    
    print("Image Proccesing undergoing.........")
    hsv = cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
    lower = np.array([110,50,50])
    upper = np.array([130,255,255])
    
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(cv_image, cv_image, mask = mask)

#Code block for Rectangular Block

    start_point = (60, 60) 
    end_point = (220,220)
    color = (0, 255, 0)
    thickness = 2
       
    #frame = cv2.imshow("Image window", output)
    #cv2.imshow("Image_windoW",mask)
    cv2.imshow("Image_Window",cv_image)
    (b, g, r) = cv_image[160, 120]

 
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY) 
    ret , thresh = cv2.threshold(gray, 127, 255, 0)

 
#Code block for Contours 

    
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

     
  
  

   
    cnt = cv2.drawContours(output,contours, -1, (0,255,0), 3)
    #cv2.imshow('Contours',cnt)
    center=[0,0]
    (x,y),radius = cv2.minEnclosingCircle(contours[0])
    center=[int(x),int(y)]
    radius=int(radius)
    
   
    #printing RGB values
    #if len(contours) >= 2 then target object is detected
    if (len(contours)>=2):
        file2 = open("contour.txt","w")
        file2.write(str(len(contours)))
        file2.close
        flag=False
        print("Target detected")
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        cnt = cv2.drawContours(cv_image,contours, -1, (0,0,255), 3)
        cv2.imshow("Image_Window",cv_image)
        #pos = rospy.Subscriber("/ground_truth_to_tf/pose",PoseStamped,self.call)
        pos = rospy.Subscriber("/sensor_pose",PoseStamped,self.call)

    else:
      file2 = open("contour.txt","w")
      file2.write(str(0))
      file2.close
    
    
    cv2.waitKey(3)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
