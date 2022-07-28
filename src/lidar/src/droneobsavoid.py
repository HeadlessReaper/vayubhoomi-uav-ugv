#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from std_msgs.msg import String
from lidar.msg import vel
import math as m

dist1=[]
dist2=[]
dist3=[]
dist4=[]

def callback(data):
	
	integ_p = 0
	error_p = 0
	error = 0
	integ = 0

	global msg
	pub = rospy.Publisher('play', vel, queue_size=10)
	msg = vel()

	#msg.linear.z = 2 * abs(error) + 0.5*(error)
	count_r = 0
	count_l = 0
	count_f = 0
	kp = 2.5
	ki = 0.0003
	kd = 0.4

	msg.linear_x = 0.1

	global dist1, dist2, dist3,dist4

	dist1=data.ranges[520:560]
	dist2=data.ranges[:25:]+data.ranges[:-25:-1]
	dist3=data.ranges[160:200]#right
	dist4=data.ranges[880:920]#left


	if((next((True for elem in dist3 if elem <1), False)==False)): 
		count_r+=1
		i=dist3[20]
		error = 1/i
		msg.linear_y = ((kp*error) + (ki*integ) + (kd*der))
		msg.linear_z = 0
	elif((next((True for elem in dist4 if elem <1), False)==False)):  
		count_l+=1
		i=dist4[20]
		error = 1/i
		msg.linear_y = -((kp*error)+(ki*integ)+(kd*der))
		msg.linear_z = 0
	elif((next((True for elem in dist1 if elem <1), False)==False)):
		print('*********************************')
		count_f+=1
		i=dist2[25]
		error = 1/i
		msg.linear_z = 1
	# Obs on three sides
	elif ((next((True for elem in dist3 if elem <1), False)==False) and (next((True for elem in dist2 if elem <1), False)==False (next((True for elem in dist4 if elem <1), False)==False))):
		error=1/(dist2[25]+dist3[25]+dist4[25])
		msg.linear_x = -((kp * error) + (ki * integ) + (kd * der))
		
	# Obs on both sides
	elif ((next((True for elem in dist3 if elem <1), False)==False) and (next((True for elem in dist4 if elem <1), False)==False)):
		msg.linear_x = (kp * error) + (ki * integ) + (kd * der)

	else:
		msg.linear_x = 0
		msg.linear_y = 0
		msg.linear_z = 0

	integ = integ_p + error
	der = error - error_p

	error_p = error
	integ_p = integ

	
	pub.publish(msg)	
		

				
def listener():
	global msg
	global error_p
	global integ_p

	integ_p=0
	error_p=0

	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/quadrotor/scan", LaserScan, callback)
	rospy.spin()
	

if __name__ == '__main__':
	listener()
