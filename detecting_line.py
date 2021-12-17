import cv2 as cv
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import numpy as np

bridge = CvBridge()

def callback(data):
    global direction
    cv_image = cv.imread('./images/line.png')
    cv_image = bridge.imgmsg_to_cv2 (data, cv.IMREAD_GRAYSCALE)
    cv.imshow('now driving', cv_image)
        
    rect_img = cv.rectangle(cv_image, (260, 430), (270, 440), (0,0,255), 3)
    rect_img = cv.rectangle(cv_image, (370, 430), (380, 440), (0,0,255), 3)
    cv.imshow('now driving',rect_img)

    left_img = cv_image[260:270, 430:440]
    right_img = cv_image[370:380, 430:440]
    
    if np.all(left_img) <60 :
        direction = 'RIGHT'
        pass
    elif np.all(right_img) < 60:
        direction = 'LEFT'
        pass
    else :
        direction = 'GO'
        pass
           
    pub = rospy.Publisher('/motor_commands', String, queue_size=10)
    pub.publish(direction)

def main():
    rospy.init_node('planer_node')
    rospy.Subscriber('/camera/image_raw',Image,callback)
    rospy.spin()
    pass

if __name__ == "__main__" :
    direction = None
    main()       
    pass

