# Report

## Solution1 : Converting to Euclidean space

The difficulty of clusttering is how to judge the "distance" of two point, Since we can easily compute the Euclidean distance, so the original idea is whether we can convert the data point to the format without direction?

As we all know, the point with the form of polar coordinates can be written as :
$$
x = r\cos(\theta)\\
y = r\sin(\theta)\\
$$
——where $r$ is the radius, and $\theta$ is the angle;

So, with the point of format $p = \left[\begin{matrix} x\\y \end{matrix}\right]$ , we can easily compute the norm of $p$

The code is in the file `MS_Convert.py`.



In the process of dealing with the data, there are some questions:

1. the efficency is low, too much data need to be processed;
2. the parameters (band_width, the threhold) have effects on the result, then how to judge the result?
3. how to choose a kernel function?

## Solution2 : 

