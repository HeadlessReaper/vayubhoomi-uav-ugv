; Auto-generated. Do not edit!


(cl:in-package distance_msgs-srv)


;//! \htmlinclude conversion-request.msg.html

(cl:defclass <conversion-request> (roslisp-msg-protocol:ros-message)
  ((a
    :reader a
    :initarg :a
    :type cl:integer
    :initform 0))
)

(cl:defclass conversion-request (<conversion-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <conversion-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'conversion-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name distance_msgs-srv:<conversion-request> is deprecated: use distance_msgs-srv:conversion-request instead.")))

(cl:ensure-generic-function 'a-val :lambda-list '(m))
(cl:defmethod a-val ((m <conversion-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader distance_msgs-srv:a-val is deprecated.  Use distance_msgs-srv:a instead.")
  (a m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <conversion-request>) ostream)
  "Serializes a message object of type '<conversion-request>"
  (cl:let* ((signed (cl:slot-value msg 'a)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <conversion-request>) istream)
  "Deserializes a message object of type '<conversion-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'a) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<conversion-request>)))
  "Returns string type for a service object of type '<conversion-request>"
  "distance_msgs/conversionRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'conversion-request)))
  "Returns string type for a service object of type 'conversion-request"
  "distance_msgs/conversionRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<conversion-request>)))
  "Returns md5sum for a message object of type '<conversion-request>"
  "7bda023e35ef66c372a0d64f03917b2f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'conversion-request)))
  "Returns md5sum for a message object of type 'conversion-request"
  "7bda023e35ef66c372a0d64f03917b2f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<conversion-request>)))
  "Returns full string definition for message of type '<conversion-request>"
  (cl:format cl:nil "int32 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'conversion-request)))
  "Returns full string definition for message of type 'conversion-request"
  (cl:format cl:nil "int32 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <conversion-request>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <conversion-request>))
  "Converts a ROS message object to a list"
  (cl:list 'conversion-request
    (cl:cons ':a (a msg))
))
;//! \htmlinclude conversion-response.msg.html

(cl:defclass <conversion-response> (roslisp-msg-protocol:ros-message)
  ((s
    :reader s
    :initarg :s
    :type cl:float
    :initform 0.0)
   (success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass conversion-response (<conversion-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <conversion-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'conversion-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name distance_msgs-srv:<conversion-response> is deprecated: use distance_msgs-srv:conversion-response instead.")))

(cl:ensure-generic-function 's-val :lambda-list '(m))
(cl:defmethod s-val ((m <conversion-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader distance_msgs-srv:s-val is deprecated.  Use distance_msgs-srv:s instead.")
  (s m))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <conversion-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader distance_msgs-srv:success-val is deprecated.  Use distance_msgs-srv:success instead.")
  (success m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <conversion-response>) ostream)
  "Serializes a message object of type '<conversion-response>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 's))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <conversion-response>) istream)
  "Deserializes a message object of type '<conversion-response>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 's) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<conversion-response>)))
  "Returns string type for a service object of type '<conversion-response>"
  "distance_msgs/conversionResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'conversion-response)))
  "Returns string type for a service object of type 'conversion-response"
  "distance_msgs/conversionResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<conversion-response>)))
  "Returns md5sum for a message object of type '<conversion-response>"
  "7bda023e35ef66c372a0d64f03917b2f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'conversion-response)))
  "Returns md5sum for a message object of type 'conversion-response"
  "7bda023e35ef66c372a0d64f03917b2f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<conversion-response>)))
  "Returns full string definition for message of type '<conversion-response>"
  (cl:format cl:nil "float32 s~%bool success~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'conversion-response)))
  "Returns full string definition for message of type 'conversion-response"
  (cl:format cl:nil "float32 s~%bool success~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <conversion-response>))
  (cl:+ 0
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <conversion-response>))
  "Converts a ROS message object to a list"
  (cl:list 'conversion-response
    (cl:cons ':s (s msg))
    (cl:cons ':success (success msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'conversion)))
  'conversion-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'conversion)))
  'conversion-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'conversion)))
  "Returns string type for a service object of type '<conversion>"
  "distance_msgs/conversion")