对数几率回归（Logistic Regression），简称为对率回归，也称逻辑斯蒂回归，或者逻辑回归，是统计学习中经典的分类模型。Logisitc模型是广义线性模型中的一类。在业界有相关广泛的应用。常见的如信用评分模型，用于判定某个人的违约概率。    
这里从统计学角度，引用周志华西瓜书里的思路，从线性回归开始，逐步讲Logistic回归。

## 线性回归
给定一个由$$d$$个属性描述的示例 $$x = (x_1;x_2;...;x_d)$$，其中$$x_i$$是$$x$$在第$$i$$个属性上的取值，线性模型试图学得一个通过属性的线性组合来进行预测的函数，即\\[f(x) = \theta_1x_1 + \theta_2x_2 + ... + \theta_dx_d + b\\]
一般用向量形式写成\\[f(x) = \theta^Tx + b\\]
通过最小二乘法，可以拟合得到如下图形
![linear](http://img.77qingliu.com/18-5-1/73773701.jpg)
我们通过这个模型，可以计算预测值，以逼近真实标记值。

线性模型很简单，也很容易理解。但是真实世界中，并不是所有数据都是简单的线性关系。那么，我们能否令模型的预测值逼近$$f(x)$$的衍生物呢？例如，假设我们认为观测与输出是在指数尺度上变化，那就可以将输出的对数作为模型逼近的目标，即\\[ln(f(x)) = \theta^Tx + b\\]
这就是对数线性回归，它实际上是在试图让$$e^{\theta^Tx + b}$$逼近$$f(x)$$。在形式上仍然是线性回归。这里的对数函数起到了将线性回归和真实值联系起来的作用。
![](http://img.77qingliu.com/18-5-1/16063290.jpg)

更一般地，考虑单调可微函数$$g(\cdot)$$，令\\[f(x) = g^{-1}(\theta^Tx + b)\\]，
这样得到的模型称为“广义线性模型”，其中函数$$g(\cdot)$$称为“联系函数”。

## Logistic回归
上面我们讨论了线性回归，但是如果要做分类任务该怎么办？答案就在上述“广义线性模型”中：只需要找到一个单调可微的函数将预测值变为分类值。   
符合这个函数有很多，其中一种就是[Sigmoid函数](https://en.wikipedia.org/wiki/Sigmoid_function)（[为什么 LR 模型要使用 sigmoid 函数](https://www.zhihu.com/question/35322351)）：\\[\sigma(z) = \frac{1}{1 + e^{-z}}\\]，
Sigmoid函数的图像：
![](http://img.77qingliu.com/18-5-1/97974721.jpg)

从图中可看出，Sigmoid函数将输出转化为一个接近0或接近1的$$y$$值。将Sigmoid函数作为$$g^{-1}(\cdot)$$代入广义线性模型中，得到\\[f(x) = \frac{1}{1 + e^{-(\theta^Tx + b)}}\\]

上式可变化为\\[ln\frac{y}{1 - y} = \theta^Tx + b\\]
若将$$y$$视作样本$$x$$作为正例的可能性，则$$1-y$$是其反例可能性，两者的比值\\[\frac{y}{1-y}\\]称为“几率”(odds)。反映了$$x$$取正例相对反例的可能性。对几率取对数则得到“对数几率”\\[ln\frac{y}{1-y}\\]，由此看出，logistic回归实际上在用线性回归模型的预测结果去逼近真实结果的”对数几率“，因此，Logistic回归又被称作”对数几率回归“。

## 模型参数估计
对于给定的数据集 $$T = \{(x_1, y_1), (x_2, y_2), ..., (x_n, y_n)\}$$，其中，$$y_i \in \{0, 1\}$$。Logistic回归的参数可以应用”极大似然估计法“进行估计。模型可重写为\\[ln\frac{p(y=1|x)}{p(y=0|x)} = \theta^Tx + b\\]显然有\\[p(y=1|x) = \frac{e^{\theta^Tx + b}}{1 + e^{\theta^Tx + b}}\\]\\[p(y=0|x) = \frac{1}{1 + e^{\theta^Tx + b}}\\]设$$P(Y=1|x) = \pi(x), P(Y=0|x) = 1 - \pi(x)$$    
则似然函数为\\[\prod_{i=1}^N[{\pi(x_i)}]^{y_i}[{1-\pi(x_i)}]^{1-y_i}\\]对数似然函数为\\[\begin{equation}\begin{aligned} L(\theta) &= \sum_{i=1}^N[ y_i\ln\pi(x_i) + (1-y_i)\ln(1-\pi(x_i)) ] \\\\&= \sum_{i=1}^N\left[ y_i\ln\frac{\pi(x_i)}{1-\pi(x_i)} + \ln(1-\pi(x_i)) \right] \\\\ &=\sum_{i=1}^N[ y_i\cdot(\theta^T{\cdot}x_i) - \ln(1+e^{\theta^T{\cdot}x_i}) ] \end{aligned}\end{equation}\\]对$$L(\theta)$$求极大值，得到$$\theta$$的估计值。上式是关于$$\theta$$的高阶可导连续凸函数，根据凸优化理论，经典的数值优化方法如梯度下降法、牛顿法等都可以求得其最优解。

## 梯度下降法
要找到某函数的最大值（或最小值），最好的方法是沿着该函数的梯度方向探寻。如果梯度记为$$\nabla$$，则函数$$J(\theta)$$的梯度由下式表示\\[\nabla_{\theta}J(\theta) = \frac{d}{d\theta}J(\theta)\\]
![](http://img.77qingliu.com/18-5-1/5633285.jpg)
梯度算子总是指向函数值增长最快的方向，梯度上升算法到达每个点后都会重新估计移动的方向，并沿着新的梯度方向移动。如此循环迭代，直到满足停止条件。迭代过程中，梯度算子总是保证我们能选取到最佳的移动方向。这里所说的是移动方向，而未提到移动量的大小。该量值称为步长，记作 α。梯度上升算法的迭代公式如下:
![](http://img.77qingliu.com/18-5-1/98671989.jpg)

**梯度下降算法**
1. 选取一个合适的步长α（比较常见的步长：0.001, 0.003, 0.01, 0.03, 0.1, 0.3）
2. 随机选取一组参数的值
3. 计算这个当前参数的梯度$$\frac{d}{d\theta}J(\theta)$$， 沿着梯度的反方向，根据步长计算新的参数的值
4. 重复上述步骤直到损失函数收敛到一定值

对于Logistic回归来说。记\\[\begin{equation}\begin{aligned}J(\theta) &= -\frac{1}{n}L(\theta) \\\\ &= -\frac{1}{n} \sum_{i=1}^N[ y_i\cdot(\theta^T{\cdot}x_i) - \ln(1+e^{\theta^T{\cdot}x_i}) ]\end{aligned}\end{equation}\\]其中：\\[\begin{equation}\begin{aligned}&\theta^Tx = \theta_0 + \theta_1x_1 + \theta_2x_2 + ... + \theta_dx_d \\\\ &\frac{\partial(\theta^Tx)}{\partial(\theta_j)} = x_j^{(i)}\end{aligned}\end{equation}\\]，要求$$L(w)$$的最大值等价于求$$J(\theta)$$的最小值。    
对$$J(\theta)$$求梯度\\[\begin{equation}\begin{aligned}\nabla_{\theta}J(\theta) &= -\frac{1}{n} \sum_{i=1}^N[ y_i - \frac{1}{1 + e^{-\theta^T{\cdot}x_i}}] * \frac{\partial(\theta^Tx)}{\partial(\theta_j)} \\\\ &= \frac{1}{n} \sum_{i=1}^N[ \frac{1}{1 + e^{-\theta^T{\cdot}x_i}} - y_i] * x_j^{(i)} \\\\ &= \frac{1}{n} \sum_{i=1}^N[ Sigmoid(\theta^T{\cdot}x_i) - y_i] * x_j^{(i)}\end{aligned}\end{equation}\\]
确定步长α，根据梯度$$J(\theta)$$反复更新参数的值，即可求出模型的参数。

## 实战
这里使用周志华-机器学习里面的西瓜数据集-使用Logistic回归分类器判断西瓜的好坏。
具体的数据集如下：

  编号 |色泽 |根蒂 |敲声 |纹理 |脐部 |触感 |密度 |含糖率 |好瓜
  -- |-- |-- |-- |-- |-- |-- |-- |-- |--
  1 |青绿 |蜷缩 |浊响 |清晰 |凹陷 |硬滑 |0.697 |0.46 |是
  2 |乌黑 |蜷缩 |沉闷 |清晰 |凹陷 |硬滑 |0.774 |0.376 |是
  3 |乌黑 |蜷缩 |浊响 |清晰 |凹陷 |硬滑 |0.634 |0.264 |是
  4 |青绿 |蜷缩 |沉闷 |清晰 |凹陷 |硬滑 |0.608 |0.318 |是
  5 |浅白 |蜷缩 |浊响 |清晰 |凹陷 |硬滑 |0.556 |0.215 |是
  6 |青绿 |稍蜷 |浊响 |清晰 |稍凹 |软粘 |0.403 |0.237 |是
  7 |乌黑 |稍蜷 |浊响 |稍糊 |稍凹 |软粘 |0.481 |0.149 |是
  8 |乌黑 |稍蜷 |浊响 |清晰 |稍凹 |硬滑 |0.437 |0.211 |是
  9 |乌黑 |稍蜷 |沉闷 |稍糊 |稍凹 |硬滑 |0.666 |0.091 |否
  10 |青绿 |硬挺 |清脆 |清晰 |平坦 |软粘 |0.243 |0.267 |否
  11 |浅白 |硬挺 |清脆 |模糊 |平坦 |硬滑 |0.245 |0.057 |否
  12 |浅白 |蜷缩 |浊响 |模糊 |平坦 |软粘 |0.343 |0.099 |否
  13 |青绿 |稍蜷 |浊响 |稍糊 |凹陷 |硬滑 |0.639 |0.161 |否
  14 |浅白 |稍蜷 |沉闷 |稍糊 |凹陷 |硬滑 |0.657 |0.198 |否
  15 |乌黑 |稍蜷 |浊响 |清晰 |稍凹 |软粘 |0.36 |0.37 |否
  16 |浅白 |蜷缩 |浊响 |模糊 |平坦 |硬滑 |0.593 |0.042 |否
  17 |青绿 |蜷缩 |沉闷 |稍糊 |稍凹 |硬滑 |0.719 |0.103 |否

 根据色泽、根蒂、敲声、纹理、脐部、触感、密度、含糖率这些特征，对测试例1进行分类。

  编号 |色泽 |根蒂 |敲声 |纹理 |脐部 |触感 |密度 |含糖率 |好瓜
  -- |-- |-- |-- |-- |-- |-- |-- |-- |--
  测1 |青绿 |蜷缩 |浊响 |清晰 |凹陷 |硬滑 |0.697 |0.46 |？

**Sklearn代码实现**
读入数据
```python
import numpy as np
from io import StringIO
import pandas as pd
import math
import re
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
def createDataSet():
    ''' 数据读入 '''
    rawData = StringIO(
    """编号,色泽,根蒂,敲声,纹理,脐部,触感,密度,含糖率,好瓜
      1,青绿,蜷缩,浊响,清晰,凹陷,硬滑,0.697,0.46,是
      2,乌黑,蜷缩,沉闷,清晰,凹陷,硬滑,0.774,0.376,是
      3,乌黑,蜷缩,浊响,清晰,凹陷,硬滑,0.634,0.264,是
      4,青绿,蜷缩,沉闷,清晰,凹陷,硬滑,0.608,0.318,是
      5,浅白,蜷缩,浊响,清晰,凹陷,硬滑,0.556,0.215,是
      6,青绿,稍蜷,浊响,清晰,稍凹,软粘,0.403,0.237,是
      7,乌黑,稍蜷,浊响,稍糊,稍凹,软粘,0.481,0.149,是
      8,乌黑,稍蜷,浊响,清晰,稍凹,硬滑,0.437,0.211,是
      9,乌黑,稍蜷,沉闷,稍糊,稍凹,硬滑,0.666,0.091,否
      10,青绿,硬挺,清脆,清晰,平坦,软粘,0.243,0.267,否
      11,浅白,硬挺,清脆,模糊,平坦,硬滑,0.245,0.057,否
      12,浅白,蜷缩,浊响,模糊,平坦,软粘,0.343,0.099,否
      13,青绿,稍蜷,浊响,稍糊,凹陷,硬滑,0.639,0.161,否
      14,浅白,稍蜷,沉闷,稍糊,凹陷,硬滑,0.657,0.198,否
      15,乌黑,稍蜷,浊响,清晰,稍凹,软粘,0.36,0.37,否
      16,浅白,蜷缩,浊响,模糊,平坦,硬滑,0.593,0.042,否
      17,青绿,蜷缩,沉闷,稍糊,稍凹,硬滑,0.719,0.103,否
    """)
    df = pd.read_csv(rawData, sep=",")
    return df
df = createDataSet()
df.head()
```

重新编码数据
```python
# re-encoding
columns = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感']
df_dummy = pd.get_dummies(df, columns=columns)
```
> 重编码问题参考[这篇文章](https://ask.hellobi.com/blog/DataMiner/4897)


建立模型
```python
# Model fitting
LR = LogisticRegression()
x = df_dummy.drop(['好瓜', '编号'], axis=1)
y = df['好瓜']
LR_fit = LR.fit(x, y)
to_predit = x.iloc[0].values.reshape(1, -1)
predit = LR_fit.predict(to_predit)
```

输出结果
```python
def series2string(series):
    string = series.to_string().split('\n')
    s = [re.sub(' +', ': ', s) for s in string]
    return ', '.join(s)
series2string(df.iloc[0].drop(['编号', '好瓜']))
print('The predit value for [{0}] - 好瓜[{1}] '.format(series2string(df.iloc[0].drop(['编号', '好瓜'])), predit[0]))
>> The predit value for [色泽: 青绿, 根蒂: 蜷缩, 敲声: 浊响, 纹理: 清晰, 脐部: 凹陷, 触感: 硬滑, 密度: 0.697, 含糖率: 0.46] = 好瓜[是]
```
最后将测试样例预测为好瓜。

## 参考文档
[机器学习-周志华](https://book.douban.com/subject/26708119/)    
[统计学习方法-李航](https://book.douban.com/subject/10590856/)
