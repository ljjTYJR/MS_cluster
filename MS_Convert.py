"""
basic idea :
Since linear data can be dealt easily, can the original data be converted to linear data?
The theta is the angle, and r is the radius
"""
import shutil
from sys import path
import numpy as np
from numpy import genfromtxt
import os
import math
import matplotlib.pyplot as plt

class MS_Convert(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.dis_threshold = 0.0000001

    # get the all original data
    def get_original_data(self):
        if os.path.exists('Combine.csv') :
            os.remove('Combine.csv')
        files = os.listdir(self.data_path)
        for file in files:
            path = self.data_path + file
            rf = open(path,'rb').read()
            with open('Combine.csv', 'ab') as f:
                f.write(rf)
        original_data = genfromtxt('Combine.csv', delimiter=',')
        print("get original data")
        return original_data

    #  convert the data of (theta, r) to (x,y)
    def get_processed_data(self):
        original_data = self.get_original_data()
        processed_data = []
        for data in original_data:
            theta = data[0]
            r = data[1]
            processed_data.append([r * math.cos(theta), r * math.sin(theta)])
        processed_data = np.array(processed_data)
        print("get processed data")
        return processed_data

    # cal the kernel by difference of point and set
    def kernel(self, point_diff, band_width):
        """
        the weight is computed by kernel function
        e^{- sqrt((xi - x) / h) ^ 2}
        """
        # TODO:是否需要带系数？
        weights = (1/(band_width*math.sqrt(2*math.pi))) * np.exp(-0.5 * np.sqrt((((point_diff / band_width)**2).sum(axis=1))))
        return weights

    def cal_dist(self, pointA, pointB):
        res = float(0)
        for i in range(len(pointA)):
            diff = pointA[i] - pointB[i]
            res += diff ** 2
        return np.sqrt(res)

    def shift_point(self, p_old, points, band_width):
        diff = p_old - points
        weights = self.kernel(diff, band_width)
        p_new_x = float(0)
        p_new_y = float(0)
        i = 0
        weights_sum = float(0)
        for p_tmp in points:
            # cal the numerator of MS
            p_new_x += p_tmp[0] * weights[i]
            p_new_y += p_tmp[1] * weights[i]
            weights_sum += weights[i]
            i = i + 1
        p_new_x /= weights_sum
        p_new_y /= weights_sum
        return [p_new_x, p_new_y]
    """
    cluster the processed data
        @points:the raw processed point data
        @bandwith:the bandwith of
    """
    def clustering(self, points, band_with):
        # initialize a max_distance greater than threshold
        max_distance = self.dis_threshold + 1
        # flag to reveal whether the point need to iterate
        end_flag = [False] * points.shape[0]
        # initialize an iteratoring array
        shifting_points = points
        iteration_times = 0

        while max_distance > self.dis_threshold:
            iteration_times += 1
            # update the points in shifting_points sumptuously
            for i in range(len(points)):
                max_distance = 0
                # if the point has got close enough already
                if end_flag[i] : continue
                # the old point in shifting array
                p_old = shifting_points[i]
                # get the new point after one iteration
                p_new = self.shift_point(p_old, points, band_with)
                old_new_dist = self.cal_dist(p_new, p_old)
                print("dis=", old_new_dist)
                # cal the distance of old point and new point, compare it with threshold
                # get the max distance in the shifting points
                if old_new_dist > max_distance:
                    max_distance = old_new_dist

                if old_new_dist < self.dis_threshold:
                    end_flag[i] = True
                shifting_points[i] = p_new
        print("iteration times = ", iteration_times)
        return shifting_points


if __name__ == '__main__' :
    MS = MS_Convert(data_path='original_data/')
    data = MS.get_processed_data()
    res_points = MS.clustering(data, band_with=1)
    print(res_points)
    x = res_points[:,0]
    y = res_points[:,1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scatter = ax.scatter(x,y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.colorbar(scatter)
    fig.savefig("aaa")


