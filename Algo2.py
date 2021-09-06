"""
The implemention of Algorithm2
"""

import os
import numpy as np
import math
class Algo1(object):
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