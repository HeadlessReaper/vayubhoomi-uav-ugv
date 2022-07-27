;; Auto-generated. Do not edit!


(when (boundp 'distance_msgs::conversion)
  (if (not (find-package "DISTANCE_MSGS"))
    (make-package "DISTANCE_MSGS"))
  (shadow 'conversion (find-package "DISTANCE_MSGS")))
(unless (find-package "DISTANCE_MSGS::CONVERSION")
  (make-package "DISTANCE_MSGS::CONVERSION"))
(unless (find-package "DISTANCE_MSGS::CONVERSIONREQUEST")
  (make-package "DISTANCE_MSGS::CONVERSIONREQUEST"))
(unless (find-package "DISTANCE_MSGS::CONVERSIONRESPONSE")
  (make-package "DISTANCE_MSGS::CONVERSIONRESPONSE"))

(in-package "ROS")





(defclass distance_msgs::conversionRequest
  :super ros::object
  :slots (_a ))

(defmethod distance_msgs::conversionRequest
  (:init
   (&key
    ((:a __a) 0)
    )
   (send-super :init)
   (setq _a (round __a))
   self)
  (:a
   (&optional __a)
   (if __a (setq _a __a)) _a)
  (:serialization-length
   ()
   (+
    ;; int32 _a
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _a
       (write-long _a s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _a
     (setq _a (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass distance_msgs::conversionResponse
  :super ros::object
  :slots (_s _success ))

(defmethod distance_msgs::conversionResponse
  (:init
   (&key
    ((:s __s) 0.0)
    ((:success __success) nil)
    )
   (send-super :init)
   (setq _s (float __s))
   (setq _success __success)
   self)
  (:s
   (&optional __s)
   (if __s (setq _s __s)) _s)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:serialization-length
   ()
   (+
    ;; float32 _s
    4
    ;; bool _success
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _s
       (sys::poke _s (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _s
     (setq _s (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass distance_msgs::conversion
  :super ros::object
  :slots ())

(setf (get distance_msgs::conversion :md5sum-) "7bda023e35ef66c372a0d64f03917b2f")
(setf (get distance_msgs::conversion :datatype-) "distance_msgs/conversion")
(setf (get distance_msgs::conversion :request) distance_msgs::conversionRequest)
(setf (get distance_msgs::conversion :response) distance_msgs::conversionResponse)

(defmethod distance_msgs::conversionRequest
  (:response () (instance distance_msgs::conversionResponse :init)))

(setf (get distance_msgs::conversionRequest :md5sum-) "7bda023e35ef66c372a0d64f03917b2f")
(setf (get distance_msgs::conversionRequest :datatype-) "distance_msgs/conversionRequest")
(setf (get distance_msgs::conversionRequest :definition-)
      "int32 a
---
float32 s
bool success
")

(setf (get distance_msgs::conversionResponse :md5sum-) "7bda023e35ef66c372a0d64f03917b2f")
(setf (get distance_msgs::conversionResponse :datatype-) "distance_msgs/conversionResponse")
(setf (get distance_msgs::conversionResponse :definition-)
      "int32 a
---
float32 s
bool success
")



(provide :distance_msgs/conversion "7bda023e35ef66c372a0d64f03917b2f")


