#!/usr/bin/env python

__author__ =  'Paul Duckworth <scpd at leeds.ac.uk>'
__version__=  '0.1'

import rospy
import sys
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

VERBOSE=False

class generate_QSR:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        self.qsr_pub = rospy.Publisher("/socialCardReader/QSR_generator", String, queue_size=10)

        # subscribed Topic
        self.Subscriber = rospy.Subscriber("/socialCardReader/cardposition", PoseStamped, self.callback,  queue_size = 1)

        if VERBOSE :
            print "subscribed to /socialCardReader/cardposition"


    def callback(self, position):

        if VERBOSE :
            rospy.loginfo("Card position (x,y,z): [ %f, %f, %f ]"%(position.pose.position.x, position.pose.position.y, position.pose.position.z))

	if position != []:
            distance = np.sqrt((position.pose.position.x)**2 + (position.pose.position.y)**2 + (position.pose.position.z)**2)
            result = 'far' if distance > 2 else 'near'

            if VERBOSE :
              rospy.loginfo("the card is %s" %result)

        # Publish qsr
        self.qsr_pub.publish(result)

def main(args):

    '''Initializes and cleanup ros node'''
    qsr = generate_QSR()
    rospy.init_node('QSR_generator', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS QSR generator module"

if __name__ == '__main__':
    main(sys.argv)
