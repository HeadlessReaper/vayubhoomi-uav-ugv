# this node takes an input stream from the camera feed and records the ground location of the drone in areas with detected targets

import sys
import cv2
import math
import rospy
import tf as transform
from sklearn.cluster import KMeans
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge, CvBridgeError

import time
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image as pilimage
from matplotlib import pyplot as plt
from tensorflow.python.util import compat
from tensorflow.core.protobuf import saved_model_pb2
from google.protobuf import text_format
import pprint
import json
import os
from object_detection.utils import visualization_utils as vis_util
from sklearn.cluster import KMeans
from object_detection.utils import label_map_util, dataset_util
from object_detection.protos import string_int_label_map_pb2

bridge = CvBridge()

# model initializations
def reconstruct(pb_path):
    if not os.path.isfile(pb_path):
        print("Error: %s not found" % pb_path)

    print("Reconstructing Tensorflow model")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(pb_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    print("Success!")
    return detection_graph

# visualize detection
def image2np(image):
    (w, h) = image.size
    return np.array(image.getdata()).reshape((h, w, 3)).astype(np.uint8)

def image2tensor(image):
    npim = image2np(image)
    return np.expand_dims(npim, axis=0)

def detect(detection_graph, test_image_path):
    with detection_graph.as_default():
        gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.01)
        with tf.compat.v1.Session(graph=detection_graph,config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)) as sess:
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            image = pilimage.open(test_image_path)
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image2tensor(image)}
            )

            npim = image2np(image)
            vis_util.visualize_boxes_and_labels_on_image_array(
                npim,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=15)

            return npim, int(num)

NCLASSES = 60
with open('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/dataset/data/annotations.json') as json_file:
    data = json.load(json_file)
    
categories = data['categories']

print('Building label map from examples')

labelmap = string_int_label_map_pb2.StringIntLabelMap()
for idx,category in enumerate(categories):
    item = labelmap.item.add()
    # label map id 0 is reserved for the background label
    item.id = int(category['id'])+1
    item.name = category['name']

with open('./labelmap.pbtxt', 'w') as f:
    f.write(text_format.MessageToString(labelmap))

print('Label map witten to labelmap.pbtxt')

with open('./labelmap.pbtxt') as f:
    pprint.pprint(f.readlines())

label_map = label_map_util.load_labelmap('labelmap.pbtxt')
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NCLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = reconstruct("/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/trained-models/ssd_mobilenet_v2_taco_2018_03_29.pb")

# node code starts here

curTime = time.time() # initializing the starting time
fps = 0 # initializing the frame rate variable

frameNumber = 0
numObj = 0
def poseRecordCallback(location) :

    global frameNumber
    global numObj

    # quaternion transformation to get yaw angle 
    quaternion = (location.pose.pose.orientation.x, location.pose.pose.orientation.y, location.pose.pose.orientation.z, location.pose.pose.orientation.w)
    euler = transform.transformations.euler_from_quaternion(quaternion)
    yaw = math.degrees(euler[2])

    file = open('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/UGVTargetAngles.csv', 'a')
    file.write(str(frameNumber) + ',' + str(yaw) + ',' + str(numObj) + '\n')
    file.close()

def imageCallback(ros_image):

    global bridge
    global curTime
    global fps
    global frameNumber
    global numObj

    try:
        img = bridge.imgmsg_to_cv2(ros_image, "bgr8")
    except CvBridgeError as e:
            print(e)

    ##############################################################
    # from this point on, 'img' is the target of processing
    ##############################################################
    height, width, channels = img.shape
    if height > width:
        cv2.resize(img, (1357, 2049))
    else:
        cv2.resize(img, (2049, 1357))

    cv2.imwrite('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/image.jpg', img)

    img, numObj = detect(detection_graph, '/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/image.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    cv2.putText(img, '{0:.2f}'.format(fps), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)
        
    if fps != 0:
        cv2.putText(img, '{0:.2f}'.format((1 / fps) * 1000), (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)
    else:
        pass

    if numObj > 0:
        # subsection to conditionally call a function to save the turtlebot3 pose 
        pos = rospy.Subscriber("/odom", Odometry, poseRecordCallback)

    cv2.putText(img, '{0:d}'.format(numObj), (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, '{0:d}'.format(frameNumber), (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)


    frameNumber += 1
    cv2.imshow("feed", img)
    ##############################################################
    fps = 1 / (time.time() - curTime)
    curTime = time.time()
    cv2.waitKey(1)

  
def main(args):

    global frameNumber

    rospy.init_node('UGVVision', anonymous=True)

    #`for turtlebot3 waffle
    # image_topic="/camera/rgb/image_raw"
    # for usb cam
    # image_topic = "/usb_cam/image_raw"
    # for hector quadrotor
    # imageTopic = "/front_cam/camera/image"

    image_topic="/camera/rgb/image_raw"
    image_sub = rospy.Subscriber(image_topic,Image, imageCallback)

    file = open('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/UGVTargetAngles.csv', 'w')
    file.write('frameNumber,angle,numObj\n')
    file.close()

    print("Press ctrl + c to trigger a KeyboardInterrupt.")

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down.")

    cv2.destroyAllWindows()

    print("\nPre-processing data ...")
    df = pd.read_csv('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/UGVTargetAngles.csv')
    df = df[df['numObj'] != '0'] # dropping angles with 0 objects detected
    df = df.drop_duplicates(subset=['frameNumber'], keep='first') # eliminating duplicates
    df.sort_values(by=['numObj'], inplace = True, ascending=False) # sort in descending to imply priority
    df.to_csv('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/UGVTargetAngles.csv', index=False)
    print("\nData pre-processing complete.")

    print("\nShutdown complete.")

if __name__ == '__main__':

    main(sys.argv)