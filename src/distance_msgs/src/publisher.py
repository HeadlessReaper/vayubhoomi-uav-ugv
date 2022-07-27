#!/usr/bin/env python3
import rospy
from distance_msgs.msg import dist_info

def talker():
    pub=rospy.Publisher('talk',dist_info,queue_size=10)
    rospy.init_node('node_1', anonymous=True)
    rate=rospy.Rate(10)
    dist=dist_info()
    dist.dist.header.stamp=rospy.Time.now()
    dist.mname="HC-05"
    dist.mno=123
    dist.dist.range=10

    while not rospy.is_shutdown():
        s="Distance : "+str(dist.dist.range)
        rospy.loginfo(s)
        # rospy.loginfo(dist.)
        pub.publish(dist)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass