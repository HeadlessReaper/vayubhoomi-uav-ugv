## **_VAYUBHOOMI UAV UGV PIL PROJECT 2022_** 
### Networked autonomous UAV - UGV system for reconnaissance and waste management over open spaces.
#### Approach:
Our approach relies on three main sub-systems :
* **The Unmanned Aerial Vehicle(UAV)** :
     Patrols preset area using :
     * Proportional Integral Derivative(PID) controller
     * records video and pose
     * sends to base station.
* **The base station:**
     * Per frame video feed analysis by Neural net(NN)
     * Neural Networks Detects trash
     * Filters trash positive frames
     * K-means cluster location stored in CSV file.
* **The Unmanned Ground Vehicle(UGV):**
     * Collects cluster location and moves to them;
     * Scans cluster vicinity for accurate trash detection.

#### Frameworks and Languages used: 
* ROS 
* PYTHON
* XML

#### Note:
* Files wrt to simulation is located under [lidar](https://github.com/HeadlessReaper/vayubhoomi-uav-ugv/tree/src/lidar) package.
* Files wrt to trash detection and clustering is present in [vision](https://github.com/HeadlessReaper/vayubhoomi-uav-ugv/tree/main/src/vision) package.

#### Gazebo worlds used for simulation:
![Image 1](resources/default_gzclient_camera(1)-2022-08-05T20_42_03.378549.jpg)
![Image 2](resources/default_gzclient_camera(1)-2022-08-05T20_42_14.778247.jpg)
![Image 3](resources/default_gzclient_camera(1)-2022-08-06T01_00_51.352346.jpg)
**Procedure to launch the simulation:**
- Make sure you have installed models necessary for [trash.world](https://github.com/HeadlessReaper/vayubhoomi-uav-ugv/blob/pramuk/src/lidar/worlds/trash.world) from (https://github.com/osrf/gazebo_models)

- Make sure the .world files are present in worlds folder of your ROS package and all the models must be present in the .gazebo/models folder for the launch file to work.

- Update the following files :

     - droneobsavoid.py

     - botmove.py

     - dronespiral.py

     - UAVpathRecorderNode.py 
          
     
- Command to launch the simulation :
 ```
 roslaunch lidar sample.launch
 ```  
Change `lidar` to the name of your ROS package


