;; Auto-generated. Do not edit!


(when (boundp 'distance_msgs::dist_info)
  (if (not (find-package "DISTANCE_MSGS"))
    (make-package "DISTANCE_MSGS"))
  (shadow 'dist_info (find-package "DISTANCE_MSGS")))
(unless (find-package "DISTANCE_MSGS::DIST_INFO")
  (make-package "DISTANCE_MSGS::DIST_INFO"))

(in-package "ROS")
;;//! \htmlinclude dist_info.msg.html
(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))


(defclass distance_msgs::dist_info
  :super ros::object
  :slots (_dist _mno _mname ))

(defmethod distance_msgs::dist_info
  (:init
   (&key
    ((:dist __dist) (instance sensor_msgs::Range :init))
    ((:mno __mno) 0)
    ((:mname __mname) "")
    )
   (send-super :init)
   (setq _dist __dist)
   (setq _mno (round __mno))
   (setq _mname (string __mname))
   self)
  (:dist
   (&rest __dist)
   (if (keywordp (car __dist))
       (send* _dist __dist)
     (progn
       (if __dist (setq _dist (car __dist)))
       _dist)))
  (:mno
   (&optional __mno)
   (if __mno (setq _mno __mno)) _mno)
  (:mname
   (&optional __mname)
   (if __mname (setq _mname __mname)) _mname)
  (:serialization-length
   ()
   (+
    ;; sensor_msgs/Range _dist
    (send _dist :serialization-length)
    ;; int32 _mno
    4
    ;; string _mname
    4 (length _mname)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; sensor_msgs/Range _dist
       (send _dist :serialize s)
     ;; int32 _mno
       (write-long _mno s)
     ;; string _mname
       (write-long (length _mname) s) (princ _mname s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; sensor_msgs/Range _dist
     (send _dist :deserialize buf ptr-) (incf ptr- (send _dist :serialization-length))
   ;; int32 _mno
     (setq _mno (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _mname
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _mname (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get distance_msgs::dist_info :md5sum-) "9437189fa374886e3521594bcfcd5828")
(setf (get distance_msgs::dist_info :datatype-) "distance_msgs/dist_info")
(setf (get distance_msgs::dist_info :definition-)
      "sensor_msgs/Range dist
int32 mno
string mname
================================================================================
MSG: sensor_msgs/Range
# Single range reading from an active ranger that emits energy and reports
# one range reading that is valid along an arc at the distance measured. 
# This message is  not appropriate for laser scanners. See the LaserScan
# message if you are working with a laser scanner.

# This message also can represent a fixed-distance (binary) ranger.  This
# sensor will have min_range===max_range===distance of detection.
# These sensors follow REP 117 and will output -Inf if the object is detected
# and +Inf if the object is outside of the detection range.

Header header           # timestamp in the header is the time the ranger
                        # returned the distance reading

# Radiation type enums
# If you want a value added to this list, send an email to the ros-users list
uint8 ULTRASOUND=0
uint8 INFRARED=1

uint8 radiation_type    # the type of radiation used by the sensor
                        # (sound, IR, etc) [enum]

float32 field_of_view   # the size of the arc that the distance reading is
                        # valid for [rad]
                        # the object causing the range reading may have
                        # been anywhere within -field_of_view/2 and
                        # field_of_view/2 at the measured range. 
                        # 0 angle corresponds to the x-axis of the sensor.

float32 min_range       # minimum range value [m]
float32 max_range       # maximum range value [m]
                        # Fixed distance rangers require min_range==max_range

float32 range           # range data [m]
                        # (Note: values < range_min or > range_max
                        # should be discarded)
                        # Fixed distance rangers only output -Inf or +Inf.
                        # -Inf represents a detection within fixed distance.
                        # (Detection too close to the sensor to quantify)
                        # +Inf represents no detection within the fixed distance.
                        # (Object out of range)
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :distance_msgs/dist_info "9437189fa374886e3521594bcfcd5828")


