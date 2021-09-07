import numpy
from Algo1 import Algo1
from Algo2 import Algo2
import numpy as np
import math
import sys

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
        # TODO:notice whether this is right
        for p_tmp in self.original_points:
            if self.cluster_record[i] in point_table.keys():
                point_table[self.cluster_record[i]].append(p_tmp)
            else:
                point_table[self.cluster_record[i]] = [p_tmp]
            i += 1
        # iterate the table to calculate the mean of each mean nad var of each cluster
        alg = Algo2()
        for index, group in point_table.items():
            # notice the group's shape
            mean_table[index], var_table[index] = alg.calculate_mean_point(group)

            """
            cos_sum = float(0)
            sin_sum = float(0)
            r_sum = float(0)
            mean_theta = float(0)
            mean_r = float(0)
            N = len(group)
            for point in group:
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
            mean_table[index] = mean_point

            # compute the variance
            # use the way of calculating distance in algorithm 2
            alg2 = Alg2()
            var_sum = float(0)
            variance = float(0)
            for point in group:
                var_sum += (alg2.calculate_distance(point, mean_point)) ** 2
            variance = var_sum / (N - 1)
            var_table[index] = variance

        # return the table of mean and variance of the cluster
        # the table key is the index of the cluster, the value is corresponding value
        """
        return mean_table, var_table



