#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from std_msgs.msg import String
from lidar.msg import vel
import math as m
import time

dist1=[]
dist2=[]
dist3=[]
dist4=[]

def callback(data):
	global dist1, dist2, dist3,dist4

	dist1=data.ranges[500:560] #forward
	dist4=data.ranges[150:320]#left
	dist3=data.ranges[800:950]#right

	error_p = 0
	error = 0
	integ = 0

	msg = vel()
	#vmsg=Twist()
	pub=rospy.Publisher('/play',vel,queue_size=10)
	# vpub=rospy.Publisher('/quadrotor/cmd_vel',Twist,queue_size=10)   

	# msg.linear_z=1
	# pub.publish(msg)
	# time.sleep(0.8)

	count_r = 0
	count_l = 0
	count_f = 0

	kp = 2.8
	ki = 0.0003
	kd = 0.4

	msg.linear_x = 0
	msg.linear_y = 0
	msg.linear_z = 0

	integ = integ + error
	der = error - error_p


	#Obs on three sides
	if ((next((True for elem in dist3 if elem <2), False)==True) and (next((True for elem in dist1 if elem <2), False)==True and (next((True for elem in dist4 if elem <2), False)==True))):
		print('ons on three sides')
		error=3/(dist1[25]+dist3[25]+dist4[25])
		msg.linear_x = -((kp * error) + (ki * integ) + (kd * der))
		pub.publish(msg)
		
	# Obs on both sides
	elif ((next((True for elem in dist3 if elem <2), False)==True) and (next((True for elem in dist4 if elem <2), False)==True)):
		print('obs on 2 sides')
		error=2/(dist3[25]+dist4[25])
		msg.linear_x = (kp * error) + (ki * integ) + (kd * der)
		pub.publish(msg)
	
	elif((next((True for elem in dist3 if elem <2), False)==True)):
		print('right') 
		#print(len(dist3))
		i=dist3[20]
		error = 1/i
		msg.linear_y = ((kp*error) + (ki*integ) + (kd*der))
		msg.linear_z = 0
		pub.publish(msg)
		# vmsg.linear.y=msg.linear_y
		# vmsg.linear.z=msg.linear_z
	elif((next((True for elem in dist4 if elem <2), False)==True)):
		print('left')  
		i=dist4[20]
		error = 1/i
		msg.linear_y = -((kp*error)+(ki*integ)+(kd*der))
		msg.linear_z = 0
		pub.publish(msg)
		# vmsg.linear.y=msg.linear_y
		# vmsg.linear.z=msg.linear_z
		
	elif((next((True for elem in dist1 if elem <2), False)==True)):
		print('front')
		print('*********************************')
		i=dist1[25]
		error = 1/i
		msg.linear_y = ((kp*error) + (ki*integ) + (kd*der))		
		msg.linear_z = 0
		pub.publish(msg)
		# vmsg.linear.y=msg.linear_y
		# vmsg.linear.z=msg.linear_z

	else:
		print('no obs')
		msg.linear_x = 0
		msg.linear_y = 0
		msg.linear_z = 0
		pub.publish(msg)
		# vmsg.linear.y=msg.linear_y
		# vmsg.linear.z=msg.linear_z


	error_p = error
		# integ_p = integ

		
	#pub.publish(msg)
	# vpub.publish(vmsg)	

if __name__ == '__main__':
	try:
		rospy.init_node('listener',anonymous=True)
		vel_pub=rospy.Publisher('/play',vel,queue_size=10)
		distsub=rospy.Subscriber('/quadrotor/scan',LaserScan,callback)
		# l=[(1,1,2),(1,6,2),(6,6,2),(6,1,2)]
		# for i in l:
		# 	move(i[0],i[1],i[2])
		rospy.spin()

	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated.")