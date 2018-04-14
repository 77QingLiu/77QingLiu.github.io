
## KNN 概述

`这篇文章旨在介绍简单而强大的机器学习算法：k-近邻（kNN, k-NearestNeighbor）`
`k-近邻算法是一种基本分类与回归方法，我们这里只讨论分类问题中的 k-近邻算法。`

**一句话总结：近朱者赤近墨者黑！**

`k 近邻算法的输入为实例的特征向量，对应于特征空间的点；输出为实例的类别，可以取多类。k 近邻算法假设给定一个训练数据集，其中的实例类别已定。分类时，对新的实例，根据其 k 个最近邻的训练实例的类别，通过多数表决等方式进行预测。因此，k近邻算法不具有显式的学习过程。`

`尽管K近邻算法很简单，但是它也能成为一个强大的分类器，在经济预测，数据压缩，基因等领域有着重要的应用。`

## KNN 原理

> KNN 工作原理

1. 假设有一个带有标签的样本数据集（训练样本集），其中包含每条数据与所属分类的对应关系。
2. 输入没有标签的新数据后，将新数据的每个特征与样本集中数据对应的特征进行比较。
    1. 计算新数据与样本数据集中每条数据的距离。有很多种度量距离的公式，最常用的是欧式距离。   
    {% raw %}$$ d(x, y) = \sqrt{{(x_1-y_1)}^{2}+{(x_2-y_2)}^{2}+...+{(x_n-y_n)}^{2}} = \sqrt{\sum\limits_{i=1}^{n}(x_i-y_i)^{2}} $${% endraw %}
    2. 对求得的所有距离进行排序（从小到大，越小表示越相似）。
    3. 取前 k （k 一般小于等于 20 ）个样本数据对应的分类标签。
3. 求 k 个数据中出现次数最多的分类标签作为新数据的分类。

> KNN 通俗理解

给定一个训练数据集，对新的输入实例，在训练数据集中找到与该实例最邻近的 k 个实例，这 k 个实例的多数属于某个类，就把该输入实例分为这个类。

> KNN 开发流程

```
收集数据：任何方法
准备数据：距离计算所需要的数值，最好是结构化的数据格式
分析数据：任何方法
训练算法：此步骤不适用于 k-近邻算法
测试算法：计算错误率
使用算法：输入样本数据和结构化的输出结果，然后运行 k-近邻算法判断输入数据分类属于哪个分类，最后对计算出的分类执行后续处理
```

> KNN 算法特点

```
优点：精度高、对异常值不敏感、无数据输入假定
缺点：计算复杂度高、空间复杂度高
适用数据范围：数值型和标称型
```

## kNN案例分析

#### 从头开始实现kNN算法
不需要费太多劲就可以写出一套python程序实现kNN。这里我们使用加州大学欧文机器学习库里面的鸢尾花数据集（IFD）。这个数据集在1936年由著名统计学家费舍尔首次引入，由来自三种鸢尾属（Iris setosa，Iris virginica和Iris versicolor）的每一种的50个观测值组成。从每个样品测量四个特征：萼片和花瓣的长度和宽度。 我们的目标是训练KNN算法，以便能够根据4个特征的测量结果来区分物种。
![iris](/img/in-post/machine-learning-in-action-knn/iris.png)

> 初始化安装包

```python
from numpy import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.neighbors import KNeighborsClassifier
from sklearn import neighbors, datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import pandas as pd
import operator
```

> 准备数据

主要分为两块：
1. 从sklearn读入特征信息(包括iris.data和iris.target)
2. 将数据分割成训练和测试数据集

```python
def _loadData(self):
    iris = datasets.load_iris()
    # 这里将target的shape从(n, ) 改成(n, 1)
    iris.target.shape = (iris.target.shape[0], 1)
    X = iris.data
    Y = iris.target
    # 分割成训练和测试数据集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    return X_train, X_test, Y_train, Y_test
```

> 绘图

下图中用iris的花瓣长度作为X轴，宽度作为Y轴。然后按不同的物种作为分组，标记不同的颜色
![iris_petal](/img/in-post/machine-learning-in-action-knn/iris-petal.png)

快速研究上图可以发现很强的分类特征。我们观察到setosas有小花瓣，versicolor有中等大小的花瓣，virginica有最大的花瓣。

> 归一化数据

在建立模型之前，有一件很重要的操作-**归一化数据**

* 归一化数据 （归一化是一个让权重变为统一的过程，更多细节请参考： [zhihu](https://www.zhihu.com/question/19951858
)

| 序号 | 玩视频游戏所耗时间百分比 | 每年获得的飞行常客里程数  | 每周消费的冰淇淋公升数  | 样本分类 |
| ------------- |:-------------:| -----:| -----:| -----:|
| 1 | 0.8 | 400     | 0.5 | 1 |
| 2 | 12  | 134 000 | 0.9 | 3 |
| 3 | 0   | 20 000  | 1.1 | 2 |
| 4 | 67  | 32 000  | 0.1 | 2 |

样本3和样本4的距离：
$$\sqrt{(0-67)^2 + (20000-32000)^2 + (1.1-0.1)^2 }$$

这里每年获得的飞行常客里程数数值特别大，完全覆盖了其他变量产生的影响。
归一化特征值，就是为了消除特征之间量级不同导致的影响

**归一化操作：**    
这里直接用线性函数转换`y=(x-MinValue)/(MaxValue-MinValue)`   
说明：x、y分别为转换前、后的值，MaxValue、MinValue分别为样本的最大值和最小值。通过转换之后，变量的取值范围都变成了0-1。

具体实现程序如下：
```python
def _autoNorm(self, dataSet):
    """
    Desc:
        归一化特征值，消除特征之间量级不同导致的影响
    parameter:
        dataSet: 数据集
    return:
        归一化后的数据集 normDataSet.  ranges和minVals即最小值与范围.

    归一化公式：
        Y = (X-Xmin)/(Xmax-Xmin)
        其中的 min 和 max 分别是数据集中的最小特征值和最大特征值。该函数可以自动将数字特征值转化为0到1的区间。
    """
    # 计算每种属性的最大值、最小值、范围
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    # 极差
    ranges      = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m           = dataSet.shape[0]
    # 生成与最小值之差组成的矩阵
    normDataSet = dataSet - tile(minVals, (m,1))
    # 将最小值之差除以范围组成矩阵
    normDataSet = normDataSet / tile(ranges, (m,1))
    return normDataSet
```

> 建立预测模型

`
kNN 算法伪代码：

  对于每一个在数据集中的数据点：   
      计算目标的数据点（需要分类的数据点）与该数据点的距离   
      将距离排序：从小到大   
      选取前K个最短距离   
      选取这K个中最多的分类类别   
      返回该类别来作为目标数据点的预测值  
`
```python
def predict(self, X_train, Y_train, X_predict, k):
  # create list for distances and targets
    distances = []
    targets = []

    # 距离度量 度量公式为欧氏距离
    diffMat     = tile(X_predict, (X_train.shape[0], 1)) - X_train
    sqDiffMat   = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances   = sqDistances**0.5
    # 将距离排序：从小到大
    sortedDistIndicies = distances.argsort()
    #选取前K个最短距离， 选取这K个中最多的分类类别
    classCount={}
    for i in range(k):
        voteIlabel = Y_train[sortedDistIndicies[i]][0]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
```

> 模型测试

```python
def kNearestNeighbor(self):
    X_train, X_test, Y_train, Y_test = self.data

  # normalize the matrix
    X_train = self._autoNorm(X_train)
    X_test = self._autoNorm(X_test)

  # loop over all observations
    predictions = []
    for i in range(len(X_test)):
        predictions.append(self.predict(X_train, Y_train, X_test[i, :], self.neighbor))

    predictions = np.asarray(predictions)
    # evaluating accuracy
    accuracy = accuracy_score(Y_test, predictions)
    print('\nThe accuracy of our classifier is {0}%'.format(accuracy*100))
```
运行的效果如下：
```python
>>> iris = kNearestNeighbor()
The accuracy of our classifier is 97%
```
效果很不错！

> 交叉验证

这里使用k重交叉验证的方法，具体的原理直接看图。
![cross_validation](/img/in-post/machine-learning-in-action-knn/cross-validation.png)
简单来说就是将原始数据集分成k份，从中选k-1份作为训练数据集，另外一份当作测试数据集。每次选择不同的测试集，重复k次验证

具体的代码实现：
```python
def crossValidation(self, X_train, Y_train):
    # creating odd list of K for KNN
    myList = list(range(1,50))

    # subsetting just the odd ones
    neighbors = list(filter(lambda x: x % 2 != 0, myList))

    # empty list that will hold cv scores
    cv_scores = []

    # perform 10-fold cross validation
    for k in neighbors:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_train, Y_train, cv=10, scoring='accuracy')
        cv_scores.append(scores.mean())

    # changing to misclassification error
    MSE = [1 - x for x in cv_scores]

    # determining best k
    optimal_k = neighbors[MSE.index(min(MSE))]
    print("The optimal number of neighbors is {0}".format(optimal_k))

    # plot misclassification error vs k
    plt.plot(neighbors, MSE)
    plt.xlabel('Number of Neighbors K')
    plt.ylabel('Misclassification Error')
    plt.show()
```
![cross](/img/in-post/machine-learning-in-action-knn/cross.png)

可以看到随着k值的增大，误分类逐渐增多。

#### 使用sklearn实现kNN
```python
class kNN_scilearn:
    def __init__(self):
        pass

    def fitModel(self):
        X_train, X_test, Y_train, Y_test = self._loadData()
        # MinMax标准化
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train = min_max_scaler.fit_transform(X_train)
        X_test = min_max_scaler.fit_transform(X_test)
        # instantiate learning model (k = 3)
        knn = KNeighborsClassifier(n_neighbors=3)
        # fitting the model
        knn.fit(X_train, Y_train)
        # predict the response
        pred = knn.predict(X_test)
        # evaluate accuracy
        print(accuracy_score(Y_test, pred))
        X = np.concatenate((X_train, X_test), axis=0)
        Y = np.concatenate((Y_train, Y_test), axis=0)
        # reshape to (n, )
        Y  = Y .reshape(Y.shape[0],)
        self.crossValidation(X, Y)

    def _loadData(self):
        iris = datasets.load_iris()
        iris.target.shape = (iris.target.shape[0], 1)
        X = iris.data
        Y = iris.target
        # split into train and test
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
        return X_train, X_test, Y_train, Y_test
```

## KNN 小结

经过上面的介绍我们可以知道， k 近邻算法有 三个基本的要素：

* k 值的选择

    * k 值的选择会对 k 近邻算法的结果产生重大的影响。
    * 如果选择较小的 k 值，就相当于用较小的邻域中的训练实例进行预测，“学习”的近似误差（approximation error）会减小，只有与输入实例较近的（相似的）训练实例才会对预测结果起作用。但缺点是“学习”的估计误差（estimation error）会增大，预测结果会对近邻的实例点非常敏感。如果邻近的实例点恰巧是噪声，预测就会出错。换句话说，k 值的减小就意味着整体模型变得复杂，容易发生过拟合。
    * 如果选择较大的 k 值，就相当于用较大的邻域中的训练实例进行预测。其优点是可以减少学习的估计误差。但缺点是学习的近似误差会增大。这时与输入实例较远的（不相似的）训练实例也会对预测起作用，使预测发生错误。 k 值的增大就意味着整体的模型变得简单。
    * 近似误差和估计误差，请看这里：[zhihu](https://www.zhihu.com/question/60793482)
     - 近似误差越小，对本数据集的预测效果就越好，但是不保证其他数据集的预测效果
     - 估计误差越小，对世界上所有相类似的数据集总体预测效果越好，对本数据集的预测效果不一定越好

  k值为1
  ![k-1](/img/in-post/machine-learning-in-action-knn/k-1.png)

  k值为2
  ![k-2](/img/in-post/machine-learning-in-action-knn/k-2.png)

* 距离度量

    * 特征空间中两个实例点的距离是两个实例点相似程度的反映。
    * k 近邻模型的特征空间一般是 n 维实数向量空间 $$ \mathbf{R}^{n} $$ 。使用的距离是欧氏距离，但也可以是其他距离，如更一般的 $$ \mathbf{L}_{p} $$ 距离，或者 Minkowski 距离。

* 分类决策规则

    * k 近邻算法中的分类决策规则往往是多数表决，即由输入实例的 k 个邻近的训练实例中的多数类决定输入实例的类。

## 参考资料
* [羊三，小瑶 - k-近邻算法](https://github.com/apachecn/MachineLearning/blob/master/docs/2.k-%E8%BF%91%E9%82%BB%E7%AE%97%E6%B3%95.md)
* [A Complete Guide to K-Nearest-Neighbors with Applications in Python and R](https://kevinzakka.github.io/2016/07/13/k-nearest-neighbor/)
