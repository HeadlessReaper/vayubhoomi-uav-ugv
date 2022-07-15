#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time

x=0
y=0
yaw=0
 
def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.pose.pose.position.x
    y= pose_message.pose.pose.position.y
    #yaw = pose_message.theta


def move(speed,dist,is_forward):
    velocity_message = Twist()
    #get current location 
    global x, y
    x0=x
    y0=y

    if (is_forward):
        velocity_message.linear.x =abs(speed)
    else:
        velocity_message.linear.x =-abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10)  
    cmd_vel_topic='/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)

    while True :
        rospy.loginfo("Turtlesim moves forwards")
        pub.publish(velocity_message)

        loop_rate.sleep()               
                
        distance_moved = abs(0.5 * math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
        print(distance_moved)               
        if  not (distance_moved<dist):
            rospy.loginfo("reached")
            break
    velocity_message.linear.x =0
    pub.publish(velocity_message)

if __name__ == '__main__':
    try:
        rospy.init_node('rabbitposer',anonymous=True)
        veltop='/cmd_vel'
        velpub=rospy.Publisher(veltop,Twist,queue_size=10)
        postop='/odom'
        possub=rospy.Subscriber(postop,Odometry,poseCallback)
        time.sleep(2)
        move(1,2,True)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")