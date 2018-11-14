#!/usr/bin/env python
"""OpenCV feature detectors with ros CompressedImage Topics in python.

This example subscribes to a ros topic containing sensor_msgs 
CompressedImage. It converts the CompressedImage into a numpy.ndarray, 
then detects and marks features in that image. It finally displays 
and publishes the new image - again as CompressedImage topic.
"""
__author__ = 'Simon Haller <simon.haller at uibk.ac.at>'
__version__ = '0.1'
__license__ = 'BSD'
# Python libs
import sys, time

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2

# Ros libraries
import roslib

roslib.load_manifest('traffic_sign')
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage

# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

VERBOSE = False


class image_feature:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        self.image_pub = rospy.Publisher("/traffic_sign/image/compressed",
                                         CompressedImage, queue_size=10)
        self.detection_pub = rospy.Publisher("/traffic_sign/detected", std_msgs.msg.String, queue_size=10)
        # self.bridge = CvBridge()

        # subscribed Topic
        self.subscriber = rospy.Subscriber("/raspicam_node/image/compressed",
                                           CompressedImage, self.callback, queue_size=10)
        if VERBOSE:
            print("subscribed to /camera/image/compressed")

    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected'''
        if VERBOSE:
            print('received image of type: "%s"' % ros_data.format)

        #### direct conversion to CV2 ####
        np_arr = np.fromstring(ros_data.data, np.uint8)
        # image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # OpenCV >= 3.0:

        """
        Shows live images with marked detections
        """
        show_face = True
        show_class1 = False
        show_class2 = False
        show_class3 = False
        show_class4 = False
        show_class5 = False
        show_class6 = False
        show_class7 = False
        show_class8 = False
        show_class9 = False
        show_class10 = False
        show_class11 = False

        np_arr = np.fromstring(ros_data.data, np.uint8)
        # image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # OpenCV >= 3.0:

        # img = cv2.resize(img, (960, 540))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        biggest_value = 0
        found_msg = "nothing"

        if show_face:
            face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if biggest_value < x*y:
                    found_msg = "face"
                    biggest_value = x * y
                self.write_text_on_image(img, "Faces", (x, y - 5))

        if show_class1:
            class_01_cascade = cv2.CascadeClassifier('cascades/cascade_entry_forbidden.xml')
            class_01 = class_01_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_01:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if biggest_value < x * y:
                    found_msg = "entry_forbidden"
                    biggest_value = x * y
                self.write_text_on_image(img, "entry forbidden", (x, y - 5))

        if show_class2:
            class_02_cascade = cv2.CascadeClassifier('cascades/cascade_pedestrians.xml')
            class_02 = class_02_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_02:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 128, 0), 2)
                if biggest_value < x * y:
                    found_msg = "pedestrians"
                    biggest_value = x * y
                self.write_text_on_image(img, "pedestrians", (x, y - 5))

        if show_class3:
            class_03_cascade = cv2.CascadeClassifier('cascades/cascade_turn_right.xml')
            class_03 = class_03_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_03:
                cv2.rectangle(img, (x, y), (x + w, y + h), (128, 255, 0), 2)
                if biggest_value < x * y:
                    found_msg = "turn_right"
                    biggest_value = x * y
                self.write_text_on_image(img, "turn right", (x, y - 5))

        if show_class4:
            class_04_cascade = cv2.CascadeClassifier('cascades/cascade_main_road.xml')
            class_04 = class_04_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_04:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                if biggest_value < x * y:
                    found_msg = "main_road"
                    biggest_value = x * y
                self.write_text_on_image(img, "main road", (x, y - 5))

        if show_class5:
            class_05_cascade = cv2.CascadeClassifier('cascades/cascade_turn_left.xml')
            class_05 = class_05_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_05:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 128, 0), 2)
                if biggest_value < x * y:
                    found_msg = "turn_left"
                    biggest_value = x * y
                self.write_text_on_image(img, "turn left", (x, y - 5))

        if show_class6:
            class_06_cascade = cv2.CascadeClassifier('cascades/cascade_warning.xml')
            class_06 = class_06_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_06:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 128, 128), 2)
                if biggest_value < x * y:
                    found_msg = "warning"
                    biggest_value = x * y
                self.write_text_on_image(img, "warning", (x, y - 5))

        if show_class7:
            class_07_cascade = cv2.CascadeClassifier('cascades/cascade_no_parking.xml')
            class_07 = class_07_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_07:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 128), 2)
                if biggest_value < x * y:
                    found_msg = "no_parking"
                    biggest_value = x * y
                self.write_text_on_image(img, "no parking", (x, y - 5))

        if show_class8:
            class_08_cascade = cv2.CascadeClassifier('cascades/cascade_bus_stop.xml')
            class_08 = class_08_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_08:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                if biggest_value < x * y:
                    found_msg = "bus_stop"
                    biggest_value = x * y
                self.write_text_on_image(img, "bus stop", (x, y - 5))

        if show_class9:
            class_09_cascade = cv2.CascadeClassifier('cascades/cascade_crossing.xml')
            class_09 = class_09_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_09:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                if biggest_value < x * y:
                    found_msg = "entry_crossing"
                    biggest_value = x * y
                self.write_text_on_image(img, "crossing", (x, y - 5))

        if show_class10:
            class_10_cascade = cv2.CascadeClassifier('cascades/cascade_slippery.xml')
            class_10 = class_10_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_10:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                if biggest_value < x * y:
                    found_msg = "entry_slippery"
                    biggest_value = x * y
                self.write_text_on_image(img, "slippery", (x, y - 5))

        if show_class11:
            class_11_cascade = cv2.CascadeClassifier('cascades/cascade_road_closed.xml')
            class_11 = class_11_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in class_11:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                if biggest_value < x * y:
                    found_msg = "entry_road_closed"
                    biggest_value = x * y
                self.write_text_on_image(img, "road closed", (x, y - 5))

        cv2.imshow('Webcam', img)
        cv2.waitKey(2)

        #### Create CompressedIamge ####
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', img)[1]).tostring()

        # Publish new image
        self.image_pub.publish(msg)
        self.detection_pub(found_msg)

        # self.subscriber.unregister()

    @staticmethod
    def write_text_on_image(img, message, bottom_left_corner_of_text=(10, 500)):
        """
        Writes text above the recognized field

        :param img:
        :param message:
        :param bottom_left_corner_of_text:
        :return:
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 255, 0)
        line_type = 2

        cv2.putText(img, message,
                    bottom_left_corner_of_text,
                    font,
                    font_scale,
                    font_color,
                    line_type)


def main(args):
    '''Initializes and cleanup ros node'''
    ic = image_feature()
    rospy.init_node('image_feature', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print
        "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)