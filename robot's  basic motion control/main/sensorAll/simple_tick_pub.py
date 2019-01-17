#!/usr/bin/env python
from __future__ import division
import rospy
import RPi.GPIO as GPIO
from time import sleep
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist

class SpeedSensor:
    """this governs the controling of LM 393 sensor module for estimating no. of counts in a rotation"""
    def __init__(self):
        self.Count = 0
        self.rate = 10
        self.accumulator = 0
        self.direction = True # True mean +ve
        self.curr_count = 0
        self.past_count = 0
        self.delta = 0

    def init_GPIO(self):
        """intitalize GPIO of raspberry pi"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.sensor,GPIO.IN,GPIO.PUD_UP)

    def count_pulse(self,channel):
        self.Count += 1

    def init_interrupt(self):
	# add rising edge detection on a channel, ignoring further edges for 20ms for switch bounce handling
	GPIO.add_event_detect(self.sensor, GPIO.RISING, callback = self.count_pulse, bouncetime = 20)

    def callback_dir(self,msg):
        self.direction = msg.data

    def publish_ticks(self):
        """publish ticks count"""
        self.curr_count = self.Count
        self.delta = self.curr_count - self.past_count

        if not self.direction:
            self.accumulator -= self.delta 
            self.Pub.publish(self.accumulator)
        else:
            self.accumulator += self.delta
            self.Pub.publish(self.accumulator)

    def main(self,pin,nodeName,topicName, dir_topic):
        try:
            self.sensor = pin
            self.init_GPIO()
            rospy.init_node(nodeName)
            self.Pub = rospy.Publisher(topicName, Int32, queue_size=10)
            self.init_interrupt()
            rate = rospy.Rate(self.rate)
            while not rospy.is_shutdown():
                self.past_count = self.Count
                rospy.Subscriber(dir_topic, Int32, self.callback_dir)
                self.publish_ticks()
                rate.sleep()
        except Exception as e:
            raise e
        finally:
            GPIO.cleanup()
