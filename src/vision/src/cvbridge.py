'''
import cv2

while True :

    img = cv2.imread('test-image.jpg')

    cv2.imshow('Image', img)

    if cv2.waitKey(0) == ord('q'):
        break
'''

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys

bridge = CvBridge()

def image_callback(ros_image):

  print('Image obtained.')
  global bridge

  # convert ros_image into an opencv-compatible image

  try:
    cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
    print(e)

  # from this point on, cv_image is the target of processing
  
  cv2.imshow("Image", cv_image)

  #cv2.waitKey(3)
  if (cv2.waitKey(1) == ord('q')):
        break

  
def main(args):

  rospy.init_node('vision', anonymous=True)

  #`for turtlebot3 waffle
  #`image_topic="/camera/rgb/image_raw/compressed"
  #`for usb cam
  #`image_topic = "/usb_cam/image_raw"
  #`for hector quadrotor
  image_topic = "/front_cam/camera/image"
  image_sub = rospy.Subscriber(image_topic,Image, image_callback)

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

  cv2.destroyAllWindows()

if __name__ == '__main__':

    main(sys.argv)