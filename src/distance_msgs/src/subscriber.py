#!/usr/bin/env python3
import rospy
from distance_msgs.msg import dist_info

def chatter_callback(message):
    #get_caller_id(): Get fully resolved name of local node
    rospy.loginfo("I heard %s from %s", message.dist.range,message.mname)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('node_2', anonymous=True)

    rospy.Subscriber("talk", dist_info, chatter_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()