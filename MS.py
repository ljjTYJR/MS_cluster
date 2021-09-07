"""
The algorithm process of MS(Mean Shift)
"""
import numpy
from Algo1 import Algo1
from Algo2 import Algo2
import numpy as np
import math
import sys

class MeanShift(object):
    def __init__(self, data_path, algo_name, bandwidth, threshold):
        self.data_path = data_path
        if algo_name == 'Algo1':
            self.alg = Algo1()
        elif algo_name == 'Algo2':
            self.alg = Algo2()
        self.bandwidth = bandwidth
        self.threshold = threshold

    def ms_process(self):
        # read data from csv and store in `data`
        # for `Algo1` : get the processed data
        # for `Algo2` : get the original data
        data = self.alg.get_data(self.data_path)
        original_points = np.array(data)
        shifting_points = np.array(data)

        # initialize a max_distance greater than threshold
        max_distance = self.threshold + 1
        # flag to reveal whether the point need to iterate
        end_flag = [False] * original_points.shape[0]
        # record the iteratoring time
        iteration_times = 0
        # if not setting the bandwidth, set the bandwidth by N
        if self.bandwidth is None:
            self.bandwidth = self._compute_bandwidth(original_points)

        # the loop for mean shift
        while max_distance > self.threshold:
            iteration_times += 1
            print("iteration times =", iteration_times, ",", "max_distance =", max_distance)
            # update the points in shifting_points simultaneously
            for i in range(len(original_points)):
                max_distance = 0
                # the ith point has already converge
                if end_flag[i] : continue
                # the old point in shifting array
                p_old = shifting_points[i]
                # get the new point after one iteration
                p_new = self._shift_point(p_old, original_points, self.bandwidth)
                old_new_distance = self.alg.calculate_distance(p_new, p_old)
                # cal the distance of old point and new point, compare it with threshold
                # get the max distance in the shifting points
                if old_new_distance > max_distance:
                    max_distance = old_new_distance

                if old_new_distance < self.threshold:
                    end_flag[i] = True
                shifting_points[i] = p_new
        return original_points, shifting_points

     # compute the bandwidth if the `self.bandwidth` is None
    def _compute_bandwidth(self, points):
        N = len(points)
        # get the mean and variance the total points
        _, var = self.alg.calculate_mean_point(points)
        # compute the standard standard deviation
        data_std = math.sqrt(var)
        print("set bandwidth=",(1.05 * data_std) * (pow(N, -0.2)))
        return (1.05 * data_std) * (pow(N, -0.2))

    # Use the MS to generate new point
    def _shift_point(self, p_old, points, bandwidth):
        weights = self._kernel(p_old, points, bandwidth)
        p_new_x = float(0)
        p_new_y = float(0)
        i = 0
        weights_num = float(0)
        for p_tmp in points:
            # iterate the new point
            p_new_x += p_tmp[0] * weights[i]
            p_new_y += p_tmp[1] * weights[i]
            weights_num += weights[i]
            i = i + 1
        p_new_x /= weights_num
        p_new_y /= weights_num
        return [p_new_x, p_new_y]

    # use the kernel function to compute the point weight
    def _kernel(self, point, point_set, bandwidth):
        weights = []
        for p_tmp in point_set:
            distance = self.alg.calculate_distance(point, p_tmp)
            norm = (distance ** 2) / (bandwidth ** 2)
            weight_tmp = (1 / (bandwidth * math.sqrt(2 * math.pi))) * math.exp(-0.5 * norm)
            weights.append(weight_tmp)
        return weights

