#!/usr/bin/env python3
from cmath import inf
import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import time

integ=0
distp=0
errorp=0

def check(d1,d):
    for elem in d1:
        if elem<=d:
            print('heeeeeeeeellllllllllllllllllllllllllllllloooooooo')
            return True
        else:
            print('Nooooooooooooooooooooo')
            return False

def rotate (angular_speed_degree, relative_angle_degree, clockwise,dist6,dist5,yaw):

    vmsg = Twist()
    vmsg.linear.x=0
    vmsg.linear.y=0
    vmsg.linear.z=0
    vmsg.angular.x=0
    vmsg.angular.y=0
    vmsg.angular.z=yaw

    angular_speed=math.radians(abs(angular_speed_degree))

    if (clockwise):
        vmsg.angular.z =-abs(angular_speed)
    else:
        vmsg.angular.z =abs(angular_speed)

    angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=5)

    t0 = rospy.Time.now().to_sec()

    while (check(dist5,0.25)==False) :
        print("Turtlesim rotates")
        velocity_publisher.publish(vmsg)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()

        print('current_angle_degree: ',current_angle_degree)
                       
        if  (current_angle_degree>relative_angle_degree):
            print('reached')
            break

    if(check(dist6,0.2)==True):
        print('rotate fn reverse')
        vmsg.linear.x=-0.1
        velocity_publisher.publish(vmsg)
        time.sleep(0.4)
    elif(check(dist5,0.25)==True):
        print('rotate fn forward')
        vmsg.linear.x=0.1
        velocity_publisher.publish(vmsg)
        time.sleep(0.4)

def obscheck(dist1,dist2,dist3,dist5,dist6,x,y,yaw):
    
    global integ,errorp

    velocity_message = Twist()
    cmd_vel_topic='/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)   
         
    #rotate(15,60,False)
    kp =0.2
    ki=0
    kd=0

    error=1/dist3
    der = error - errorp
    integ= 0.67*integ+error
    
    linear_speed = kp*error+ki*integ+(kd*der)
    print('obs error',error,'Integ : ',ki*integ,'der',kd*der, 'linear speed',linear_speed)

    K_angular =4
    desired_angle_goal = math.atan2((y+2)-y, (x+2)-x)
    angular_speed = (desired_angle_goal-yaw)*K_angular

    velocity_message.linear.x = 0.707*linear_speed +0.04
    #velocity_message.angular.z = angular_speed

    if(next((True for elem in dist1 if elem <0.5), False)):
        print('******************** obstacle on left ********************')
        #print('dist1 :',dist1,'dist2 :',dist2,'dist3 :' ,dist3)
        print("linear speed",linear_speed)
        if (next((True for elem in dist1 if elem <0.25), False)):
            velocity_message.linear.x=-0.65
            pub.publish(velocity_message) 
            time.sleep(0.5)
            rotate(10,40,True,dist6,dist5,yaw)
            return False
        else:
            rotate(10,40,True,dist6,dist5,yaw)
            velocity_message.linear.x =0.707*linear_speed
            #velocity_message.angular.z = -angular_speed
            pub.publish(velocity_message)
            time.sleep(0.5)
            return False

    elif(next((True for elem in dist2 if elem <0.5), False)):
        print('******************** obstacle on right *******************')
        #print('dist :',min(dist1,dist2,dist3))
        print("linear speed",linear_speed)
        if (next((True for elem in dist2 if elem <0.25), False)):
            velocity_message.linear.x=-0.65
            pub.publish(velocity_message)
            time.sleep(0.5)
            rotate(10,40,False,dist6,dist5,yaw)
            return False
        else:
            rotate(10,40,False,dist6,dist5,yaw)
            velocity_message.linear.x = 0.707*linear_speed
            #velocity_message.angular.z = angular_speed
            pub.publish(velocity_message)
            time.sleep(0.5)
            return False
    else:
        return True
        
if __name__ == '__main__':
    try:
        rospy.init_node('obsnode',anonymous=True)
        veltop='/cmd_vel'
        velpub=rospy.Publisher(veltop,Twist,queue_size=10)
        # postop='/odom'
        # possub=rospy.Subscriber(postop,Odometry,poseCallback)
        # disttop='/scan'
        # distsub=rospy.Subscriber(disttop,LaserScan,distCallback)
        time.sleep(1)
        #move(0.2,0.35,True)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")