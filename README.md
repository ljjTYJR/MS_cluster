# Report

## Solution 1 : Converting to Euclidean space

### Introduction

The difficulty of clustering is how to judge the "distance" of two point, Since we can easily compute the Euclidean distance, so the original idea is whether we can convert the data point to the format without direction?

As we all know, the point with the form of polar coordinates can be written as :
$$
x = r\cos(\theta)\\
y = r\sin(\theta)\\
$$
——where $r$ is the radius, and $\theta$ is the angle;

So, with the point of format $p = \left[\begin{matrix} x\\y \end{matrix}\right]$ , we can easily compute the norm of $p$

The code is in the directory *MS_Convert/*

### Conclusion

In the process of dealing with the data, there are some questions:

1. the efficiency is low, too much data need to be processed;
2. the parameters (band_width, the threshold) have effects on the result, then how to judge the result?
3. how to choose a kernel function?

### Toto List

- [ ] restore the point with the format of $\left[\begin{matrix} x\\y \end{matrix}\right]$ back to $\left[\begin{matrix} \theta\\r \end{matrix}\right]$ and compute the mean and the variance.
- [ ] Improve the performance of the algorithm.
- [ ] Add the result analysing, the data, the picture(visualisation), the result assessment.

## Solution 2

### Introduction

After I finishing the **solution 1**, I find the maximum consumption of the program is the computation weight in the MS algorithm. The basic idea of MS algorithm is :
$$
m(x) = \frac{\sum_{s\in S'}K(s-x)s}{K(s-x)}
$$
In **solution 1**, I convert the data format to an Euclidean space, to compute the weight $K(s-x)$ , I employ the standard Gaussian kernel function,  and the norm is the Euclidean distance :
$$
distance = \sqrt{(x_{1} - x_{2})^2 + (y_{1} - y_{2})^2 }
$$
Let's go back to the basic idea of the Mean Shift Algorithm, from the reference [Mean Shift, Mode Seeking, and Clustering](./Mean Shift, Mode Seeking, and Clustering.pdf) , we can summarise the steps to employ the algorithm:

1.  Choose a kernel function, including the form and the parameter(bandwidth);
2. Iterate with the MS, until the algorithm converge;
3. Identify the clusters;

### Methods

#### Evaluation of the distance

First, the kernel function is used for probability density function around the point $x$ , the expression $(s-x)$ can be seen as the *distance*  between two point.  So, the basic idea is can we just use data of $(\theta, r)$ to measure the *distance* between two point? For example, similar to Euclidean distance, we can compute by :
$$
distance = \sqrt{(\theta_{1} - \theta_{2})^2 + (r_{1} - r_{2})^2 }
$$
​	However, the variable $\theta$ is angle in $[0, 2 \pi]$, the angle is a kind of periodic variable. That means the real distance between $0$ and $2\pi$ is $0$ , not $2\pi$. Similarly, the distance between $0$ and $\frac{3}{2} \pi$ is $\frac{1}{2} \pi$. As shown below:

<img src="./\pictures\0-23.JPG" style="zoom:50%;" />



​	So, to evaluate the distance between two angle should be :
$$
d(\theta_1, \theta_2) = 
\begin{cases} 
2\pi - |\theta_1 - \theta_2| &|\theta_1 - \theta_2|>\pi\\
|\theta_1 - \theta_2|  &else
\end{cases}
$$
​	The distance function can be written as :
$$
d(v_1,v_2)=(v_1 - v_2) = \sqrt{d^2(\theta_1 - \theta_2) + (r_1 - r_2)^2}
$$
​	——where $v$ is the data point of $v = \left[\begin{matrix} \theta\\r \end{matrix}\right]$

​	The kernel function can choose the Gaussian kernel.

#### Algorithm

##### Mean Shift Process

Assuming $S$ is the sampleing set, $T$ is the "clustering center" set. For a blurring process, letting $S = T$ and the expression:

​	 $p_i$ —— the *ith*  point in the sampling set $S$. 

​	$\epsilon$ —— the threhold of distance.

​	The MS algorithm can be descriped as :

---

For $p_i$ in T:
	Let $shifting\_p = p_i$ 
	Loop :
		Let $p_{old} = shifting\_p$ 
		$p_{new} = MS(p_{old})$ 
		Let $d = d(p_{old}, p_{new})$ 
		$shifting\_p = p_{new}$
		If $d < \epsilon$ :
			Exit loop
		Else :
			Continue

---

##### Parameters

The main parameter of the algorithm MS is the *bandwith* of the kernel function. If the *bandwidth* is too small, there may be a question that the points to be included are not enough. The result can be many clusters. But if the *bandwidth* is too large, this can result in only one cluster in the end.

​	So, there is a trade-off when chossing the parameter. The probability density function $f(x)$ has two parateters : $N$ and $h$. If the size of the sample( $N$ )  is infinity( $N -> \infin$), h should approches zero ($h -> 0$). By this, we can get the relationship between $N$ and $h$ :
$$
h = cN^{-1/5}
$$
​	——where $c$ is a constant	

​	For the gaussian distribution, $h$ is :
$$
\begin{align}
h &= (\frac{4\sigma^5}{3N})^{1/5}\\
&=\frac{1.05 * \sigma}{N^5}
\end{align}
$$
​	——where $\sigma$ is the standard deviation for  the sample.

### Todo List 

- [ ] Modify the format of README to latex, especially algorithm expression.