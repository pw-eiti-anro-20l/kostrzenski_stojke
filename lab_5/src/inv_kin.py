#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header


def handle_inversion(data):

    x = data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z

    if x > 1.0 or x < 0.0 or y > 0.0 or y < -1.0 or z < 0.0 or z > 1.0:
    	rospy.logerr('Incorrect position - x: ' + str(x) + ', y: ' + str(y) + ', z: ' + str(z))
    	return

    joint_state = JointState()
    joint_state.header = Header()
    joint_state.header.stamp = rospy.Time.now()
    joint_state.name = ['i_1', 'i_2', 'i_3']
    joint_state.position = [z-1, -y-1, x-1]

    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    pub.publish(joint_state)


if __name__ == "__main__":
    rospy.init_node('ikin', anonymous=True)
    rospy.Subscriber('oint', PoseStamped, handle_inversion)
    rospy.spin()
