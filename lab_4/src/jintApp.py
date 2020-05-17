#!/usr/bin/env python


import rospy
from lab_4.srv import Jint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math

freq = 50 
flag = 0 

start = [0, 0, 0]
def interpolate(jMsg):
	if(jMsg.j1>1 or jMsg.j2>1 or jMsg.j3>1):
		return False
	global start
	end = [jMsg.j1, jMsg.j2, jMsg.j3]
	change = start
	step=[(end[0]-start[0])/(freq*jMsg.time), (end[1]-start[1])/(freq*jMsg.time), (end[2]-start[2])/(freq*jMsg.time)]
	for k in range(0, int(freq*jMsg.time)+1):
		for i in range(0, 3):
			change[i]=change[i] + step[i]
		pose_str = JointState()
		pose_str.header.stamp = rospy.Time.now()
		pose_str.name = ['base_i1', 'i1_i2', 'i2_i3']
		pose_str.position = [change[0], change[1], change[2]]
		publisher.publish(pose_str)
		rate.sleep()
	curr_time = 0
	start = end
	return True

if __name__ == "__main__":
	rospy.init_node('int_srv')
	rate = rospy.Rate(50)
	publisher = rospy.Publisher('joint_states',JointState, queue_size=10)
	s = rospy.Service('int', Jint, interpolate)
	rospy.spin()
