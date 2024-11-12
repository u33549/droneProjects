#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

bridge = CvBridge()
image_received = False

selected_area_dimensions = None  # Seçilen alanın boyutlarını kaydetmek için bir değişken

def image_callback(msg):
    global selected_area_dimensions
    try:
        # ROS mesajını OpenCV formatına çevir
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Görüntüyü HSV formatına çevir
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        # Kırmızı rengi seçmek için HSV aralığı belirle
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        
        # Kırmızı renk maskesi oluştur
        mask = cv2.inRange(hsv_image, lower_red, upper_red)
        
        # Maskeyi kullanarak kırmızı alanları filtrele
        result = cv2.bitwise_and(cv_image, cv_image, mask=mask)

        # İşlenmiş görüntüyü göster
        cv2.imshow("Original Image", cv_image)
        cv2.imshow("Red Filtered Image", result)
        cv2.waitKey(1)

    except CvBridgeError as e:
        rospy.logerr("CvBridge hatası: {}".format(e))

def main():
    rospy.init_node('image_listener', anonymous=True)
    rospy.Subscriber("roscam/cam/image_raw", Image, image_callback)
    rospy.spin()
    # Diğer kod parçalarında boyutlara erişmek için burada kullanabilirsiniz
    if selected_area_dimensions:
        x, y, w, h = selected_area_dimensions
        rospy.loginfo("Seçilen alan boyutları - x: {}, y: {}, genişlik: {}, yükseklik: {}".format(x, y, w, h))


main()
