#!/usr/bin/env python3
from cmath import inf
import math
import rospy
from lidar.msg import distlist
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import time

integ=0
distp=0
errorp=0
dist3=0
dist4=0
dist1=[]
dist2=[]
dist5=[]
dist6=[]

def poseCallback(pose_message):
    global x
    global y, yaw
    orientation_q = pose_message.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    yaw=round(yaw,2)
    x= round(pose_message.pose.pose.position.x,2)
    y= round(pose_message.pose.pose.position.y,2)

def distCallback(msg):
    global dist1,dist2,dist3,dist4,dist5,dist6
    dist1=msg.ranges[8:100]#left 0 to 75
    dist2=msg.ranges[200:350]#right
    dist5=msg.ranges[100:270]
    dist6=msg.ranges[:45:]+msg.ranges[:-45:-1]
    dist3=msg.ranges[10] 
    dist4=msg.ranges[310]

def check(d1,d):
    for elem in d1:
        if elem<=d:
            print('heeeeeeeeellllllllllllllllllllllllllllllloooooooo')
            return True
        else:
            pass

def rotate (angular_speed_degree, relative_angle_degree, clockwise):

    global dist5,dist6,yaw
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

    while ((next((True for elem in dist5 if elem <0.2), False)==False )and (next((True for elem in dist6 if elem <0.2), False)==False )) :
        print("Turtlesim rotates")
        velocity_publisher.publish(vmsg)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()

        print('current_angle_degree: ',current_angle_degree)
                       
        if  (current_angle_degree>relative_angle_degree):
            print('reached')
            break
    else:
        if(check(dist6,0.2)==True):
            print('rotate fn reverse')
            vmsg.linear.x=-0.1
            velocity_publisher.publish(vmsg)
            time.sleep(0.4)
        elif(check(dist5,0.2)==True):
            print('rotate fn forward')
            vmsg.linear.x=0.1
            velocity_publisher.publish(vmsg)
            time.sleep(0.4)

def obscheck():
    
    global dist1,dist2,dist3,dist4,dist5,dist6,integ,errorp

    #rospy.init_node('obsnodes',anonymous=False)
    veltop='/cmd_vel'
    pub=rospy.Publisher(veltop,Twist,queue_size=10)
    postop='/scan'
    possub=rospy.Subscriber(postop,LaserScan,distCallback)
    dissub=rospy.Subscriber('/odom',Odometry,poseCallback)

    velocity_message = Twist()

    #rotate(15,60,False)
    kp =0.1
    ki=0
    kd=0

    error= 0 if dist3==inf else 1/dist3
    der = error - errorp
    integ= 0.67*integ+error
    
    linear_speed = kp*error+ki*integ+(kd*der)
    print('obs error',error,'Integ : ',ki*integ,'der',kd*der, 'linear speed',linear_speed)

    K_angular =4
    desired_angle_goal = math.atan2((y+2)-y, (x+2)-x)
    angular_speed = (desired_angle_goal-yaw)*K_angular

    velocity_message.linear.x = 0.707*linear_speed +0.04
    #velocity_message.angular.z = angular_speed

    if(next((True for elem in dist1 if elem <0.4), False)):
        print('******************** obstacle on left ********************')
        #print('dist1 :',dist1,'dist2 :',dist2,'dist3 :' ,dist3)
        print("linear speed",linear_speed)
        if (next((True for elem in dist1 if elem <0.2), False)):
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

    elif(next((True for elem in dist2 if elem <0.4), False)):
        print('******************** obstacle on right *******************')
        #print('dist :',min(dist1,dist2,dist3))
        print("linear speed",linear_speed)
        if (next((True for elem in dist2 if elem <0.2), False)):
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

        # disttop='/scan'
        time.sleep(1)
        #move(0.2,0.35,True)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")