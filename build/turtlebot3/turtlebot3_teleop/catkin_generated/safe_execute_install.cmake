execute_process(COMMAND "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/build/turtlebot3/turtlebot3_teleop/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/build/turtlebot3/turtlebot3_teleop/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
