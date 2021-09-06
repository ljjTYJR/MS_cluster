"""
MS(Mean Shift) algorithm to be employed directly on the raw data with (theta, r)
"""

import shutil
from sys import path
import numpy as np
from numpy import genfromtxt
import os
import math
import matplotlib.pyplot as plt

# The class for the algorithm for MeanShift Algo
class MS_Direct(object):
    def __init__(self, data_path):
        self.data_path = data_path

    # read the data from the dir of `../original_data` and return
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

    # Use the kernel function to compute the weight of the point set, return the weights
    # @point : the point to iterate
    # @points : the sampling set
    # @band_width : ~
    def kernel(self, point, points, band_width):
        weights = []
        for p_tmp in points:
            diff_tmp = self.cal_dist(point, p_tmp)
            norm = (diff_tmp ** 2) / (band_width ** 2)
            density_estimation = (1 / (band_width * math.sqrt(2 * math.pi))) * math.exp(-0.5 * norm)
            weights.append(density_estimation)
        return weights

    # calcaulate the `distance` between two points
    def cal_dist(self, pointA, pointB):
        diff_theta = pointA[0] - pointB[0]
        diff_r = pointA[1] - pointB[1]
        # the distance should be in (0,pi)
        if abs(diff_theta) > math.pi:
            diff_theta = 2 * math.pi - abs(diff_theta)
        distance = math.sqrt(diff_theta ** 2 + diff_r ** 2)
        return distance

    # Use the Mean Shift to generate the new point
    def shift_point(self, p_old, points, band_width):
        weights = self.kernel(p_old, points, band_width)
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

    # compute the bandwidth by N
    def compute_bandwidth(self, points):
        N = len(points)
        dis_arr = []
        for p_tmp in points:
            dis_arr.append(self.cal_dist(p_tmp, [0,0]))
        # compute the standard standard deviation
        data_std = np.std(np.array(dis_arr), ddof=1)
        print("set bandwidth=",(1.05 * data_std) * (pow(N, -0.2)))
        return (1.05 * data_std) * (pow(N, -0.2))


    # input the original points data, return the clustering points array
    def clustering(self, points, dis_threshold, band_width=None):
        # creating the shifting points to record next point after iteration
        shifting_points = np.array(points)
        points = np.array(points)

        # initialize a max_distance greater than threshold
        max_distance = dis_threshold + 1
        # flag to reveal whether the point need to iterate
        end_flag = [False] * points.shape[0]
        # record the iteratoring time
        iteration_times = 0

        # if not setting the bandwidth, set the bandwidth by N
        if band_width is None:
            band_width = self.compute_bandwidth(points)

        while max_distance > dis_threshold:
            iteration_times += 1
            print("iteration times =", iteration_times, ",", "max_distance=", max_distance)
            # update the points in shifting_points sumptuously
            for i in range(len(points)):
                max_distance = 0
                # if the point has got close enough already
                if end_flag[i] : continue
                # the old point in shifting array
                p_old = shifting_points[i]
                # get the new point after one iteration
                p_new = self.shift_point(p_old, points, band_width)
                old_new_dist = self.cal_dist(p_new, p_old)
                # cal the distance of old point and new point, compare it with threshold
                # get the max distance in the shifting points
                if old_new_dist > max_distance:
                    max_distance = old_new_dist

                if old_new_dist < dis_threshold:
                    end_flag[i] = True
                shifting_points[i] = p_new
        return shifting_points





if __name__ == '__main__':
    MS = MS_Direct(data_path='../original_data/')

    # get the original data
    original_data = MS.get_original_data()
    if os.path.exists('original_data.csv'):
        os.remove('original_data.csv')
    np.savetxt("original_data.csv", original_data, delimiter=',')

    # get the result after the clustering
    center_points = MS.clustering(points=original_data, dis_threshold=0.00001, band_width=None)
    if os.path.exists('res_data.csv'):
        os.remove('res_data.csv')
    np.savetxt("res_data.csv", center_points, delimiter=',')

    # plot the points
    fig = plt.figure()

    original_data = np.array(original_data)
    picture = fig.add_subplot(111)
    p_ori_x = original_data[:,0]
    p_ori_y = original_data[:,1]
    scatter_original = picture.scatter(p_ori_x,p_ori_y,s=5,c='b')

    p_cen_x = center_points[:,0]
    p_cen_y = center_points[:,1]
    scatter_center = picture.scatter(p_cen_x,p_cen_y,s=10,c='r')

    picture.set_xlabel('theta')
    picture.set_ylabel('r')
    plt.colorbar(scatter_original)
    plt.colorbar(scatter_center)

    # save the plot
    fig.savefig("res_plt")
