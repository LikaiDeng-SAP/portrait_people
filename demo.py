#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import os
from timeit import time
import warnings
import sys
import cv2
import numpy as np
from PIL import Image
from yolo import YOLO
import datetime
from ui import *
import random
from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from deep_sort.detection import Detection as ddet
from utils import *

warnings.filterwarnings('ignore')
empty_image = cv2.imread("nothing.jpg")
maximum_objects = 10
warning_threshold = 0
warning_photos_file = '/home/denglikai/Documents/Pycharm Projects/people-photo-distinction/warning_pictures'

#video_path = sys.argv[1]

def start(yolo,path,number_display):
    average_distance_list = [0] * maximum_objects
    video_capture = cv2.VideoCapture(path)
    ret, frame = video_capture.read()
    old_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    former_boxs = []
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH,416)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)
    while True:
        ret, frame = video_capture.read()  # frame shape 640*480*3
        print(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        print(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if ret != True:
            break;

        image = Image.fromarray(frame)
        boxs = yolo.detect_image(image)
        num_people = 0
        num_picture =0


        for box in boxs:
            box[2]+=box[0]
            box[3] += box[1]

        if len(boxs)>=maximum_objects:
            break

        if len(former_boxs) == 0 or len(former_boxs)!=len(boxs):
            former_boxs = boxs
            average_distance_list = [0] * maximum_objects
        else:
            boxs = sort_boxs(former_boxs,boxs)
            former_boxs = boxs

        for index, box in enumerate(boxs):

            distance = points_matrix(box, frame, old_frame)
            average_distance_list[index] = round((average_distance_list[index] + distance) / 2, 3)

            if average_distance_list[index] >= 1:
                num_people+=1
                cv2.putText(frame, str(index) + ' Person ',
                            (int(box[0]), int(box[1])), 0,
                            5e-3 * 200,
                            (0, 255, 0), 2)
                cv2.rectangle(frame, (int(box[0]), int(box[1])),
                              (int(box[2]), int(box[3])), (0, 255, 0), 2)
            else:

                num_picture+=1
                cv2.putText(frame, str(index) + ' Picture ',
                            (int(box[0]), int(box[1])), 0,
                            5e-3 * 200,
                            (255, 0, 0), 2)
                cv2.rectangle(frame, (int(box[0]), int(box[1])),
                              (int(box[2]), int(box[3])), (255, 0, 0), 2)
        print(average_distance_list)

        old_frame = new_frame

        number_display.display(num_people)

        if num_people <= warning_threshold:
            empty_warning(frame,warning_photos_file)


        print('People: ' + str(num_people) + '   Picture: ' + str(num_picture))
        cv2.imshow('', frame)

        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def yolo_launcher(path,ui):
    number_display = ui.lcd_people
    start(YOLO(),path,number_display)


path = '/home/denglikai/Documents/Pycharm Projects/people-photo-distinction/demos/demo_normal_too.mp4'
if __name__ == '__main__':
    yolo_launcher(path,UI)