import cv2
import numpy as np
import datetime


lk_params = dict(winSize = (15, 15),
                 maxLevel = 4,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

def get_points(top,bottom,left,right):

	mid_point = ((right-left)//2+left,(bottom-top)//2+top)
	top_left_point = ((right - left) // 4 + left, (bottom - top) // 4 + top)
	top_right_point = (3*(right - left) // 4 + left, (bottom - top) // 4 + top)
	bottom_left_point = ((right - left) // 4 + left, 3*(bottom - top) // 4 + top)
	bottom_right_point = (3*(right - left) // 4 + left, 3*(bottom - top) // 4 + top)

	return [mid_point,top_left_point,top_right_point,bottom_left_point,bottom_right_point]

def points_matrix(coordinate_list,frame,old_frame):
    distance = 0
    new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    old_points = np.array([get_points(coordinate_list[1],coordinate_list[3],coordinate_list[0],coordinate_list[2])], dtype=np.float32)

    new_points, status, error = cv2.calcOpticalFlowPyrLK(old_frame, new_frame, old_points, None, **lk_params)
    #for point in get_points(coordinate_list[1],coordinate_list[3],coordinate_list[0],coordinate_list[2]):
    new_points, status, error = cv2.calcOpticalFlowPyrLK(old_frame, new_frame, old_points, None, **lk_params)

    for index,point in enumerate(new_points[0]):
        distance += np.sqrt(np.sum(np.square(old_points[0][index][0] - point[0]) + np.square(old_points[0][index][1] - point[1])))

    for i, (new, old) in enumerate(zip(new_points[0], old_points[0])):
        a, b = new.ravel()
        c, d = old.ravel()
        cv2.line(frame, (a, b), (c, d), (0, 0, 255), 2)
        frame = cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)
    return distance

def get_point_similarity(former_point,new_point):
    similarity = 0
    for index, item in enumerate(former_point):
        similarity = similarity + abs(item - new_point[index])
    return similarity

def sort_boxs(former_boxs,new_boxs):
    sorted_boxs = former_boxs
    for box in new_boxs:
        similarity_list = []
        for index, former_box in enumerate(former_boxs):
                similarity = get_point_similarity(former_box,box)
                similarity_list.append(similarity)
        sorted_boxs[np.argmin(similarity_list)]=box
    return sorted_boxs

def empty_warning(frame,file_path):
    print('Warning!!' + '\n')
    cv2.imwrite(file_path+ '/' + str(datetime.datetime.now())[:-7] + '.jpg', frame)
    with open(file_path + '/warning_log.txt', 'a+') as f:
        f.writelines(str(datetime.datetime.now())[:-7] + '\n')


