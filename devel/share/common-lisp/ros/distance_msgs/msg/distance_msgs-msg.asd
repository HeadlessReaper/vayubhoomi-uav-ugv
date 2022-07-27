
(cl:in-package :asdf)

(defsystem "distance_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
)
  :components ((:file "_package")
    (:file "dist_info" :depends-on ("_package_dist_info"))
    (:file "_package_dist_info" :depends-on ("_package"))
  ))