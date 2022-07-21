#!/usr/bin/env python3

from cmath import inf
import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from obsavoidance import obscheck
import time

x=0
y=0
yaw=0
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
    
    print(x,y)

def distCallback(msg):
    global dist1,dist2,dist3,dist4,dist5,dist6
    dist1=msg.ranges[8:100]#left 0 to 75
    dist2=msg.ranges[200:350]#right
    dist5=msg.ranges[100:270]
    dist6=msg.ranges[:45:]+msg.ranges[:-45:-1]
    dist3=msg.ranges[10] 
    dist4=msg.ranges[310]
    #print(" Distance from scan topic : ",dist1)

def go_to_goal(x_goal, y_goal):

    global x,distp,errorp
    global y, yaw

    velocity_message = Twist()
    cmd_vel_topic='/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)   

    slope=y_goal/x_goal
    global integ,dist2,dist3

    while (True):

        kp =0.8
        ki=0.00004
        kd=1.3

        distance = round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2)
        distyex=round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-(slope*x)) ** 2))),2)
        #distyex-distance
        error=(abs((-slope * x +y)) / (math.sqrt(slope**2 + 1))) if (dist3==inf or dist4==inf) else (0.5-min(dist3,dist4))
        der = error - errorp
        integ= 0.67*integ+error
        
        #c=op(distance)
        linear_speed = kp*distance+ki*integ+(kd*der)
        print('error',error,'Integ : ',ki*integ,'der',kd*der, 'linear speed',linear_speed)
 
        K_angular =4
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = 0.707*linear_speed
        velocity_message.angular.z = angular_speed

        if ((x==x_goal and y==y_goal) or (0.95*x_goal<=x<=1.1*x_goal and 0.95*y_goal<=y<=1.1*y_goal)):
            velocity_message.linear.x = 0
            velocity_message.angular.z = 0
            print('*********************************************************')
            pub.publish(velocity_message)
            break
        elif(obscheck(dist1,dist2,dist3,dist5,dist6,x,y,yaw)==False):
            pass
        else:
            pub.publish(velocity_message)
            print ('x=', x, 'y=',y)
            distp= min(dist4,dist3) if (dist3!=inf or dist4!=inf ) else distance
            errorp=error



if __name__ == '__main__':
    try:
        rospy.init_node('botnode',anonymous=False)
        veltop='/cmd_vel'
        velpub=rospy.Publisher(veltop,Twist,queue_size=10)
        postop='/odom'
        possub=rospy.Subscriber(postop,Odometry,poseCallback)
        disttop='/scan'
        distsub=rospy.Subscriber(disttop,LaserScan,distCallback)
        time.sleep(1)
        #move(0.2,0.35,True)
        l=[(1.2,1.2)]
        for (i,j) in l:
            go_to_goal(i,j)
            print("next stop")
            time.sleep(1)
            
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")