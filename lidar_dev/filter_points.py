from collections import defaultdict
import numpy as np
import pickle
import time

distance_maximum = 150
kth_closet = 54
# angle_maximum = front
#
def filter_distance_and_angle(samples):
    samples_return = []
    for sample in samples:
        angle = sample.angle
        if 0 <= angle <= 90000 or 270000 <= angle <= 360000:
            distance = min(sample.distance, distance_maximum)
            point = [angle, distance]
            samples_return.append(point)
    return samples_return   
def fetch_kth_closet_points(points):
    # Assumption: the input should be larger than kth_closet
    distance_map = defaultdict(list)
    distance_list = []
    for point in points:
        distance = point[1]
        distance_map[distance].append(point)
        distance_list.append(distance)
    distance_list.sort()
    final_length = min(len(distance_list), kth_closet)
    distance_list = distance_list[:final_length]
    points_return = []
    for distance in distance_list:
        points_return.extend(distance_map[distance])
    gap = kth_closet - len(distance_list)
    for _ in range(gap):
        points_return.append([-1, -1])
    return points_return
def print_by_left_and_right(points):
    stat = [0, 0]
    for point in points:
        angle = point[0]
        distance = point[1]
        if 0 < angle < 90000 and distance == 1:
            stat[0] += 1
        if 270000 < angle < 360000 and distance == 1:
            stat[1] += 1
    return stat
from sweeppy import Sweep
with Sweep('/dev/ttyUSB1') as sweep:
    sweep.set_sample_rate(1000)
    sweep.set_motor_speed(10)
    sweep.start_scanning()
    for scan in sweep.get_scans():
        samples = scan.samples
        points = filter_distance_and_angle(samples)
	t = time.time()
	pickle.dump(points,open( 'dataset_l/lidar_{0}.pickle'.format(t), 'wb' ))
        #kth_points = fetch_kth_closet_points(points)
        #print(len(points))
        #print(len(kth_points))
        #print(print_by_left_and_right(points))
        #print('{}\n'.format(kth_points))
