# 决策树模型
`
决策树是一种常用的分类和回归机器学习方法，是最经常使用的机器学习算法之一。这里只讨论分类决策树。
决策树模型呈树形结构，在分类问题中，表示基于特征对实例分类的过程。它可以认为是if-then规则的集合，也可以认为是定义在特征空间与类空间上的条件概率分布。    
决策树学习通常包括3个步骤：特征选择、决策树的生成和剪枝。
`

# 决策树场景
这里以机器学习-周志华书中西瓜书数据集为例子。在挑选西瓜的时候，我们要面对“这是好瓜吗？”这样的问题。进行决策时，通常会进行一系列的判断或“子决策”：我们先看“它是什么颜色？”，如果是“青绿色”，则我们再看“它的根蒂是什么形态？”，如果是“卷缩”，我们再判断“它敲起来是什么声音？”，最后，我们得出最终决策：这是一个好瓜。这个决策过程如图所示：
![](http://img.77qingliu.com/18-4-20/48288531.jpg)

# 决策树原理
## 决策树生成算法
如何构造一个决策树？这里采用递归的方法，伪代码如下：
```python
def createBranch():
'''
此处运用了迭代的思想。 感兴趣可以搜索 迭代 recursion， 甚至是 dynamic programing。
'''
    检测数据集中的所有数据的分类标签是否相同:
        If so return 类标签
        Else:
            寻找划分数据集的最好特征（划分之后信息熵最小，也就是信息增益最大的特征）
            划分数据集
            创建分支节点
                for 每个划分的子集
                    调用函数 createBranch （创建分支的函数）并增加返回结果到分支节点中
            return 分支节点
```

## 属性划分选择
决策树学习的关键是根据属性划分子集，也就是如何最优化生成子树。那么怎么划分子树最好呢？一般而言我们希望**随着划分的不断进行，我们希望决策树的分支节点所包含的样本尽可能属于同一类，即节点的“纯度”越来越高**。   
那么如何判断节点的纯度呢？这里使用信息论的算法。

* 信息熵    
信息熵是度量样本集合纯度的最常用指标。假定样本集合D中第k类样本所占的比例为$$ p_k $$，则信息熵D的定义为

$$
Ent(D) = -\sum\limits_{k=1}^{|\mathbf{y}|}p_klog_2p_k
$$    

End(D)的值越小，则D的纯度越高。

* 信息增益    
假设离散属性a有V个可能的取值（$$a^1, a^2, ..., a^v$$），若使用a来对样本集D进行划分，则会产生V个分支节点，其中第v个分支节点包含了D中所在的属性a上取值为$$a^v$$的样本，记为$$D^v$$。我们可根据信息熵的定义，计算出$$D^v$$的信息熵，再考虑到不同分支节点所包含的样本量不同，给每个分支节点赋予权重$|D^v|/|D|$，即样本数越多的分支结点的影响越大，于是可计算出用属性a对样本集进行划分所获得的“信息增益”

$$
Gain(D,a) = Ent(D) - \sum\limits_{v=1}^V\frac{|D^v|}{|D|}Ent(D^v)
$$    

还有其他如**增益率**、**基尼系数**等等算法，这里就不一一介绍了。

## 决策树开发流程
收集数据：可以使用任何方法。    
准备数据：树构造算法    
分析数据：可以使用任何方法，构造树完成之后，我们应该检查图形是否符合预期。    
训练算法：构造树的数据结构。    
测试算法：使用训练好的树计算错误率。    
使用算法：此步骤可以适用于任何监督学习任务，而使用决策树可以更好地理解数据的内在含义。    

# 决策树项目案例
这里使用周志华-机器学习里面的西瓜数据集-使用决策树方法判断西瓜的好坏。
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

 根据色泽、根蒂、敲声、纹理、脐部、触感、密度、含糖率这些特征判断西瓜是好瓜还是坏瓜。

## 读入数据
> 将数据读入，存入pandas dataframe中

```python
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
```

## 特征工程
> 类别变量重编码

对于类别变量(Categorical Variable)，例如：男和女、high和low等，这种字符串变量一般是不能直接输入到算法模型中的，需要重编码为数字1,2,3,4等或者是二进制bitmap，否则会报错`ValueError: could not convert string to float`。

sklearn库里面提供了LabelEncoder 和 OneHotEncoder两种重编码方法。

* LabelEncoder
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit_transform(['男','女'])
>> array([1, 0], dtype=int64)
```
* OneHotEncoder两种重编码方法
```python
from sklearn import preprocessing
# 需要先将字符转成数值
features = ['男', '女']
enc = preprocessing.LabelEncoder()
features = enc.fit_transform(features)
# 再将数值特征OneHotEncoder
features = features.reshape(-1, 1) # Needs to be the correct shape
ohe = preprocessing.OneHotEncoder(sparse=False) #Easier to read
ohe.fit_transform(features)
>> array([[ 0.,  1.],[ 1.,  0.]])
```

通俗的讲，分类变量如性别：男，女，LabelEncoder将它直接变成数值变量0，1。而oneHotEncoder将变量扩维，变成对应的哑变量，男变成[0, 1]，女变成[1, 0]。想要了解更多见这篇文章[CNBLOGS](https://www.cnblogs.com/king-lps/p/7846414.html)。

树模型直接用LabelEncoder就可以。
```python
class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)
```
有些细节问题需要特别注意，详见[关于一些重编码的坑](https://ask.hellobi.com/blog/DataMiner/4897)

## 训练模型
这里使用信息增益作为划分标准，对决策树进行训练
参考链接： [DecisionTreeClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier)
```python
def predict_train(x_train, y_train):
    '''
    '''
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf.fit(x_train, y_train)
    ''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
    print('feature_importances_: %s' % clf.feature_importances_)
    return clf
```

## 可视化
我们需要借助[graphviz](http://www.graphviz.org/)这个软件来作图，需要提前安装这个软件，并且将`dot`这个可执行文件加入系统环境变量中：
```python
def visualize_tree(tree, feature_names):
    """Create tree png using graphviz.

    Args
    ----
    tree -- scikit-learn DecsisionTree.
    feature_names -- list of feature names.
    """
    with open("dt.dot", 'w', encoding='utf-8') as f:
        export_graphviz(tree, out_file=f,
                        feature_names=feature_names)
    command = ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
    subprocess.check_call(command)
```
最终得到的是以下图形
![](http://img.77qingliu.com/18-4-20/64345968.jpg)
> 注意！使用中文会出现乱码问题。这里需要将`with open("dt.dot", 'w', encoding='utf-8')`这里面生成的`dt.dot`文件重新打开，并且在里面加入`node [shape=box fontname="FangSong"] ;`，然后将文件另存为**不带BOM的UTF-8编码文件**，最后在命令行里面手动通过`dot -Tpng dt.dot -o dt.png`手动生成最后的图片。

## 总结
直接调用sklearn的包真是方便！以后有机会再手写代码吧，最近忙着找工作，先糊弄过去再说:)。
文章的代码都在[machine_learning_in_action](https://github.com/77QingLiu/machine_learning_in_action)这个仓库里面。
这里遇到的坑主要是重编码以及乱码的问题，如果遇到同样的问题请查看前面的链接。
