import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean

class Visualize_Plot(object):
    def __init__(self, original_points, cluster_class, mean_points, data_path, algo_name, bandwidth, threshold):
        self.fig = plt.figure()
        self.picture = self.fig.add_subplot(111)
        self.original_points = original_points
        self.cluster_class = cluster_class
        self.mean_points = np.array(mean_points)
        # used to save the parameter to save the figure
        self.data_path = data_path
        self.algo_name = algo_name
        self.bandwidth = bandwidth
        self.threshold = threshold
        return

    # plot the original data
    # [original_points] : the original data from csv file
    # [cluster_class] : the cluster_class[i] = k is the kth cluster
    def plot_ori_cluster_points(self):
        p_ori_theta = self.original_points[:,0]
        p_ori_r = self.original_points[:,1]
        ori_scatter = self.picture.scatter(p_ori_theta, p_ori_r, s = 5, c = self.cluster_class)

        p_cluster_theta = self.mean_points[:,0]
        p_cluster_r = self.mean_points[:,1]
        cluster_scatter = self.picture.scatter(p_cluster_theta, p_cluster_r, s = 15, c = 'r', marker = 'x')

        self.picture.set_xlabel('theta')
        self.picture.set_ylabel('r')
        self.picture.legend((ori_scatter, cluster_scatter), ('original_points', 'cluster_points'), loc = 0)
        plt.colorbar(ori_scatter)

        # delete dir and .csv in the string of data_path
        self.data_path = self.data_path.replace('data/','')
        self.data_path = self.data_path.replace('.csv','')

        res_path = self.data_path + '_' + self.algo_name + '_' + str(self.bandwidth) + '_' +str(self.threshold)
        self.fig.savefig(res_path + '.png')



