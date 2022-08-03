#!/usr/bin/env python3
#Hector to move to a certain height, then move to the corner of pre-defined rectangular patrol area
#traverse the perimeter of the rectangle by moving from corner to corner using a PID controller

import math
import rospy
from time import sleep
from lidar.msg import vel
from nav_msgs.msg import Odometry
import time
from numpy import *
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from sensor_msgs.msg import LaserScan

x=0
y=0
z=0
yaw=0
distp = 0
integ = 0
heightp=0
errorp=0.
derh=0
errorhp=0
integh=0
ctr=0
global height

vel_pub = rospy.Publisher('/quadrotor/cmd_vel', Twist, queue_size=1)

def clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif upper is not None and value > upper:
        return upper
    elif lower is not None and value < lower:
        return lower
    return value

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

def call_obs(data_obs):
    global ctr
    print('in call obs function')
    vmsg=Twist()
    pub = rospy.Publisher('/quadrotor/cmd_vel', Twist, queue_size=10)
    # If it receives non-zero velocities, an obstacle is present
    if data_obs.linear_x == 0.0 and data_obs.linear_y == 0.0 and data_obs.linear_z == 0.0:
        #print('obs linearx 0')
        pass

    else:
        ctr=ctr+1
        print('obs true',data_obs.linear_x,data_obs.linear_y,data_obs.linear_z)
        vmsg.linear.x = data_obs.linear_x
        vmsg.linear.y = data_obs.linear_y
        vmsg.linear.z = data_obs.linear_z
        pub.publish(vmsg)
        

def go_to_goal(x_goal, y_goal,z_goal):
    global x, distp , errorp,errorhp,integh,derh,height,ctr
    global y, z,yaw

    velocity_message = Twist()
    cmd_vel_topic='/quadrotor/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)
    print('gotogoal function') 
    obssub=rospy.Subscriber('/play',vel,call_obs)
    print('after call_obs function') 
    #der = error - error_p
    # velocity_message.linear.y = -((kp*error) + (ki*integ) + (kd*der)) 
    #distref=round(abs(math.sqrt(((x_goal-0) * 2) + ((y_goal-0) * 2))),2)
    while (True):        
        
        global integ,heightp
        '''
        kp = 0.5
        ki=0.0001
        kd=1.4
        '''
        
        Kp_vertical = 1.2
        Ki_vertical = 0.0001
        Kd_vertical = 1.5
        
        kp = 0.21
        ki=0.00001
        kd=1.15

        '''
        Kp_vertical = 10
        Ki_vertical = 0.1
        Kd_vertical = 1
        '''
        if(z_goal<z):

            height = -(round((math.sqrt(((z_goal-z))**2)),2))
            
        elif(z_goal>z):
            height = round((math.sqrt(((z_goal-z))**2)),2)

        distance = round(abs(math.sqrt(((x_goal-x)** 2) + ((y_goal-y)** 2))),2)
        #if(x_goal<x and y_goal<y):
         #   distance = -(round(abs(math.sqrt(((x_goal-x) * 2) + ((y_goal-y) * 2))),2))

        #elif(x_goal>x and y_goal<y):
          #  distance = -(round(abs(math.sqrt(((x_goal-x) * 2) + ((y_goal-y) * 2))),2))
            
        #elif(x_goal>x and y_goal>y):
           # distance = round(abs(math.sqrt(((x_goal-x) * 2) + ((y_goal-y) * 2))),2)
        error=distance-distp        
        der = error - errorp
        integ= integ+error

        errorh=height-heightp
        integh=integh+errorh
        derh=errorh-errorhp
        
        vertical_speed = height*Kp_vertical+derh*Kd_vertical+integh*Ki_vertical
        linear_speed = kp*distance+ki*integ+(kd*der)
        

        K_angular = 3
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
        #print('errorh',errorh,'Integ : ',integh, "derh :",derh, 'linear speed',linear_speed,"angular_speed",angular_speed,"yaw",yaw)
        
        # if(velocity_message.angular.z>0.01):
        #      velocity_message.linear.x=0
        #      velocity_message.linear.y=0
        #      velocity_message.linear.z=0

        if ((x==x_goal and y==y_goal and z==z_goal) or ((0.98*x_goal<=x<=1.02*x_goal) and (0.98*y_goal<=y<=1.02*y_goal)and (0.98*z_goal<z<=1.02*z_goal)) ):
            print("*************")
            ctr=0
            velocity_message.linear.x = 0
            velocity_message.linear.y=0
            velocity_message.linear.z=0
            velocity_message.angular.z=0
            pub.publish(velocity_message)
            #time.sleep(0.25)
            break
        else:
            if ctr>2000:
                ctr=0
                break
            else:
                pub.publish(velocity_message)
                #print ('x=', x, 'y=',y,"z=",z)
                heightp=height
                distp=distance
                errorp=error
                errorhp=errorh
        '''
        elif(distance<0.5):
            print('*******obstacle seen******')
            print('dist :',distance)
            velocity_message.linear.x = -2
            pub.publish(velocity_message)
            time.sleep(0.5)
            go_to_goal(5,2)
        '''

def receiver():
    rospy.init_node('autohector',anonymous=True)
    veltop='/quadrotor/cmd_vel'
    velpub=rospy.Publisher(veltop,Twist,queue_size=10)
    postop='/quadrotor/ground_truth/state'
    possub=rospy.Subscriber(postop,Odometry,poseCallback)
    

    vel_msg = Twist()
    vel_msg.linear.z = float(1.0)
    velpub.publish(vel_msg)

    hover()
        
    k=2

    r = linspace(0,30,40)
    t = linspace(0,2000,40)
    for x,y in zip(r,t):
        i = x*cos(radians(y))
        j = x*sin(radians(y))
        i1=clamp(i,[-30,30])
        j1=clamp(j,[-30,18])
        go_to_goal(round(i1,1),round(j1,1),k)
        print('*********************************************************************')
        #sleep(0.5)

    rospy.spin()


if __name__ == '__main__':
    receiver()

        #go_to_goal(x,y,k)
        # for g in range(-6,6,1):
        #     for h in range(1,5):
        #         if h%2==1:
        #             if h%3==0:
        #                 j=j-g+2
        #                 print(i,j,h)
        #                 go_to_goal(i,j,k)
        #             else:
        #                 j=j+g-1
        #                 print(i,j,h)
        #                 go_to_goal(i,j,k)
        #         elif h%2==0:
        #             if h%4==0:
        #                 i=i-g+2
        #                 print(i,j,h)
        #                 go_to_goal(i,j,k)
        #             else:
        #                 i=i+g-1
        #                 print(i,j,h)
        #                 go_to_goal(i,j,k)

            

    # except rospy.ROSInterruptException:
    #     rospy.loginfo("node terminated.")