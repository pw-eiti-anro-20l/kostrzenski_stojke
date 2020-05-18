#!/usr/bin/env python


import rospy
from lab_4.srv import Jint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
import math

freq = 50 
path = Path()

start = [0, 0, 0]
def interpol(jReq):
	if(jReq.j1>1 or jReq.j2>1 or jReq.j3>1):
		return False
	global start
	curr_time = 0.
	end = [jReq.j1, jReq.j2, jReq.j3]
	change = start



	for k in range(0, int(freq*jReq.time)+1):
		for i in range(0, 3):
			change[i]=inter(change[i],end[i],jReq.time,curr_time,jReq.iflin)
		pose_str = JointState()
		pose_str.header = Header()
		pose_str.header.stamp = rospy.Time.now()
		pose_str.name = ['i_1', 'i_2', 'i_3']
		pose_str.position = [change[0], change[1], change[2]]
		publisher.publish(pose_str)
		
		curr_time = curr_time +1./freq
		rate.sleep()
	start = end
	
	return True
def inter(pos0, pos1,  time, curr_time, iflin):
	if iflin == False:
		h = 2.*(pos1-pos0)/time
		rat = h/(time/2.)
		if curr_time < time/2.:
			return pos0 + curr_time**2 * rat/2.
		else:
			return pos1 - (time - curr_time)**2 * rat/2.
	else:
		return pos0 + ((pos1-pos0)/time) * curr_time

if __name__ == "__main__":
	rospy.init_node('int_srv')
	rate = rospy.Rate(50)
	publisher = rospy.Publisher('joint_states',JointState, queue_size=10)
	s = rospy.Service('int', Jint, interpol)
	rospy.spin()
