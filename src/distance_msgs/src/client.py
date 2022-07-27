#!/usr/bin/env python3

import rospy
from distance_msgs.srv import conversion, conversionRequest, conversionResponse

def multiplier_client(x):
    # First wait for the service to become available.
    rospy.loginfo("Waiting for service...")
    rospy.wait_for_service('multiserver')
    try:
        # Create a service proxy.
        multiserver = rospy.ServiceProxy('multiserver', conversion)

        # Call the service here.
        service_response = multiserver(x)

        print("I only got here AFTER the service call was completed!")

        # Return the response to the calling function.
        return service_response

    except rospy.ServiceException as e:
        print("Service call failed: %s", e)


if __name__ == "__main__":

    # Initialize the client ROS node.
    rospy.init_node("client", anonymous=False)

    # The distance to be converted to feet.
    dist_metres = 2
    s="Requesting conversion of "+str(dist_metres)+" to multiplier of 100"
    rospy.loginfo(s)

    # Call the service client function.
    service_response = multiplier_client(dist_metres)

    # Process the service response and display log messages accordingly.
    if(not service_response.success):
        rospy.logerr("Conversion unsuccessful! Requested distance in metres should be a positive real number.")
    else:
        rospy.loginfo("%4.2f *100 = %4.2f "%(dist_metres, service_response.s))
        rospy.loginfo("Conversion successful!")