#!/usr/bin/env python

from math import cos, sin
import sys
import rospy
from lab_5.srv import oint


def circle():
    freq = 30.0
    ax = 0.3
    ay = 0.2
    az = 0.2
    th = 0.0
    dth = 0.5 * 3.1415 / freq

    t = 1.0 / freq
    x0 = 0.5
    y0 = -0.5
    z0 = 0.8

    rospy.wait_for_service('oint_control_srv')
    rate = rospy.Rate(freq)
    while not rospy.is_shutdown():
        x = x0 + ax * cos(th)
        y = y0 + ay * sin(th)
        z = z0 + az * sin(th)
        interpolation = rospy.ServiceProxy('oint_control_srv', oint)
        resp1 = interpolation(x, y, z, 0.0, 0.0, 0.0, 1.0, t)

        th = th + dth
        rate.sleep()


if __name__ == "__main__":
    rospy.init_node('circle')
    circle()
