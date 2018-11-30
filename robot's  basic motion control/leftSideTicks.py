#!/usr/bin/env python
import rospy
from main.sensorAll import simple_tick_pub

"""Objectve: to count no. ticks from left wheel sensor"""
obj = simple_tick_pub.SpeedSensor()
obj.main(31,'left_tick_pub','lwheel_ticks','left')