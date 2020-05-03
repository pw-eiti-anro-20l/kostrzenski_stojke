#! /usr/bin/python

import rospy
import json
import os
import PyKDL as pykdl
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
import math
from tf.transformations import *

xAxis = (1,0,0)
yAxis = (0,1,0)
zAxis = (0,0,1)


def kin_fwd(params):
	publish = True
	k=1
	chain = pykdl.Chain()
	frame = pykdl.Frame()
	angles = pykdl.JntArray(3)
	prev_d=0
	prev_theta=0
	counter = 0
	for i in parametres.keys():
		
		a, d, alpha, theta = parametres[i]
		a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)	
		
		joint = pykdl.Joint(pykdl.Joint.TransZ)
		if k!=1:
			fr = frame.DH(a, alpha, prev_d, prev_theta)
			chain.addSegment(pykdl.Segment(joint,fr))
		k = k+1	
		prev_d = d
		prev_theta = theta
		
	chain.addSegment(pykdl.Segment(joint,frame.DH(0,0,d,theta)))
		
	angles[0] = params.position[0]
	angles[1] = params.position[1]
	angles[2] = params.position[2]
	solver = pykdl.ChainFkSolverPos_recursive(chain)
	secFrame = pykdl.Frame()
	solver.JntToCart(angles,secFrame)
	quater = secFrame.M.GetQuaternion()
	pose = PoseStamped()
	pose.header.frame_id = 'base_link'
	pose.header.stamp = rospy.Time.now()

	pose.pose.position.x = secFrame.p[0]
	pose.pose.position.y = secFrame.p[1]
	pose.pose.position.z = secFrame.p[2]

	pose.pose.orientation.x = quater[0]
	pose.pose.orientation.y = quater[1]
	pose.pose.orientation.z = quater[2]		
	pose.pose.orientation.w = quater[3]
	
	publisher.publish(pose)

if __name__ == '__main__':

	parametres = {}
	path = os.path.realpath(__file__)
	with open(os.path.dirname(path) + '/../yaml/dh_params.json') as params:
		parametres = json.loads(params.read())
		buf = parametres["i_3"]
		parametres["i_3"] = parametres["i_1"]
		parametres["i_1"] = buf
		print(parametres)

	rospy.init_node('KDL', anonymous=True)
	publisher=rospy.Publisher('KDL', PoseStamped, queue_size=10)
	rospy.Subscriber('/joint_states', JointState, kin_fwd)
	
	 
	rospy.spin()
