# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "hector_pose_estimation_core;nodelet;sensor_msgs;geometry_msgs;nav_msgs;tf;message_filters".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lhector_pose_estimation_nodelet;-lhector_pose_estimation_node".split(';') if "-lhector_pose_estimation_nodelet;-lhector_pose_estimation_node" != "" else []
PROJECT_NAME = "hector_pose_estimation"
PROJECT_SPACE_DIR = "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/install"
PROJECT_VERSION = "0.4.0"
