from Mean_Shift import MeanShift
from Data_Process import DataProcess
from Data_Process import ResultProcess
from Visualize_Plot import Visualize_Plot

if __name__ == '__main__':
    data_path = 'original_data/'
    algo_name = 'Algo2'
    bandwidth = None
    threshold = 0.00001

    MS = MeanShift(data_path = data_path, algo_name = algo_name, bandwidth = bandwidth, threshold = threshold)
    theta_raw_points, original_points, shifting_points = MS.ms_process()

    cluster_distance = 0.5
    DP = DataProcess(shifting_points, cluster_distance = cluster_distance, algo_name = algo_name)
    index_record, cluster_record, groups = DP.data_process()

    RP = ResultProcess(cluster_record, theta_raw_points)
    mean_table, var_table = RP.compute_mean_var()

    mean_points = []
    for point in mean_table.values():
        mean_points.append(point)
    VP = Visualize_Plot(theta_raw_points, cluster_record, mean_points)
    VP.plot_ori_cluster_points()

