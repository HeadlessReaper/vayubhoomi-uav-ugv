#!/usr/bin/env python3
# license removed for brevity
#publisher sends info via topics.
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('sensorinfo', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():# The string to be published on the topic.
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass



# def talk():
#     talk=rospy.Publisher("talker",String,queue_size=10)
#     rospy.init_node('node_1',anonymous=False)
#     rate=rospy.Rate(10)
#     topic1_content = "my first ROS topic"
#     while not rospy.is_shutdown():
#         talk.publish(topic1_content)
#         rate.sleep()