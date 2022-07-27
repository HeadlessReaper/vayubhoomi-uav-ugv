#!/usr/bin/env python3

from cmath import inf
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math
import time

distp=0
yaw=0
errorp=0
integ=0
x_p=0
y_p=0
z_p=0
dist1=0
dist2=0
dist3=0

def poseCallback(pose_message):
    global x_p
    global y_p, z_p,yaw
    x_p=(pose_message.pose.pose.position.x)
    y_p=(pose_message.pose.pose.position.y)
    z_p=(pose_message.pose.pose.position.z)
    orientation_q = pose_message.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    yaw=round(yaw,2)
    
def distCallback(msg):
    global dist1
    global dist2 , dist3
    dist1=round(msg.ranges[540],2)
    dist2=round(msg.ranges[8],2)
    dist3=round(msg.ranges[1070],2)#backwards
    print(" Distance from scan topic : ",dist1,dist2,dist3)

def move(xgoal,ygoal,zgoal):
    global x_p,y_p, z_p
    global dist1,dist2,dist3,distp,yaw,errorp,integ
    vmsg = Twist()
    pub=rospy.Publisher('/quadrotor/cmd_vel',Twist,queue_size=10)  

    vmsg.linear.z=0.8
    pub.publish(vmsg)
    time.sleep(0.8)

    while(True):
        distance = round(abs(math.sqrt(((xgoal-x_p) ** 2) + ((ygoal-y_p) ** 2)+((zgoal-z_p) ** 2))),2)
        print(distance)
        error=distance-distp
        der = error - errorp
        integ= integ+error

        kp=2
        ki=0
        kd=0
          
        linear_speed = kp*distance+ki*integ+(kd*der)
        print('error',error,'Integ : ',ki*integ, 'linear speed',linear_speed)


        K_angular = 4.0
        desired_angle_goal = math.atan2(ygoal-y_p, xgoal-x_p)
        angular_speed = (desired_angle_goal-yaw)*K_angular

        vmsg.linear.x = linear_speed
        vmsg.angular.z = angular_speed

        if((dist1>0.5 or dist1==inf)):
            pub.publish(vmsg)
            print ('x=', x_p, 'y=',y_p)
            distp=distance
            errorp=error
        elif ((x_p==xgoal and y_p==ygoal and z_p==zgoal) or distance<0.5):            
            vmsg.angular.z = 0
            print('*********************************************************')
            pub.publish(vmsg)
            break
        if(dist1<0.5 ):#or dist2<1.5 or dist3<1.5
            print('********************obstacle seen*****************')
            print('dist :',dist1)
            vmsg.linear.x = -1
            pub.publish(vmsg)
            time.sleep(1)
            vmsg.linear.x = 0
            vmsg.linear.z=0
            pub.publish(vmsg)
            break


if __name__ == '__main__':
    try:
        rospy.init_node('drone',anonymous=False)
        velpub=rospy.Publisher('/quadrotor/cmd_vel',Twist,queue_size=10)
        possub=rospy.Subscriber('ground_truth/state',Odometry,poseCallback)
        distsub=rospy.Subscriber('/quadrotor/scan',LaserScan,distCallback)
        time.sleep(0.5)
        move(4,-5,10)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")