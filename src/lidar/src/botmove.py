#!/usr/bin/env python3

from cmath import inf
import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import time
#from simple_pid import PID

x=0
y=0
dist1=0
yaw=0
integ=0
distp=0
errorp=0

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
    global dist1
    dist1=msg.ranges[0]
    print(" Distance from scan topic : ",dist1)

def move(speed,dist,is_forward):
    velocity_message = Twist()
    #get current location 
    global x, y
    # x0=x
    # y0=y

    if (is_forward):
        velocity_message.linear.x =abs(speed)
    else:
        velocity_message.linear.x =-abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10)  
    cmd_vel_topic='/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)

    while True :
        print("turtlebot moves forwards")
        if(x<5):
            pub.publish(velocity_message)
            print ('x=', x, 'y=',y)
            loop_rate.sleep()
        else:
            rospy.loginfo("obstacle seen.")
            break

                       
                
        #distance_moved = abs(0.5 * math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
        #rospy.loginfo(distance_moved)               
        # if  (distance_moved==dist):
            
    velocity_message.linear.x =0
    pub.publish(velocity_message)


def rotate (angular_speed_degree, relative_angle_degree, clockwise):
    
    velocity_message = Twist()
    velocity_message.linear.x=0
    velocity_message.linear.y=0
    velocity_message.linear.z=0
    velocity_message.angular.x=0
    velocity_message.angular.y=0
    velocity_message.angular.z=0

    angular_speed=math.radians(abs(angular_speed_degree))

    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed)

    angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/cmd_vel_mux/input/teleop'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True :
        rospy.loginfo("Turtlesim rotates")
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()

        print('current_angle_degree: ',current_angle_degree)
                       
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break

    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)

def go_to_goal(x_goal, y_goal):

    global x,distp,errorp
    global y, yaw

    velocity_message = Twist()
    cmd_vel_topic='/cmd_vel'
    pub=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)   

    #der = error - error_p
    # velocity_message.linear.y = -((kp*error) + (ki*integ) + (kd*der)) 
    distref=round(abs(math.sqrt(((x_goal-0) ** 2) + ((y_goal-0) ** 2))),2)
    while (True):
        global integ
        kp = 0.2
        ki=0.001
        kd=2

        distance = round(abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2))),2)
        error=distance-distp
        der = error - errorp
        integ= integ+error
        
        #c=op(distance)
        linear_speed = kp*distance+ki*integ+(kd*der)
        print('error',error,'Integ : ',ki*integ, 'linear speed',linear_speed)


        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        if(dist1>0.5 or dist1==inf):
            pub.publish(velocity_message)
            print ('x=', x, 'y=',y)
            distp=distance
            errorp=error
        elif ((x==x_goal and y==y_goal) or distance<0.1):
            velocity_message.linear.x = 0
            pub.publish(velocity_message)
            break
        elif(dist1<0.5):
            print('********************obstacle seen*****************')
            print('dist :',dist1)
            velocity_message.linear.x = -2
            pub.publish(velocity_message)
            time.sleep(0.5)
            go_to_goal(5,2)

            


        
if __name__ == '__main__':
    try:
        rospy.init_node('rabbitposer',anonymous=True)
        veltop='/cmd_vel'
        velpub=rospy.Publisher(veltop,Twist,queue_size=10)
        postop='/odom'
        possub=rospy.Subscriber(postop,Odometry,poseCallback)
        #rospy.init_node('scannode',anonymous=True)
        disttop='/scan'
        distsub=rospy.Subscriber(disttop,LaserScan,distCallback)
        time.sleep(1)
        #move(0.2,0.35,True)
        l=[(2,3)]
        for (i,j) in l:
            go_to_goal(i,j)
            print("next stop")
            time.sleep(2)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")