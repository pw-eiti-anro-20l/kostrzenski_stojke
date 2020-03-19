#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from pynput.keyboard import Key, Listener


class TurtleKeyboardController:

	default_control = {
		"forward": 'w',
		"backward": 's',
		"left": 'a',
		"right": 'd',
	}

	def __init__(self):
		rospy.init_node('turtle_keyboard_controller', anonymous=True)
		self.publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
		self.turtle_control = self.get_turtle_controls()			# load turtle controls

		
	def start(self):
		self.keyboard_listener = Listener(on_press=self.key_pressed) # start key listener
		self.keyboard_listener.start()
		self.keyboard_listener.join()
		rospy.spin()

	def get_turtle_controls(self):
		if rospy.has_param("turtle_control"):
			turtle_control = rospy.get_param("turtle_control")
			for key in self.default_control.keys():				# check if all direction keys are defined
					if key not in turtle_control.keys():		# if key is not defined, set default value
						rospy.loginfo(key + " control not found, setting default...")
						turtle_control[key] = self.default_control[key]

			return turtle_control
		else:	# if parameter is missing
			rospy.loginfo("Turtle controls not found in params server, setting default controls...")
			return self.default_control

	def key_pressed(self, key):
		try:
			keyboard_key = key.char
			if keyboard_key in self.turtle_control.values():		# checks whether loaded key is on of the control keys
				msg = Twist()										# define empty Twist message
				if self.turtle_control["forward"] == keyboard_key:	# check which key is it and add correct velocity
					msg.linear.x = 2
				elif self.turtle_control["backward"] == keyboard_key:
					msg.linear.x = -2
				elif self.turtle_control["left"] == keyboard_key:
					msg.angular.z = 2
				elif self.turtle_control["right"] == keyboard_key:
					msg.angular.z = -2

				self.publisher.publish(msg)					# publish message

		except AttributeError:								# if input is not normal key like Ctrl or Shift
			rospy.logerr("Incorrect key type! Stopped publishing...")
			self.keyboard_listener.stop()

if __name__ == '__main__':
	try:
		TurtleKeyboardController().start()
	except rospy.ROSInterruptException:
		pass