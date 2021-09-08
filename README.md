# README

## Introduction

This repository is a simple implemention for Mean Shift(MS) algorithm.

### The structure of the repository 

```
├── Algo1.py
├── Algo2.py
├── data/
├── Data_Process.py
├── Mean_Shift.py
├── README.md
├── Reference/
├── report/
├── res/
├── run.py
└── Visualize_Plot.py
```

Directories here include :

```log
data/			—— The input original data(csv file)
Referencr/		—— The reference paper
report/			—— My report resources
res/			—— the result of different data set / algorithms
```

The python file :

```
Algo1.py		—— The implemention of Algo1
Algo2.py		—— The implemention of Algo2
Mean_Shift.py	—— The process of Mean Shift algorithm
Data_Process.py	—— The data processing methods
Visualize_Plot.py —— The data visualization methods
run.py			—— main function to run the algorithm
```

## How to run

The `main` function is defined in the file `run.py`. 

The main loop of the `run.py` is :

1. Decide what parameters to use, the parameters include : 

   1. data_path : the path of the data, e.g : `data/data1.csv` 

   2. algo_name : to use `Algo1` or `Algo2`, e.g : `Algo1`

   3. bandwidth : the bandwith of kernel function. (If it is set `None`, it means it will compute bandwidth by N).

   4. threshold : the threshold of the mean shift, e.g : `0.00001`

2. By command `python3 run.py` 

3. The log can be shown as :

   ```
   use Algo1
   get original data
   get processed data
   get original data
   set bandwidth= 0.9336688328456105
   iteration times = 1 , max_distance = 1.00001
   iteration times = 2 , max_distance = 0.17686936528050956
   iteration times = 3 , max_distance = 0.04682090822565989
   iteration times = 4 , max_distance = 0.012449725359511938
   iteration times = 5 , max_distance = 0.0033168315077783343
   iteration times = 6 , max_distance = 0.0008840820836842969
   iteration times = 7 , max_distance = 0.00023567080958232224
   iteration times = 8 , max_distance = 6.282444587304013e-05
   iteration times = 9 , max_distance = 1.674764765164474e-05
   use Algo1
   use Algo2
   N= 100
   N= 200
   index = 0 centroid = [6.264581278374883, 4.835123552413281]
   index = 1 centroid = [3.260652115284019, 0.9951555487518141]
   index = 0 variance of cluster = 0.939911335274201
   index = 1 variance of cluster = 0.4847930143675687
   ```

   The last output : 

   ```
   index = 0 centroid = [6.264581278374883, 4.835123552413281]
   index = 1 centroid = [3.260652115284019, 0.9951555487518141]
   index = 0 variance of cluster = 0.939911335274201
   index = 1 variance of cluster = 0.4847930143675687
   ```

   is the centroid and variance of corresponding cluster.

4. The result of points and clusters is shown in the file `data_alg_bandwidth_threshold.png` ， e.g: `data1_Algo1_None_1e-05.png`

## Todo list

- [ ] Multi-threaded optimization;
- [ ] Estimation of different parameters;