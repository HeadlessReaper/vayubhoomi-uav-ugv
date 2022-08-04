'''
from object_detection.utils import label_map_util, dataset_util
from object_detection.protos import string_int_label_map_pb2
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt
from tensorflow.python.util import compat
from tensorflow.core.protobuf import saved_model_pb2
from google.protobuf import text_format
import pprint
import json
import os
import cv2
from object_detection.utils import visualization_utils as vis_util
from sklearn.cluster import KMeans


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

            image = Image.open(test_image_path)
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
            return int(num)

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

def recordPoint(x, y):
     # currently focusing on appending to text file, although a pandas dataframe will be a more appropriate data structure for collecting recon data
    file = open('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/poi.csv', 'a')
    file.write(str(x) + ',' + str(y) + '\n')
    file.close()

# running a video and collecting all the points of interest 

# FPS initializations
import time
curTime = time.time() # initializing the starting time
fps = 0 # initializing the frame rate variable
  
# This will return video from the first webcam on your computer.
cap = cv2.VideoCapture('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/video.mp4')  
frameNumber = 0

# point of interest file initialization
file = open('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/poi.csv', 'a')
file.write('x,y\n')
file.close()

# initializing the positions dataframe and dropping duplicate poses before saving again
df = pd.read_csv('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/positions.csv')
df = df.drop_duplicates(subset=['frameNumber'], keep='first')
df.to_csv('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/positions.csv', index=False)
df = pd.read_csv('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/positions.csv')

# loop runs if capturing has been initialized. 
while(True):

    # reads frames from a camera 
    # ret checks return at each frame
    ret, frame = cap.read() 

    # kill if no frame detected
    if not ret:
        break

    # conditional resizing based on the frame dimensions to minimize dataloss
    height, width, channels = frame.shape
    if height > width:
        cv2.resize(frame, (1357, 2049))
    else:
        cv2.resize(frame, (2049, 1357))

    cv2.imwrite('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/image.jpg', frame)
      
    frameNumber += 1
    index = frameNumber - 1

    # detecting the number of objects
    numObjs = detect(detection_graph, '/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/image.jpg')
    # numObjs -= 1
    
    print("Frame number : ", frameNumber)
    print("Number of objects detected : ", numObjs)
    print("FPS : ", fps)

    if numObjs > 0 and index < len(df['frameNumber']):
        recordPoint(df['x'][index], df['y'][index])
  
    # FPS calculation
    fps = 1 / (time.time() - curTime)
    curTime = time.time()

    cv2.imshow('Frame', frame)
    cv2.waitKey(1) 
  
# Close the window / Release webcam
cap.release()
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()
'''
import pandas as pd
from sklearn.cluster import KMeans

# importing poi.csv
dataset = pd.read_csv('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/poi.csv')
X = pd.DataFrame(dataset)
X = X.to_numpy(dtype ='float32')

# setting the thresholds for clustering
numClusters = 5
print('Number of clusters = ', numClusters)

# clustering
kmeans = KMeans(n_clusters = numClusters, init = 'k-means++', random_state = 42)
y_kmeans = kmeans.fit_predict(X)

# saving centroids in a new CSV file
centroidDataframe = pd.DataFrame(kmeans.cluster_centers_)
centroidDataframe.columns = ['x', 'y']
centroidDataframe.to_csv('/home/sr42/catkin_ws/src/vayubhoomi-uav-ugv/src/vision/src/wasteTensorflow/centroids.csv', index=False)


