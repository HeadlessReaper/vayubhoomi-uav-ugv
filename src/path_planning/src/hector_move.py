#!/usr/bin/env python
from ftplib import error_perm
from rosdep2 import RosdepInternalError
import rospy
import math
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import time
import warnings
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range
from std_msgs.msg import String

x=0
y=0
z=0
yaw=0
 
def poseCallback(pose_message):
    global x
    global y, yaw
    orientation_q = pose_message.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    yaw=round(yaw,2)
    x= round(pose_message.pose.pose.position.x,2)
    y= round(pose_message.pose.pose.position.y,2)
    z= round(pose_message.pose.pose.position.z,2)

    print(x,y,z)

def go_to_goal(x_goal, y_goal, z_goal):
    global x
    global y
    global z, yaw
    global distp, errorp 

    velocity_message = Twist()
    pub=rospy.Publisher('cmd_vel', Twist, queue_size = 10 )
    distref=round(abs(math.sqrt(((x_goal-0) ** 2) + ((y_goal-0) ** 2))),2)
    
    while (True):
        global integ
        kh=0.2
        kp=0.2
        ki=0.001
        kd=2

        distance = round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2)
        error = distance - distp
        der = error-errorp 
        integ= integ+error
        linear_speed = kp*distance+ki*integ+(kd*der)
        print('error', error, 'Integ: ',ki*integ, 'linear speed',linear_speed) 
        height = round(abs(math.sqrt(((z_goal-z)**2))))
        vertical_speed = kh*height

        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x= linear_speed
        velocity_message.angular.z= angular_speed
        
        