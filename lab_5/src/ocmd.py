#!/usr/bin/env python

from math import cos, sin
import sys
import rospy
from lab_5.srv import oint


def ellipse():
    frequency = 30.0
    ax = 0.3
    ay = 0.2
    az = 0.2
    theta = 0.0
    dth = 0.5 * 3.1415 / frequency

    t = 1.0 / frequency
    x0 = 0.5
    y0 = -0.5
    z0 = 0.8

    interpol = rospy.ServiceProxy('oint_control_srv', oint)
    interpol(x0 + ax*cos(theta), y0 + ay*sin(theta), z0 + az*sin(theta), 0.0, 0.0, 0.0, 1.0, 2.0)

    rospy.wait_for_service('oint_control_srv')
    rate = rospy.Rate(frequency)
    while not rospy.is_shutdown():
        x = x0 + ax * cos(theta)
        y = y0 + ay * sin(theta)
        z = z0 + az * sin(theta)
        move = interpol(x, y, z, 0.0, 0.0, 0.0, 1.0, t)

        theta = theta + dth
        rate.sleep()


if __name__ == "__main__":
    rospy.init_node('ellipse')
    ellipse()
