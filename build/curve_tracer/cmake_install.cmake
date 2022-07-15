# Install script for directory: /home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/src/curve_tracer

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/build/curve_tracer/catkin_generated/installspace/curve_tracer.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/curve_tracer/cmake" TYPE FILE FILES
    "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/build/curve_tracer/catkin_generated/installspace/curve_tracerConfig.cmake"
    "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/build/curve_tracer/catkin_generated/installspace/curve_tracerConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/curve_tracer" TYPE FILE FILES "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/src/curve_tracer/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/etc/catkin/profile.d" TYPE FILE FILES "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/src/curve_tracer/env_hooks/curve_tracer_gazebo.bash")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/curve_tracer/catkin_env_hook" TYPE FILE FILES "/home/pramuk/Desktop/UAV-UGV/vayubhoomi-uav-ugv/catkin_ws/src/curve_tracer/env_hooks/curve_tracer_gazebo.bash")
endif()

