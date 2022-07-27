; Auto-generated. Do not edit!


(cl:in-package distance_msgs-msg)


;//! \htmlinclude dist_info.msg.html

(cl:defclass <dist_info> (roslisp-msg-protocol:ros-message)
  ((dist
    :reader dist
    :initarg :dist
    :type sensor_msgs-msg:Range
    :initform (cl:make-instance 'sensor_msgs-msg:Range))
   (mno
    :reader mno
    :initarg :mno
    :type cl:integer
    :initform 0)
   (mname
    :reader mname
    :initarg :mname
    :type cl:string
    :initform ""))
)

(cl:defclass dist_info (<dist_info>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <dist_info>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'dist_info)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name distance_msgs-msg:<dist_info> is deprecated: use distance_msgs-msg:dist_info instead.")))

(cl:ensure-generic-function 'dist-val :lambda-list '(m))
(cl:defmethod dist-val ((m <dist_info>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader distance_msgs-msg:dist-val is deprecated.  Use distance_msgs-msg:dist instead.")
  (dist m))

(cl:ensure-generic-function 'mno-val :lambda-list '(m))
(cl:defmethod mno-val ((m <dist_info>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader distance_msgs-msg:mno-val is deprecated.  Use distance_msgs-msg:mno instead.")
  (mno m))

(cl:ensure-generic-function 'mname-val :lambda-list '(m))
(cl:defmethod mname-val ((m <dist_info>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader distance_msgs-msg:mname-val is deprecated.  Use distance_msgs-msg:mname instead.")
  (mname m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <dist_info>) ostream)
  "Serializes a message object of type '<dist_info>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'dist) ostream)
  (cl:let* ((signed (cl:slot-value msg 'mno)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'mname))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'mname))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <dist_info>) istream)
  "Deserializes a message object of type '<dist_info>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'dist) istream)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mno) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mname) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'mname) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<dist_info>)))
  "Returns string type for a message object of type '<dist_info>"
  "distance_msgs/dist_info")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'dist_info)))
  "Returns string type for a message object of type 'dist_info"
  "distance_msgs/dist_info")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<dist_info>)))
  "Returns md5sum for a message object of type '<dist_info>"
  "9437189fa374886e3521594bcfcd5828")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'dist_info)))
  "Returns md5sum for a message object of type 'dist_info"
  "9437189fa374886e3521594bcfcd5828")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<dist_info>)))
  "Returns full string definition for message of type '<dist_info>"
  (cl:format cl:nil "sensor_msgs/Range dist~%int32 mno~%string mname~%================================================================================~%MSG: sensor_msgs/Range~%# Single range reading from an active ranger that emits energy and reports~%# one range reading that is valid along an arc at the distance measured. ~%# This message is  not appropriate for laser scanners. See the LaserScan~%# message if you are working with a laser scanner.~%~%# This message also can represent a fixed-distance (binary) ranger.  This~%# sensor will have min_range===max_range===distance of detection.~%# These sensors follow REP 117 and will output -Inf if the object is detected~%# and +Inf if the object is outside of the detection range.~%~%Header header           # timestamp in the header is the time the ranger~%                        # returned the distance reading~%~%# Radiation type enums~%# If you want a value added to this list, send an email to the ros-users list~%uint8 ULTRASOUND=0~%uint8 INFRARED=1~%~%uint8 radiation_type    # the type of radiation used by the sensor~%                        # (sound, IR, etc) [enum]~%~%float32 field_of_view   # the size of the arc that the distance reading is~%                        # valid for [rad]~%                        # the object causing the range reading may have~%                        # been anywhere within -field_of_view/2 and~%                        # field_of_view/2 at the measured range. ~%                        # 0 angle corresponds to the x-axis of the sensor.~%~%float32 min_range       # minimum range value [m]~%float32 max_range       # maximum range value [m]~%                        # Fixed distance rangers require min_range==max_range~%~%float32 range           # range data [m]~%                        # (Note: values < range_min or > range_max~%                        # should be discarded)~%                        # Fixed distance rangers only output -Inf or +Inf.~%                        # -Inf represents a detection within fixed distance.~%                        # (Detection too close to the sensor to quantify)~%                        # +Inf represents no detection within the fixed distance.~%                        # (Object out of range)~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'dist_info)))
  "Returns full string definition for message of type 'dist_info"
  (cl:format cl:nil "sensor_msgs/Range dist~%int32 mno~%string mname~%================================================================================~%MSG: sensor_msgs/Range~%# Single range reading from an active ranger that emits energy and reports~%# one range reading that is valid along an arc at the distance measured. ~%# This message is  not appropriate for laser scanners. See the LaserScan~%# message if you are working with a laser scanner.~%~%# This message also can represent a fixed-distance (binary) ranger.  This~%# sensor will have min_range===max_range===distance of detection.~%# These sensors follow REP 117 and will output -Inf if the object is detected~%# and +Inf if the object is outside of the detection range.~%~%Header header           # timestamp in the header is the time the ranger~%                        # returned the distance reading~%~%# Radiation type enums~%# If you want a value added to this list, send an email to the ros-users list~%uint8 ULTRASOUND=0~%uint8 INFRARED=1~%~%uint8 radiation_type    # the type of radiation used by the sensor~%                        # (sound, IR, etc) [enum]~%~%float32 field_of_view   # the size of the arc that the distance reading is~%                        # valid for [rad]~%                        # the object causing the range reading may have~%                        # been anywhere within -field_of_view/2 and~%                        # field_of_view/2 at the measured range. ~%                        # 0 angle corresponds to the x-axis of the sensor.~%~%float32 min_range       # minimum range value [m]~%float32 max_range       # maximum range value [m]~%                        # Fixed distance rangers require min_range==max_range~%~%float32 range           # range data [m]~%                        # (Note: values < range_min or > range_max~%                        # should be discarded)~%                        # Fixed distance rangers only output -Inf or +Inf.~%                        # -Inf represents a detection within fixed distance.~%                        # (Detection too close to the sensor to quantify)~%                        # +Inf represents no detection within the fixed distance.~%                        # (Object out of range)~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <dist_info>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'dist))
     4
     4 (cl:length (cl:slot-value msg 'mname))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <dist_info>))
  "Converts a ROS message object to a list"
  (cl:list 'dist_info
    (cl:cons ':dist (dist msg))
    (cl:cons ':mno (mno msg))
    (cl:cons ':mname (mname msg))
))
