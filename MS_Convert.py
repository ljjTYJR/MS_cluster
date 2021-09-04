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
        # dis_threshold = 0.0000000000001

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
    def get_processed_data(self, original_data):
        processed_data = []
        for data in original_data:
            theta = data[0]
            r = data[1]
            processed_data.append([r * math.cos(theta), r * math.sin(theta)])
        print("get processed data")
        return processed_data

    # cal the kernel by difference of point and set
    def kernel(self, point_diff, band_width):
        # TODO:是否需要带系数？
        # weights = (1/(band_width*math.sqrt(2*math.pi))) * np.exp(-0.5 * np.sqrt((((point_diff / band_width)**2).sum(axis=1))))
        weights = []
        for diff in point_diff:
            norm = ((diff[0] ** 2) + (diff[1] ** 2)) / (band_width ** 2)
            density_estimation = (1 / (band_width * math.sqrt(2 * math.pi))) * math.exp(-0.5 * norm)
            weights.append(density_estimation)
        return weights

    def cal_dist(self, pointA, pointB):
        res = float(0)
        for i in range(len(pointA)):
            diff = pointA[i] - pointB[i]
            res += diff ** 2
        return math.sqrt(res)

    def shift_point(self, p_old, points, band_width):
        diff = p_old - points
        weights = np.array(self.kernel(diff, band_width))
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
    def clustering(self, points, band_with, dis_threshold):
        # creating the shifting points to record next point after iteration
        shifting_points = np.array(points)
        points = np.array(points)

        # initialize a max_distance greater than threshold
        max_distance = dis_threshold + 1
        # flag to reveal whether the point need to iterate
        end_flag = [False] * points.shape[0]
        # record the iteratoring time
        iteration_times = 0

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
                p_new = self.shift_point(p_old, points, band_with)
                old_new_dist = self.cal_dist(p_new, p_old)
                # cal the distance of old point and new point, compare it with threshold
                # get the max distance in the shifting points
                if old_new_dist > max_distance:
                    max_distance = old_new_dist

                if old_new_dist < dis_threshold:
                    end_flag[i] = True
                shifting_points[i] = p_new
        return shifting_points


if __name__ == '__main__' :

    MS = MS_Convert(data_path='original_data/')
    # read original data
    original_data = MS.get_original_data()
    if os.path.exists('original_data.csv'):
        os.remove('original_data.csv')
    np.savetxt("original_data.csv", original_data, delimiter=',')

    # convert (angle,r) -> (x,y)
    processed_data = MS.get_processed_data(original_data)
    if os.path.exists('processed_data.csv'):
        os.remove('processed_data.csv')
    np.savetxt("processed_data.csv", processed_data, delimiter=',')

    center_points = MS.clustering(processed_data, band_with=1, dis_threshold=0.00001)
    if os.path.exists('res_data.csv'):
        os.remove('res_data.csv')
    np.savetxt("res_data.csv", center_points, delimiter=',')

    # plot the points
    fig = plt.figure()

    processed_data = np.array(processed_data)
    picture = fig.add_subplot(111)
    p_ori_x = processed_data[:,0]
    p_ori_y = processed_data[:,1]
    scatter_original = picture.scatter(p_ori_x,p_ori_y,s=5,c='b')

    p_cen_x = center_points[:,0]
    p_cen_y = center_points[:,1]
    scatter_center = picture.scatter(p_cen_x,p_cen_y,s=10,c='r')

    picture.set_xlabel('x')
    picture.set_ylabel('y')
    plt.colorbar(scatter_original)
    plt.colorbar(scatter_center)

    # save the plot
    fig.savefig("res_plt")



