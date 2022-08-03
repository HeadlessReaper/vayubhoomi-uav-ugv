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
dist1=[]
dist2=[]
dist3=[]
dist4=[]

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
    
def distCallback(data):
    global dist1,dist2,dist3,dist4

    dist1=data.ranges[520:560]
    dist2=data.ranges[:25:]+data.ranges[:-25:-1]
    dist3=data.ranges[160:200]#right
    dist4=data.ranges[880:920]#left
    #print(" Distance from scan topic : ",dist1,dist2,dist3)

def move(xgoal,ygoal,zgoal):
    global x_p,y_p, z_p
    global dist1,dist2,dist3,distp,yaw,errorp,integ

    count_r = 0
    count_l = 0
    count_f = 0

    vmsg = Twist()
    pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)  

    vmsg.linear.z=1
    pub.publish(vmsg)
    time.sleep(0.8)

    while(True):

        # distance = round(abs(math.sqrt(((xgoal-x_p) ** 2) + ((ygoal-y_p) ** 2)+((zgoal-z_p) ** 2))),2)
        # print(distance)
        # error=distance-distp
        der = error - errorp
        integ= integ+error

        kp=2.5
        ki=0.0003
        kd=0.4
          
        linear_speed = kp*error+ki*integ+(kd*der)

        print('error',error,'Integ : ',ki*integ, 'linear speed',linear_speed)


        # K_angular = 4.0
        # desired_angle_goal = math.atan2(ygoal-y_p, xgoal-x_p)
        # angular_speed = (desired_angle_goal-yaw)*K_angular

        vmsg.linear.x = 0.1
        #vmsg.angular.z = angular_speed

        if((next((True for elem in dist3 if elem <2), False)==False)): 
            count_r+=1
            print(len(dist3))
            i=dist3[20]
            error = 1/i
            vmsg.linear.y = ((kp*error) + (ki*integ) + (kd*der))
            vmsg.linear.z = 0
        elif((next((True for elem in dist4 if elem <2), False)==False)):  
            count_l+=1
            i=dist4[20]
            error = 1/i
            vmsg.linear.y = -((kp*error)+(ki*integ)+(kd*der))
            vmsg.linear.z = 0
        elif((next((True for elem in dist1 if elem <2), False)==False)):
            print('*********************************')
            count_f+=1
            i=dist2[25]
            error = 1/i
            vmsg.linear.z = 1
        # elif ((x_p==xgoal and y_p==ygoal and z_p==zgoal) ):            
        #     vmsg.angular.z = 0
        #     print('*********************************************************')
        #     pub.publish(vmsg)
        #     break
        pub.publish(vmsg)


if __name__ == '__main__':
    try:
        rospy.init_node('drone',anonymous=False)
        velpub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        possub=rospy.Subscriber('ground_truth/state',Odometry,poseCallback)
        distsub=rospy.Subscriber('/scan',LaserScan,distCallback)
        time.sleep(0.5)
        l=[(1,1,2),(1,6,2),(6,6,2),(6,1,2)]
        for i in l:
            move(i[0],i[1],i[2])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")