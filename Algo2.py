"""
The implemention of Algorithm2
"""

import os
import numpy as np
import math
class Algo2(object):
    def __init__(self):
        print("use Algo2")

    # read and combine the csv file in `data_path`
    def _get_original_data(self, data_path):
        if os.path.exists('Combine.csv') :
            os.remove('Combine.csv')
        files = os.listdir(data_path)
        for file in files:
            path = data_path + file
            rf = open(path,'rb').read()
            with open('Combine.csv', 'ab') as f:
                f.write(rf)
        original_data = np.genfromtxt('Combine.csv', delimiter=',')
        print("get original data")
        return original_data

    # return the ultimate data
    def get_data(self, data_path):
        return self._get_original_data(data_path)

    # for Algo2, calculate the distance should consider the theta
    def calculate_distance(self, pointA, pointB):
        diff_theta = pointA[0] - pointB[0]
        diff_r = pointA[1] - pointB[1]
        # the distance should be in (0,pi)
        if abs(diff_theta) > math.pi:
            diff_theta = 2 * math.pi - abs(diff_theta)
        distance = math.sqrt(diff_theta ** 2 + diff_r ** 2)
        return distance

    # alg2 compute the mean value of the points
    def calculate_mean_point(self, points):
        cos_sum = float(0)
        sin_sum = float(0)
        r_sum = float(0)
        mean_theta = float(0)
        mean_r = float(0)
        N = len(points)
        for point in points:
            # [theta, r]
            cos_sum += math.cos(point[0])
            sin_sum += math.sin(point[0])
            r_sum += point[1]
            # the return of `atan2` is [-pi, pi], if the return < 0
            # plus 2pi to the positive
            mean_theta = math.atan2(sin_sum, cos_sum)
            if mean_theta < 0 :
                mean_theta += 2 * math.pi
            mean_r = r_sum / N
        mean_point = [mean_theta, mean_r]

        # compute the variance
        # use the way of calculating distance in algorithm 2
        var_sum = float(0)
        variance = float(0)
        for point in points:
            var_sum += (self.calculate_distance(point, mean_point)) ** 2
        variance = var_sum / (N - 1)

        # return the table of mean and variance of the cluster
        # the table key is the index of the cluster, the value is corresponding value
        return mean_point, variance