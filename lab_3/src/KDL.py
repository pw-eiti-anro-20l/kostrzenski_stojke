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
	
	chain = pykdl.Chain()
	frame = pykdl.Frame()
	angles = pykdl.JntArray(3)
	joints = [2,3,1]
	
	for i in joints:
		
		a, d, alpha, theta = parametres['i_'+str(i)]
		a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
		fr = frame.DH(a, alpha, d, theta)
		joint = pykdl.Joint(pykdl.Joint.RotZ)
		chain.addSegment(pykdl.Segment(joint,fr))
		
		angles[i-1] = params.position[i-1]
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
	rospy.init_node('KDL', anonymous=True)
	publisher=rospy.Publisher('KDL', PoseStamped, queue_size=10)
	rospy.Subscriber('/joint_states', JointState, kin_fwd)
	
	parametres={}
	print os.path.dirname(os.path.realpath(__file__))
	with open(os.path.dirname(os.path.realpath(__file__))+'/../yaml/dh_params.json', 'r') as file:
		parametres = json.loads(file.read())
	rospy.spin()
