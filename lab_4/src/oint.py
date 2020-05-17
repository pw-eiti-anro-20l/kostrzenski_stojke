#! /usr/bin/python

import rospy
from lab_4.srv import oint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from nav_msgs.msg import Path
import math
from geometry_msgs.msg import PoseStamped
 

class OintInterpolator:

	def __init__(self):
		self.current_position = [ 0.0, 0.0, 0.0 ]
		self.current_q = [ 0.0, 0.0, 0.0, 1.0 ]
		self.frequency = 50
		self.path = Path()

		self.init_node()
		self.setup_publisher()
		self.setup_service()
		self.setup_rate()

	def init_node(self):
		rospy.init_node('int_srv')

	def setup_publisher(self):
		self.publisher = rospy.Publisher('oint', PoseStamped, queue_size=10)
		self.path_publisher = rospy.Publisher('oint_path', Path, queue_size=10)

	def setup_service(self):
		self.service = rospy.Service('oint_control_srv', oint, self.create_interpolation)

	def setup_rate(self):
		self.rate = rospy.Rate(self.frequency)

	def validate_message(self, message):
		if message.t <= 0:
			return False

		return True

	def calculate_step(self, start, end, current_time, time):
		return start + ((end - start)/time) * current_time

	def create_interpolation(self, data):
		if self.validate_message(data) == False:
			return False

		new_position = (data.x, data.y, data.z)
		new_q = (data.qx, data.qy, data.qz, data.qw)
		how_many_frames = int(math.ceil(data.t * self.frequency))
		current_time = 1.0 / self.frequency

		for i in range(how_many_frames + 1):
			x = self.calculate_step(self.current_position[0], new_position[0], current_time, data.t)
			y = self.calculate_step(self.current_position[1], new_position[1], current_time, data.t)
			z = self.calculate_step(self.current_position[2], new_position[2], current_time, data.t)
			qx = self.calculate_step(self.current_q[0], new_q[0], current_time, data.t)
			qy = self.calculate_step(self.current_q[1], new_q[1], current_time, data.t)
			qz = self.calculate_step(self.current_q[2], new_q[2], current_time, data.t)
			qw = self.calculate_step(self.current_q[3], new_q[3], current_time, data.t)


			pose = PoseStamped()
			pose.header.frame_id = "base_link"
			pose.header.stamp = rospy.Time.now()
			pose.pose.position.x = x
			pose.pose.position.y = y
			pose.pose.position.z = z
			pose.pose.orientation.x = qx
			pose.pose.orientation.y = qy
			pose.pose.orientation.z = qz
			pose.pose.orientation.w = qw
			self.publisher.publish(pose)

			self.path.header = pose.header
			self.path.poses.append(pose)
			self.path_publisher.publish(self.path)

			current_time = current_time + 1.0/self.frequency
			self.rate.sleep()

		self.current_position = new_position
		self.current_q = new_q
		return True
 
if __name__ == "__main__":
	interpolator = OintInterpolator()
	rospy.spin()