#!/usr/bin/env python3
#Hector to move to a certain height, then move to the corner of pre-defined rectangular patrol area
#traverse the perimeter of the rectangle by moving from corner to corner using a PID controller

import math
from turtle import distance
from numpy import where
import rospy
from time import sleep
from std_msgs.msg import Empty
from nav_msgs.msg import Odometry
import time
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import warnings
from sensor_msgs.msg import LaserScan

x=0
y=0
z=0
yaw=0
distp = 0
integ = 0
heightp=0
errorp=0
derh=0
errorhp=0
integh=0
global height

vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

def poseCallback(pose_message):
    global x
    global y,z,yaw
    orientation_q = pose_message.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    yaw=round(yaw,2)
    x= round(pose_message.pose.pose.position.x,2)
    y= round(pose_message.pose.pose.position.y,2)
    z=round(pose_message.pose.pose.position.z,2)
'''    
def distCallback(msg):
    global dist1
    dist1=msg.ranges[0]
    print(" Distance from scan topic : ",dist1)
    '''

def initMessage(vx,vy,vz,vaz):
    vel_msg = Twist()
    vel_msg.linear.x = float(vx)
    vel_msg.linear.y = float(vy)
    vel_msg.linear.z = float(vz)
    vel_msg.angular.z = float(vaz)
    vel_msg.angular.x = float(0.0)
    vel_msg.angular.y = float(0.0)
    vel_pub.publish(vel_msg)

def up():
    vel_msg = Twist()
    vel_msg.linear.z = float(1.0)
    vel_pub.publish(vel_msg)

def hover():
    initMessage(0.0,0.0,0.0,0.0)

def down():
    vel_msg = Twist()
    vel_msg.linear.z = float(-1.0)
    vel_pub.publish(vel_msg)

def forward():
    vel_msg = Twist()
    vel_msg.linear.x = float(1.0)
    vel_pub.publish(vel_msg)

def backward():
    vel_msg = Twist()
    vel_msg.linear.x = float(-1.0)
    vel_pub.publish(vel_msg)

def right():
    vel_msg = Twist()
    vel_msg.linear.y = float(-1.0)
    vel_pub.publish(vel_msg)

def left():
    vel_msg = Twist()
    vel_msg.linear.y = float(1.0)
    vel_pub.publish(vel_msg)

def cw():
    vel_msg = Twist()
    vel_msg.angular.z = float(-1.0)
    vel_pub.publish(vel_msg)

def ccw():
    vel_msg = Twist()
    vel_msg.angular.z = float(1.0)
    vel_pub.publish(vel_msg)

'''def rectangle(x_goal, y_goal):
    global x
    global y
    global z,yaw
    

    vel_msg = Twist()
    cmd_vel_topic='/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while(True):
        K_linear = 0.1
        distance = round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2)
        linear_speed = distance*K_linear
        vel_msg.linear.x = linear_speed
        vel_pub.publish(vel_msg)

        if (distance <0.01):
            break
'''

def go_to_goal(x_goal, y_goal,z_goal):
    global x, distp , errorp,errorhp,integh,derh,height
    global y, z,yaw

    velocity_message = Twist()
    cmd_vel_topic='/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)   

    #der = error - error_p
    # velocity_message.linear.y = -((kp*error) + (ki*integ) + (kd*der)) 
    distref=round(abs(math.sqrt(((x_goal-0) ** 2) + ((y_goal-0) ** 2))),2)
    while (True):
        global integ,heightp
        
        kp = 0.5
        ki=0.0001
        kd=1.4
        
        Kp_vertical = 1.2
        Ki_vertical = 0.0001
        Kd_vertical = 1.5
        '''
        kp = 0.1
        ki=0.00001
        kd=1.8
        
        Kp_vertical = 10
        Ki_vertical = 0.1
        Kd_vertical = 1
        '''
        if(z_goal<z):

            height = -(round((math.sqrt(((abs(z_goal-z))**2))),2))
            
        elif(z_goal>z):
            height = round((math.sqrt(((abs(z_goal-z))**2))),2)

        distance = round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2)
        #if(x_goal<x and y_goal<y):
         #   distance = -(round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2))

        #elif(x_goal>x and y_goal<y):
          #  distance = -(round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2))
            
        #elif(x_goal>x and y_goal>y):
           # distance = round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2)
        error=distance-distp        
        der = error - errorp
        integ= integ+error

        errorh=height-heightp
        integh=integh+errorh
        derh=errorh-errorhp
        
        vertical_speed = height*Kp_vertical+derh*Kd_vertical+integh*Ki_vertical
        #c=op(distance)
        linear_speed = kp*distance+ki*integ+(kd*der)
        


        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        # if(desired_angle_goal-yaw>180):
        #     desired_angle_goal = -180-(yaw)
        if((desired_angle_goal-yaw)>3.14159):
            desired_angle_goal = desired_angle_goal-(2*3.14159)
        if((desired_angle_goal-yaw)<-3.14159):
            desired_angle_goal=desired_angle_goal+(2*3.14159) 
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.linear.z = vertical_speed
        velocity_message.angular.z = angular_speed
        #velocity_message.linear.z = vertical_speed
        print('errorh',errorh,'Integ : ',integh, "derh :",derh, 'linear speed',linear_speed,"angular_speed",angular_speed,"yaw",yaw)
        if(velocity_message.angular.z>0.01):
             velocity_message.linear.x=0
             velocity_message.linear.y=0
             velocity_message.linear.z=0

        if ((x==x_goal and y==y_goal and z==z_goal) or ((0.98*x_goal<=x<=1.02*x_goal) and (0.98*y_goal<=y<=1.02*y_goal)and (0.98*z_goal<z<=1.02*z_goal)) ):
            print("***********************************")
            velocity_message.linear.x = 0
            velocity_message.linear.y=0
            velocity_message.linear.z=0
            velocity_message.angular.z=0
            pub.publish(velocity_message)
            time.sleep(1)
            break
        else:
            pub.publish(velocity_message)
            print ('x=', x, 'y=',y,"z=",z)
            heightp=height
            distp=distance
            errorp=error
            errorhp=errorh
        '''
        elif(distance<0.5):
            print('********************obstacle seen*****************')
            print('dist :',distance)
            velocity_message.linear.x = -2
            pub.publish(velocity_message)
            time.sleep(0.5)
            go_to_goal(5,2)
        '''

if __name__=='__main__':
    try:
        rospy.init_node('autohector',anonymous=True)
        veltop='/cmd_vel'
        velpub=rospy.Publisher(veltop,Twist,queue_size=10)
        postop='/ground_truth/state'
        possub=rospy.Subscriber(postop,Odometry,poseCallback)
        disttop ='/scan'
        #distsub=rospy.Subscriber(disttop,LaserScan,distCallback)
        time.sleep(1)
        up()
        sleep(2)
        hover()
        #move(0.2,0.35,True)
        l=[(1,2,1),(1,6,1),(6,6,1),(6,2,1),(1,2,1)]
        for (i,j,k) in l:
            go_to_goal(i,j,k)
            print("next stop")
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")




