import cv2
import numpy as np
import time
from utils import *

video_capture = cv2.VideoCapture('demo_normal.mp4')
ret, frame = video_capture.read()
#old_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(frame)

old_points = np.array([[500, 603]], dtype=np.float32)

lk_params = dict(winSize=(15, 15),
                 maxLevel=4,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

distance_list = []
average_distance = 0

def get_distance(old_points, new_points):
    return np.sqrt(np.sum(np.square(old_points[0] - new_points[0]) + np.square(old_points[1] - new_points[1])))


def select_point(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(str(x) + ' ' + str(y))


cv2.namedWindow("Optical Flow")
cv2.setMouseCallback("Optical Flow", select_point)

while True:

    ret, frame = video_capture.read()
    coordinate_list = [148, 484, 322, 895]
    distance = points_matrix(coordinate_list, frame, old_frame)

    average_distance = (distance+average_distance)/2
    print(average_distance)


    old_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Optical Flow', frame)
    time.sleep(0.25)
    key = cv2.waitKey(1)
    if key == 27:
        break

video_capture.release()
cv2.destroyAllWindows()
