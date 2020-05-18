#! /usr/bin/python

import rospy
import json
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from sensor_msgs.msg import JointState
import os
from tf.transformations import *
from visualization_msgs.msg import Marker

path = Path()

class path_drawer:

	def __init__(self):
		rospy.init_node("path_draw", anonymous=True)
		self.load_dh_params()
		self.load_restrictions()
		self.setup_publisher()
		self.start_listening_to_topic()
		rospy.spin()

	def load_dh_params(self):
		path = os.path.realpath(__file__)
		with open(os.path.dirname(path) + '/../yaml/dh_params.json') as params:
			self.dh_params = json.loads(params.read())
			buf = self.dh_params["i_3"]
			self.dh_params["i_3"] = self.dh_params["i_1"]
			self.dh_params["i_1"] = buf

	def load_restrictions(self):
		path = os.path.realpath(__file__)
		with open(os.path.dirname(path) + '/../yaml/restrictions.json') as rest:
			self.restrictions = json.loads(rest.read())	


	def setup_publisher(self):
		self.publisher = rospy.Publisher('Path_drawer', Path, queue_size=10)

	def start_listening_to_topic(self):
		rospy.Subscriber("/joint_states", JointState, self.publish_position_to_rviz)

	def check(self, pose):
		if pose.position[0] < self.restrictions['i_1'][0] or pose.position[0] > self.restrictions['i_1'][1]:
			return False
		if pose.position[1] < self.restrictions['i_2'][0] or pose.position[1] > self.restrictions['i_2'][1]:
			return False
		if pose.position[2] < self.restrictions['i_3'][0] or pose.position[2] > self.restrictions['i_3'][1]:
			return False
		return True

	def publish_position_to_rviz(self, pose):
		if(self.check(pose) == False):
			rospy.logerr('Impossible position: ' + str(pose))
			return

		x_axis = (1, 0, 0)
		z_axis = (0, 0, 1)
		matrix = translation_matrix((0, 0, 0))
		link_counter = 0
		for key in self.dh_params.keys():
			a, d, alpha, theta = self.dh_params[key]
			a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)

			d_translation = translation_matrix((0, 0, d + pose.position[link_counter]))
			theta_rotation = rotation_matrix(theta, z_axis)
			a_translation = translation_matrix((a, 0, 0))
			alpha_rotation = rotation_matrix(alpha, x_axis)

			concatenated_matrix = concatenate_matrices(alpha_rotation, a_translation, theta_rotation, d_translation)
			matrix = concatenate_matrices(matrix, concatenated_matrix)
			link_counter += 1

		x, y, z = translation_from_matrix(matrix)
		qx, qy, qz, qw = quaternion_from_matrix(matrix)
		pose = PoseStamped()
		pose.header.frame_id = 'base_link'
		pose.header.stamp = rospy.Time.now()

		pose.pose.position.x = x
		pose.pose.position.y = y
		pose.pose.position.z = z
		pose.pose.orientation.x = qx
		pose.pose.orientation.y = qy
		pose.pose.orientation.z = qz
		pose.pose.orientation.w = qw

		path.header = pose.header
		path.poses.append(pose)
		self.publisher.publish(path)
			

if __name__ == '__main__':
	try:
		path_drawer()
	except rospy.ROSInterruptException:
		pass
