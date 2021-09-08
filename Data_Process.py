import numpy
from numpy.lib.function_base import select
from Algo1 import Algo1
from Algo2 import Algo2
import numpy as np
import math
import sys

class DataProcess(object):
    def __init__(self, data, cluster_distance, algo_name):
        self.data = data
        self.cluster_distance = cluster_distance
        if algo_name == 'Algo1':
            self.alg = Algo1()
        elif algo_name == 'Algo2':
            self.alg = Algo2()


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
        # [index_record] : the number of clusters
        # [cluster_record] : cluster_record[i] = k means the ith element belongs to kth cluster
        # [groups] : the points set in one cluster(the elements are shifting points)
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

# The result process : compute the mean and the variance of the cluster
class ResultProcess(object):
    def __init__(self, cluster_record, original_points):
        self.cluster_record = cluster_record
        # change the np.array to the list
        self.original_points = original_points.tolist()

    def compute_mean_var(self):
        point_table = dict()
        mean_table = dict()
        var_table = dict()
        i = 0
        for p_tmp in self.original_points:
            if self.cluster_record[i] in point_table.keys():
                point_table[self.cluster_record[i]].append(p_tmp)
            else:
                point_table[self.cluster_record[i]] = [p_tmp]
            i += 1
        # iterate the table to calculate the mean of each mean nad var of each cluster
        alg = Algo2()
        for index, group in point_table.items():
            # if the size of group is small, omit it
            if len(group) < 2 :
                continue
            mean_table[index], var_table[index] = alg.calculate_mean_point(group)

        return mean_table, var_table



