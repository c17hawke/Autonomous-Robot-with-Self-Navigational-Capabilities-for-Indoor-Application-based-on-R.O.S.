#!/usr/bin/env python
import rospy
from main.sensorAll import simple_tick_pub


"""Objectve: to count no. ticks from right wheel sensor"""
obj = simple_tick_pub.SpeedSensor()
#main(self,pin,nodeName,topicName):
obj.main(32,'right_tick_pub','rwheel_ticks','right')