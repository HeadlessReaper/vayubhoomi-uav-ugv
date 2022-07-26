# this node takes an input stream from the camera feed and records the ground location of the drone in areas with detected targets

import sys
import cv2
import rospy
import numpy as np
import pandas as pd
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/video.mp4', fourcc, 20.0, (640, 480))
frameNumber = 0

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def poseRecordCallback(location) :

    # currently focusing on appending to text file, although a pandas dataframe will be a more appropriate data structure for collecting recon data
    file = open('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/positions.csv', 'a')
    file.write(str(frameNumber) + ',' + str(location.pose.position.x) + ',' + str(location.pose.position.y) + '\n')
    file.close()

def imageCallback(ros_image):

    global bridge
    global frameNumber
    global out

    try:
        img = bridge.imgmsg_to_cv2(ros_image, "bgr8")
    except CvBridgeError as e:
            print(e)

    ##############################################################
    # from this point on, 'img' is the target of processing
    ##############################################################

    # writing the frame to the video object
    out.write(img) 
    
    # updating the frame number
    frameNumber += 1

    # subsection to call a function to save the quadrotor pose 
    pos = rospy.Subscriber("/ground_truth_to_tf/pose", PoseStamped, poseRecordCallback)
        
    # imgStacked = stackImages(0.5, ([img, dilate, imgResult]))
    cv2.imshow("Image", img)
    ##############################################################
    cv2.waitKey(1)

  
def main(args):

    global out
    global frameNumber

    rospy.init_node('vision', anonymous=True)

    # file initialization
    file = open('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/positions.csv', 'a')
    file.write('frameNumber,x,y\n')
    file.close()

    #`for turtlebot3 waffle
    #`image_topic="/camera/rgb/image_raw/compressed"
    #`for usb cam
    #`image_topic = "/usb_cam/image_raw"
    #`for hector quadrotor
    imageTopic = "/front_cam/camera/image"

    image_sub = rospy.Subscriber(imageTopic,Image, imageCallback)

    print("Press ctrl + c to trigger a KeyboardInterrupt.")

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down.")

    out.release() 
    cv2.destroyAllWindows()
    print("Shutdown complete.")
    print(frameNumber)

if __name__ == '__main__':

    main(sys.argv)