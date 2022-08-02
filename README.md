## **_VAYUBHOOMI UAV UGV PIL PROJECT 2022_** 
* ROS 
* PYTHON
* XML
#### Note: All files are located under src/lidar/...

**Procedure to launch the simulation:**
1. Make sure you have installed models necessary for [trash.world](https://github.com/HeadlessReaper/vayubhoomi-uav-ugv/blob/pramuk/src/lidar/worlds/trash.world) from (https://github.com/osrf/gazebo_models)
2. Make sure the .world files are present in worlds folder of your ROS package and all the models must be present in the .gazebo/models folder for the launch file to work. 
3. Update the following files :
     > droneobsavoid.py 
     > 
     > botmove.py
     > 
     > dronespiral.py
 4. Command to launch the simulation :
`roslaunch lidar sample.launch` . 
Change lidar to the name of your ROS package


