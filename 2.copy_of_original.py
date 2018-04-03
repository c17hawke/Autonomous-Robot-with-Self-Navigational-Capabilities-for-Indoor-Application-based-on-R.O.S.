#!/usr/bin/env python

import rospy
import pygame
import time
from std_msgs.msg import Float32
import cv2
import numpy



# def write(e):
# 	with open('hello.txt', 'a') as f: 
# 		f.write(str(e))




def callback(data):
    rospy.loginfo("I receive dist from sensor ONE= %s", data.data)
    ratio = 5
    d = data.data
    with open('logfile.txt','a') as f:
    	f.write('sensor 1= '+str(d) + ',')

    gap =int(4.8*ratio)
    #-----------Trial-----------------------------
    img = numpy.ones((800,800,1),numpy.uint8)*55
    cv2.imwrite('map1.png', img)
    vx = 50
    vy = 50
    grid = 1
    for i in range(0,45,1):
    	grid = i*50
    	cv2.line(img, (vx+grid,vy), (vx+grid,800), (116,139,69), 1)
    	cv2.imwrite('map1.png', img)
    	#print i
    vx = 50
    vy = 50
    grid = 1
    for i in range(0,45,1):
    	grid = i*50
    	cv2.line(img, (vx,vy+grid), (800,vy+grid), (116,139,69), 1)
    	cv2.imwrite('map1.png', img)
    	#print i
    #--------------ends---------------------------
    image = cv2.imread('map1.png')
    #print d
    d = int(d*ratio)
    start1 = (400,400)
    end1 = (400+d,400)
    cv2.line(image, start1, end1, (0,255,0), 2)
    cv2.imwrite('map1.png', image)
    #cv2.imshow('map1.png', image)
    #cv2.waitKey(1)
    #write(end1)
    end1 = str(end1[0]) + " " + str(end1[1]) + " "
    with open('hello.txt', 'w') as f: 
		f.write(end1)


def callback2(data):
    rospy.loginfo("I receive dist from sensor TWO= %s", data.data)
    ratio = 5
    d = data.data
    with open('logfile.txt','a') as f:
    	f.write('sensor 2= '+str(d)+ '\n')
    gap =int(4.8*ratio)
    # #-----------Trial-----------------------------
    # img = numpy.ones((800,800,1),numpy.uint8)*1
    # cv2.imwrite('map1.png', img)
    # vx = 100
    # vy = 100
    # grid = 1
    # for i in range(0,9,1):
    # 	grid = i*100
    # 	cv2.line(img, (vx+grid,vy), (vx+grid,800), (255,0,0), 1)
    # 	cv2.imwrite('map1.png', img)
    # 	#print i
    # vx = 100
    # vy = 100
    # grid = 1
    # for i in range(0,9,1):
    # 	grid = i*100
    # 	cv2.line(img, (vx,vy+grid), (800,vy+grid), (255,0,0), 1)
    # 	cv2.imwrite('map1.png', img)
    # 	#print i
    # # #--------------ends---------------------------
    image = cv2.imread('map1.png')
    #print d
    d = int(d*ratio)
    start2 = (400,424)
    end2 = (400+d,424)
    cv2.line(image, start2, end2, (0,255,0), 2)
    cv2.imwrite('map1.png', image)
    #cv2.imshow('map1.png', image)
    #cv2.waitKey(1)
    #write(end2)
    end2 = str(end2[0]) + " " + str(end2[1]) + " "
    with open('hello.txt', 'a') as f: 
    	f.write(end2)
    joinEnd()

def joinEnd():
	with open('hello.txt', 'r') as f:
		data = f.read()
		theList = data.split(" ")

	start = (int(theList[0]),int(theList[1]))
	end = (int(theList[2]),int(theList[3]))
	image = cv2.imread('map1.png')
	cv2.line(image, start, end, (0,0,255), 2)
	cv2.imwrite('map1.png', image)
	cv2.imshow('map1.png', image)
	cv2.waitKey(1)
    


def subscriber():
    rospy.init_node('listner')
    for i in range(2):
    	if i == 0:
    		rospy.Subscriber('dist',Float32, callback)
    	if i == 1:
    		rospy.Subscriber('dist2',Float32, callback2)


    #joinend(e1[0],e1[1],e2[0],e2[1])
    rospy.spin()



if __name__ == "__main__":
	# img = numpy.ones((800,800,1),numpy.uint8)*1
	# #cv2.imshow('image',img)
	# cv2.imwrite('map1.png', img)

	# # ---------------Trial----------------
	# vx = 100
	# vy = 100
	# grid = 1
	# for i in range(0,9,1):
	# 	grid = i*100
	# 	cv2.line(img, (vx+grid,vy), (vx+grid,800), (255,0,0), 1)
	# 	cv2.imwrite('map1.png', img)
	# 	#print i

	# vx = 100
	# vy = 100
	# grid = 1
	# for i in range(0,9,1):
	# 	grid = i*100
	# 	cv2.line(img, (vx,vy+grid), (800,vy+grid), (255,0,0), 1)
	# 	cv2.imwrite('map1.png', img)
	# 	#print i
	#----------------Trial ends-----------
	try:
		subscriber()
	except rospy.ROSInterruptException:
		pass
        #callback(data)




    # pygame.quit()
    # quit()