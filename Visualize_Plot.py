import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean

class Visualize_Plot(object):
    def __init__(self, original_points, cluster_class, mean_points):
        self.fig = plt.figure()
        self.picture = self.fig.add_subplot(111)
        self.original_points = original_points
        self.cluster_class = cluster_class
        self.mean_points = np.array(mean_points)
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
        plt.colorbar(ori_scatter)
        print("funck!!!")
        self.fig.savefig("cluster_res")



