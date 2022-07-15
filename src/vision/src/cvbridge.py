# this node takes an input stream from the camera feed and records the ground location of the drone in areas with detected targets

import sys
import cv2
import rospy
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

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
    file = open('positions.csv', 'a')
    file.write(str(location.pose.position.x) + ',' + str(location.pose.position.y) + '\n')
    file.close()

def imageCallback(ros_image):

    global bridge

    try:
        img = bridge.imgmsg_to_cv2(ros_image, "bgr8")
    except CvBridgeError as e:
            print(e)

    ##############################################################
    # from this point on, 'img' is the target of processing
    ##############################################################
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

    # currently, the target being detected is a coke can
    # replace this subsection with bounding box classifier to detect trash at a later stage
    hMin, sMin, vMin, hMax, sMax, vMax =  147 , 52 , 0 , 179 , 248 , 214
    lower = np.array([hMin, sMin, vMin])  # minimum range array
    upper = np.array([hMax, sMax, vMax])  # maximum range array
    mask = cv2.inRange(imgHSV, lower, upper)

    kernel = np.ones((5,5), np.uint8)
    dilate = cv2.dilate(mask, kernel, iterations=1)

    imgResult = img

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # image, retrieval method (here, for outermost contours), approximation 
    x, y, w, h = 0, 0, 0, 0

    for cnt in contours : # contours - array of contours detected in image

        area = cv2.contourArea(cnt) # finds area of selected contour
        # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0),3)  # image copy, selected contour, (-1 to draw all contours), color, thickness
        perimeter = cv2.arcLength(cnt, True) # contour, is closed(?)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True) # contour, resolution, is closed(?)
        x, y, w, h = cv2.boundingRect(cnt) # coordinates of each shape
        cv2.rectangle(imgResult, (x,y), (x+w, y+h), (0, 255, 0), 2) # bounding rectangle (green for each detected shape)

        # subsection to call a function to save the quadrotor pose 
        pos = rospy.Subscriber("/ground_truth_to_tf/pose", PoseStamped, poseRecordCallback)
        
    # imgStacked = stackImages(0.5, ([img, dilate, imgResult]))
    cv2.imshow("Image", imgResult)
    ##############################################################
    cv2.waitKey(3)

  
def main(args):

    rospy.init_node('vision', anonymous=True)

    # file initialization
    file = open('positions.csv', 'a')
    file.write('x,y\n')
    file.close()

    #`for turtlebot3 waffle
    #`image_topic="/camera/rgb/image_raw/compressed"
    #`for usb cam
    #`image_topic = "/usb_cam/image_raw"
    #`for hector quadrotor
    imageTopic = "/front_cam/camera/image"

    image_sub = rospy.Subscriber(imageTopic,Image, imageCallback)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

    cv2.destroyAllWindows()

if __name__ == '__main__':

    main(sys.argv)