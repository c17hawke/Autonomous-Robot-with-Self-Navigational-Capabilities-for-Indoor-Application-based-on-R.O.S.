##!/usr/bin/env python
import rospy
from main.botCommander import co

"""This is main file for controling"""
obj = co.motor_cmd()
obj.control('co')
