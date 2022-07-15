#!/usr/bin/env python3
import rospy
from distance_msgs.srv import conversion, conversionRequest, conversionResponse

def servicereq(objreq):
    objres=conversionResponse()
    
    if(objreq.a < 0):
        objres.success=False
        objres.s=0
    else:
        objres.success=True
        objres.s=objreq.a*100

    return objres

def multiplier():
    rospy.init_node('server',anonymous=False)
    rospy.Service('multiserver',conversion,servicereq)
        # Log message about service availability.
    rospy.loginfo('Multiplier now available.')
    rospy.spin()


if __name__ == "__main__":
    multiplier()