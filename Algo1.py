"""
The implemention of Algorithm1
"""

import os
import numpy as np
import math
class Algo1(object):
    def __init__(self):
        print("use Algo1")

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

    # convert the data to the (theta,r)-->(x,y)
    def _get_processed_data(self, original_data):
        processed_data = []
        for data in original_data:
            theta = data[0]
            r = data[1]
            processed_data.append([r * math.cos(theta), r * math.sin(theta)])
        print("get processed data")
        return processed_data

    # return the ultimate data
    def get_data(self, data_path):
        return self._get_processed_data(self._get_original_data(data_path))

    # for Algo1, calculate the distance is compute the Euclidean distance
    def calculate_distance(self, pointA, pointB):
        res = float(0)
        for i in range(len(pointA)):
            diff = pointA[i] - pointB[i]
            res += diff ** 2
        return math.sqrt(res)