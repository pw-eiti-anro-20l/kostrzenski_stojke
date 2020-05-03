#! /usr/bin/python

import rospy
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
import os
from tf.transformations import *
from visualization_msgs.msg import Marker

class NonKdlDkin:

	def __init__(self):
		rospy.init_node("non_kdl_dkin", anonymous=True)
		self.load_dh_params()
		self.setup_publisher()
		self.start_listening_to_topic()
		rospy.spin()

	def load_dh_params(self):
		json_reader = open('../yaml/dh_params.json', 'r')
		self.dh_params = json.loads(json_reader.read())
		buf = self.dh_params["i_3"]
		self.dh_params["i_3"] = self.dh_params["i_1"]
		self.dh_params["i_1"] = buf 

	def setup_publisher(self):
		self.publisher = rospy.Publisher('/geometry_msgs', PoseStamped, queue_size=10)

	def start_listening_to_topic(self):
		rospy.Subscriber("/joint_states", JointState, self.publish_position_to_rviz)

	def publish_position_to_rviz(self, position):
		x_axis = (1, 0, 0)
		z_axis = (0, 0, 1)
		matrix = translation_matrix((0, 0, 0))
		
		link_counter = 0
		for key in self.dh_params.keys():
			a, d, alpha, theta = self.dh_params[key]
			a, d, alpha, theta = float(a), float(d), float(alpha), float(theta)
			print(link_counter)
			print(a)
			print(d)
			print(alpha)
			print(theta)

			d_translation = translation_matrix((0, 0, d + position.position[link_counter]))
			theta_rotation = rotation_matrix(theta, z_axis)
			a_translation = translation_matrix((a, 0, 0))
			alpha_rotation = rotation_matrix(alpha, x_axis)

			concatenated_matrix = concatenate_matrices(alpha_rotation, a_translation, theta_rotation, d_translation)
			matrix = concatenate_matrices(matrix, concatenated_matrix)
			link_counter += 1

		x, y, z = translation_from_matrix(matrix)
		qx, qy, qz, qw = quaternion_from_matrix(matrix)
		non_kdl_pose = PoseStamped()
		non_kdl_pose.header.frame_id = 'base_link'
		non_kdl_pose.header.stamp = rospy.Time.now()

		non_kdl_pose.pose.position.x = x
		non_kdl_pose.pose.position.y = y
		non_kdl_pose.pose.position.z = z
		non_kdl_pose.pose.orientation.x = qx
		non_kdl_pose.pose.orientation.y = qy
		non_kdl_pose.pose.orientation.z = qz
		non_kdl_pose.pose.orientation.w = qw
		self.publisher.publish(non_kdl_pose)
			

if __name__ == '__main__':
	try:
		NonKdlDkin()
	except rospy.ROSInterruptException:
		pass
