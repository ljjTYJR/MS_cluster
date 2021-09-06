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
        distances = []
        for p_tmp in points:
            distances.append(self.alg.calculate_distance(p_tmp, [0,0]))
        # compute the standard standard deviation
        data_std = np.std(np.array(distances), ddof=1)
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

class DataProcess(object):
    def __init__(self, data, cluster_distance):
        self.data = data
        self.cluster_distance = cluster_distance

    # process the data, return the clusters
    def data_process(self):
        shifting_points = self.data.tolist()
        # size = len(shifting_points), cluster_record[i] = k means the ith element in data belongs to k cluster
        cluster_record = []
        # the element `group` in `groups` is the points belong to the same cluster
        groups = []
        # index to record the number of the clusters(group)
        index_record = 0
        # the ith element
        i = 0

        for p_tmp in shifting_points:
            index = self._get_index_of_cluster(p_tmp, groups, self.cluster_distance)
            if index is None:
                # the p_tmp does not belong to any current group, so we need to make a new group
                # append a new group which include the p_tmp
                groups.append([p_tmp])
                cluster_record.append(index_record)
                # create a new index, so increase the index_record
                index_record += 1
            else:
                # the p_tmp belongs to a existed group, add the p_tmp to the groups
                groups[index].append(p_tmp)
                cluster_record.append(index)
            i += 1

        return index_record, cluster_record, groups

    # find the index of cluster that include the point, if point does not belong to, then return None
    def _get_index_of_cluster(self, point, groups, cluster_distance):
        index_res = None
        index_tmp = 0
        for group in groups:
            distance = self._get_distance_to_group(point, group)
            if distance <= cluster_distance:
                index_res = index_tmp
                return index_res
            index_tmp += 1

        return index_res

    # calculate the minium distance between the point and the points in the group
    def _get_distance_to_group(self, point, group):
        distance = sys.float_info.max
        for p_tmp in group:
            distance_tmp = self.alg.calculate_distance(point, p_tmp)
            if distance_tmp < distance:
                distance = distance_tmp
        return distance


if __name__ == '__main__':
    MS = MeanShift(data_path='original_data/', algo_name='Algo1', bandwidth=None, threshold=0.0001)
    MS.ms_process()

