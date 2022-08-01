#!/usr/bin/env python3

from cmath import inf
import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler
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
    dist1=msg.ranges[0:100]#left 0 to 75
    dist2=msg.ranges[200:350]#right
    dist5=msg.ranges[100:270]
    dist6=msg.ranges[:50:]+msg.ranges[:-50:-1]
    dist3=msg.ranges[10] 
    dist4=msg.ranges[310]
    #print(" Distance from scan topic : ",dist1)

def check(d1,d):
    ctr=0
    for elem in d1:
        if elem<=d:
            print('heeeeeeeeellllllllllllllllllllllllllllllloooooooo')
            return True
        else:
            pass

def rotate (angular_speed_degree, relative_angle_degree, clockwise):
    global dist1,dist2,dist5,dist6,yaw
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
    cmd_vel_topic='/turtlebot/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=5)

    t0 = rospy.Time.now().to_sec()

    while ((next((True for elem in dist5 if elem <0.3), False)==False)and (next((True for elem in dist6 if elem <0.3), False)==False )) :
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
        print("**********False************")
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

def go_to_goal(x_goal, y_goal):

    global x,distp,errorp
    global y, yaw

    velocity_message = Twist()
    cmd_vel_topic='/turtlebot/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)   

    slope=y_goal/x_goal

    while (True):
        global integ,dist2,dist3
        kp =0.15
        ki=0.000004
        kd=1.3

        distance = round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2)
        # distyex=round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-(slope*x)) ** 2))),2)
        # #distyex-distance

        error=(abs((-slope * x +y)) / (math.sqrt(slope**2 + 1))) if (dist3==inf or dist4==inf) else (0.5-min(dist3,dist4))
        der = error - errorp
        integ= 0.67*integ+error
        
        #c=op(distance)
        linear_speed = kp*distance+ki*integ+(kd*der)
        print('error',error,'Integ : ',ki*integ,'der',kd*der, 'linear speed',linear_speed)
 
        K_angular =3
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = 0.707*linear_speed
        velocity_message.angular.z = angular_speed

        if ((x==x_goal and y==y_goal) or (0.98*x_goal<=x<=1.05*x_goal and 0.98*y_goal<=y<=1.05*y_goal)):
            velocity_message.linear.x = 0
            velocity_message.angular.z = 0
            print('*********************************************************')
            pub.publish(velocity_message)
            break

        elif(next((True for elem in dist1 if elem <0.7), False)):
            print('******************** obstacle on left ********************')
            #print('dist1 :',dist1,'dist2 :',dist2,'dist3 :' ,dist3)
            print("linear speed",linear_speed)
            if (next((True for elem in dist1 if elem <0.4), False)):
                print('less than 0.4')
                velocity_message.linear.x=-0.65
                pub.publish(velocity_message) 
                time.sleep(0.4)
                rotate(10,40,True)
                errorp=error
            else:
                print('less than 0.7')
                rotate(10,40,True)
                velocity_message.linear.x =0.707*linear_speed
                #velocity_message.angular.z = -angular_speed
                pub.publish(velocity_message)
                time.sleep(0.4)
                errorp=error

        elif(next((True for elem in dist2 if elem <0.7), False)):
            print('******************** obstacle on right *******************')
            #print('dist :',min(dist1,dist2,dist3))
            print("linear speed",linear_speed)
            if (next((True for elem in dist2 if elem <0.4), False)):
                velocity_message.linear.x=-0.65
                pub.publish(velocity_message)
                time.sleep(0.4)
                rotate(10,40,False)
                errorp=error
            else:
                rotate(10,40,False)
                velocity_message.linear.x = 0.707*linear_speed
                #velocity_message.angular.z = angular_speed
                pub.publish(velocity_message)
                time.sleep(0.4)
                errorp=error

        else:
            pub.publish(velocity_message)
            print ('x=', x, 'y=',y)
            distp= min(dist4,dist3) if (dist3!=inf or dist4!=inf ) else distance
            errorp=error
        
if __name__ == '__main__':
    try:
        rospy.init_node('rabbitposer',anonymous=False)
        veltop='/turtlebot/cmd_vel'
        velpub=rospy.Publisher(veltop,Twist,queue_size=10)
        postop='/turtlebot/odom'
        possub=rospy.Subscriber(postop,Odometry,poseCallback)
        disttop='/turtlebot/scan'
        distsub=rospy.Subscriber(disttop,LaserScan,distCallback)
        time.sleep(1)
        #move(0.2,0.35,True)
        l=[(-1.75,7),(-2,-5.5)]
        for (i,j) in l:
            go_to_goal(i,j)
            print("next stop")
            time.sleep(1)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")