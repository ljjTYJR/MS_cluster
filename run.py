from Mean_Shift import MeanShift
from Data_Process import DataProcess
from Data_Process import ResultProcess
from Visualize_Plot import Visualize_Plot

if __name__ == '__main__':
    """
    The parameters set to run the algorithm:
    data_path : the path of the data;
    algo_name : to use `Algo1` or `Algo2`
    bandwidth : the bandwith of kernel function
    threshold : the threshold of the mean shift
    """
    data_path = 'data/data1.csv'
    algo_name = 'Algo1'
    bandwidth = None
    threshold = 0.00001


    MS = MeanShift(data_path = data_path, algo_name = algo_name, bandwidth = bandwidth, threshold = threshold)
    """
    Here,
    theta_raw_points are raw data of format [theta, r]
    original_points : for `Algo1` are processed points
    shifting_points : The points after MS
    """
    theta_raw_points, original_points, shifting_points = MS.ms_process()


    """
    Find the cluster of the data
    """
    cluster_distance = 0.5
    DP = DataProcess(shifting_points, cluster_distance = cluster_distance, algo_name = algo_name)
    index_record, cluster_record, groups = DP.data_process()

    """
    mean_table : the table with dict{index : point}, the index and corresponding mean_point
    var_table : the table with dict{index : variance}, the index and corresponding variance
    """
    RP = ResultProcess(cluster_record, theta_raw_points)
    mean_table, var_table = RP.compute_mean_var()


    """
    Plot raw data and the clusters
    """
    for i, val in mean_table.items():
        print("index =", i, "centroid =", val)
    for i, val in var_table.items():
        print("index =", i, "variance of cluster =", val)
    mean_points = []
    for point in mean_table.values():
        mean_points.append(point)
    VP = Visualize_Plot(theta_raw_points, cluster_record, mean_points, data_path, algo_name, bandwidth, threshold)
    VP.plot_ori_cluster_points()

