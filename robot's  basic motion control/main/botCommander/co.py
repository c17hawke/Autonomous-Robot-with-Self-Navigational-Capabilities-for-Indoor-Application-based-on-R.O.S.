#!/usr/bin/env python

import rospy
import curses
import RPi.GPIO as GPIO
import time
from std_msgs.msg import Int32

class motor_cmd:
    def __init__(self):
        """declare variables and setup raspberry pi 3"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.Ap = 33
        self.Am = 35
        self.Ae = 37
        self.Bp = 36
        self.Bm = 38
        self.Be = 40
        GPIO.setup(self.Ap,GPIO.OUT)
        GPIO.setup(self.Am,GPIO.OUT)
        GPIO.setup(self.Ae,GPIO.OUT)

        GPIO.setup(self.Bp,GPIO.OUT)
        GPIO.setup(self.Bm,GPIO.OUT)
        GPIO.setup(self.Be,GPIO.OUT)

        self.my_pwm_A = GPIO.PWM(self.Ae,50)
        self.my_pwm_B = GPIO.PWM(self.Be,50)
        self.begin_pwm()

    def begin_pwm(self):
        """set initial pwm"""
        self.my_pwm_A.start(50)
        self.my_pwm_B.start(50)

        self.fasta=int(raw_input("How fast a? (20-100)"))
        self.fastb=int(raw_input("How fast b? (20-100)"))

        self.my_pwm_A.ChangeDutyCycle(self.fasta)
        self.my_pwm_B.ChangeDutyCycle(self.fastb)

    def control(self, nodeName):
        """Initialize node and basic keyboard control for our robot"""
        rospy.init_node(nodeName)
        self.pub_left = rospy.Publisher('left', Int32, queue_size=10)
        self.pub_right = rospy.Publisher('right', Int32, queue_size=10)

        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)

        #GPIO.output(Ae,True)
        #GPIO.output(Be,True)
        try:
                while True:
                    char = screen.getch()
                    if char == ord('q'):
            		    self.my_pwm_A.stop()
            		    self.my_pwm_B.stop()
                            break
                    elif char == curses.KEY_UP:
    	                    t = rospy.Time.from_sec(time.time())
            		    seconds_then = t.to_sec()
            		    self.forward()
                            print "forward time: \r"
                    elif char == curses.KEY_DOWN:
                        t = rospy.Time.from_sec(time.time())
                        seconds_then = t.to_sec()
                        self.back()
                        print "retreat time: \r"
                    elif char == curses.KEY_RIGHT:
                        t = rospy.Time.from_sec(time.time())
                        seconds_then = t.to_sec()
                        self.right()
                        print "right turn time: \r"
                    elif char == curses.KEY_LEFT:
                        t = rospy.Time.from_sec(time.time())
                        seconds_then = t.to_sec()
                        self.left()
                        print "left turn time: \r"
                    elif char == 10:
                        now = rospy.Time.from_sec(time.time())
                        seconds_now = now.to_sec()
                        print str(seconds_now-seconds_then) + " secs \r"
                        print "--"*20 + "\r"
                        self.stop()

        except:
    	       print "done !!"
        finally:
            #Close down curses properly, inc turn echo back on!
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()
            GPIO.cleanup()

    def back(self):
        """retreat"""
        GPIO.output(self.Ap,False)
        GPIO.output(self.Am,True)
        GPIO.output(self.Bp,False)
        GPIO.output(self.Bm,True)
        self.pub_left.publish(-1)
        self.pub_right.publish(-1)

    def forward(self):
        """Advance"""
        GPIO.output(self.Am,False)
        GPIO.output(self.Ap,True)
        GPIO.output(self.Bp,True)
        GPIO.output(self.Bm,False)
        self.pub_left.publish(1)
        self.pub_right.publish(1)

    def left(self):
        """Left turn"""
        GPIO.output(self.Am,True)
        GPIO.output(self.Ap,False)
        GPIO.output(self.Bp,True)
        GPIO.output(self.Bm,False)
        self.pub_left.publish(-1)
        self.pub_right.publish(1)

    def right(self):
        """Right turn"""
        GPIO.output(self.Ap,True)
        GPIO.output(self.Am,False)
        GPIO.output(self.Bp,False)
        GPIO.output(self.Bm,True)
        self.pub_left.publish(1)
        self.pub_right.publish(-1)

    def stop(self):
        """Halt"""
        GPIO.output(self.Ap,False)
        GPIO.output(self.Am,False)
        GPIO.output(self.Bp,False)
        GPIO.output(self.Bm,False)
        self.pub_left.publish(0)
        self.pub_right.publish(0)

# def main():
#     commander = motor_cmd()
#     commander.control()
# if __name__ == '__main__':
#     main()
