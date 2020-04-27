#! /usr/bin/python

import rospy
from geometry_msgs.msg import PoseStamped
import json

class NonKdlDkin:

	def __init__():
		rospy.init_node("non_kdl_dkin", anonymous=True)
		self.load_dh_params()
		self.setup_publisher()
		self.start_listening_to_topic()
		rospy.spin()

	def load_dh_params():
		json_reader = open('../yaml/dh_params.json', 'r')
		self.dh_params = json.loads(json_reader.read())

	def setup_publisher():
		self.publisher = rospy.Publisher('/geometry_msgs', PoseStamped, queue_size=10)

	def start_listening_to_topic():
		rospy.Subscriber("/sensor_msgs", JointState, publish_position_to_rviz)

	def publish_position_to_rviz(position):
		x_axis = (1, 0, 0)
		y_axis = (0, 1, 0)
		z_axis = (0, 0, 1)

		for link in dh_params:
			print("test")



if __name__ = '__main__':
	try:
		NonKdlDkin()
	except rospy.ROSInterruptException:
		pass
