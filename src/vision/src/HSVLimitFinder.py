# HSV limit finding from rostopic 
# not in a working state at the moment

import sys
import cv2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def empty(a):  # argument required
    pass

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

bridge = CvBridge()

def imageCallback(rosImage) :

    global bridge

    try :

        img = bridge.imgmsg_to_cv2(rosImage, 'bgr8')

    except CvBridgeError as e :

        print(e)

    ##############################################################
    # from this point on, 'img' is the target of processing
    ##############################################################

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hMin = cv2.getTrackbarPos('H minimum', 'Trackbars')
    hMax = cv2.getTrackbarPos('H maximum', 'Trackbars')
    sMin = cv2.getTrackbarPos('S minimum', 'Trackbars')
    sMax = cv2.getTrackbarPos('S maximum', 'Trackbars')
    vMin = cv2.getTrackbarPos('V minimum', 'Trackbars')
    vMax = cv2.getTrackbarPos('V maximum', 'Trackbars')

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    mask = cv2.inRange(imgHSV, lower, upper)

    imgStacked = stackImages(0.5, ([img, mask]))
    cv2.imshow('Feed', imgStacked)
    ##############################################################

    cv2.waitKey(3)

def main(args):

    rospy.init_node('HSVLimitFinder', anonymous=True)

    #`for turtlebot3 waffle
    #`image_topic="/camera/rgb/image_raw/compressed"
    #`for usb cam
    #`image_topic = "/usb_cam/image_raw"
    #`for hector quadrotor
    imageTopic = "/front_cam/camera/image"

    image_sub = rospy.Subscriber(imageTopic,Image, imageCallback)

    try :
        
        rospy.spin()
    
    except KeyboardInterrupt :
        
        print("Shutting down")

    print()
    print('Required values : ')
    print('hMin, sMin, vMin, hMax, sMax, vMax = ', hMin, ',', sMin, ',', vMin, ',', hMax, ',', sMax, ',', vMax)
    cv2.destroyAllWindows()

if __name__ == '__main__' :

    cv2.namedWindow('Trackbars')  # Creating trackbars to isolate required color
    cv2.resizeWindow('Trackbars', 640, 240)
    cv2.createTrackbar('H minimum', 'Trackbars', 0, 179, empty) # 180 hues available in opencv (lower and upper limits for trackbars), empty is a function called each time the trackbar is changed
    cv2.createTrackbar('H maximum', 'Trackbars', 179, 179, empty) # initial trackbars for color detection and limit identification
    cv2.createTrackbar('S minimum', 'Trackbars', 0, 255, empty)
    cv2.createTrackbar('S maximum', 'Trackbars', 255, 255, empty)
    cv2.createTrackbar('V minimum', 'Trackbars', 0, 255, empty)
    cv2.createTrackbar('V maximum', 'Trackbars', 255, 255, empty)

    main(sys.argv)
