from MS import MeanShift
from DataProcess import DataProcess

if __name__ == '__main__':
    MS = MeanShift(data_path='original_data/', algo_name='Algo1', bandwidth=None, threshold=0.0001)