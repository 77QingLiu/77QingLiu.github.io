![](http://img.77qingliu.com/post/2019-05-12-021000.jpg)

---

在进行监督学习时，我们经常要处理分类特征。也就是将字符转变成一个计算机能识别的数值表示。除了LightGBM, Catboost之类的算法在内部有自动encoding的机制之外，现在大多数机器学习算法都要求输入数据是数值的。

有很多方法可以实现Encoding
* [Label encoding](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) 为每个类别选择一个任意的数字
* [One-hot encoding](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html) 为每个类别创建一个二进制列
* [Vector representation](https://www.tensorflow.org/tutorials/representation/word2vec) 类似word2vec，使用一个低维子空间表示分类
* [Optimal binning](https://github.com/Microsoft/LightGBM/blob/master/docs/Advanced-Topics.rst#categorical-feature-support) LightGBM or CatBoost内部的编码方法
* [Target mean encoding](http://www.saedsayad.com/encoding.htm) 根据目标类别取平均目标值

每种方法都有其优缺点，通常取决于数据和需求。其中one-hot encoding是现在比较通用和流行的方法。one-hot将每个类别映射到$\mathbb{R}^{n - 1}$中的一个向量。向量中的每个向量都包含一个“1”，其余的值都是“0”。这种编码通常用于线性模型，而不是树模型的最佳选择，主要是因为one-hot编码有以下两个缺点：

* 对于高基数的特征，one-hot编码会产生很多列，使得数据的维度显著增加，这样会降低学习速度。另外，在随机模型和GBDT模型中，通常我们会指定模型进行`随机列采样`，但是由于one-hot编码会产生许多列，这样会人为的增加该分类特征的比例，造成此分类特征的列占比增加，使得模型将一个one-hot编码特征视为比没其他特征更有用
* 在每一个分割上，树模型只能将一个类别与其他类别分开。列的增加造成了树深度的增加，增加了过拟合的风险。

### Mean Target Encoding
一般的Mean Target Encoding可以看作是`Label Encoding`的一种变体。想法很简单，对于每个类别，将它的值设置为**训练数据上目标变量的平均值**。
$$
label_{c} = p_{c}
$$
$p_c$是目标变量在特征取值为$c$时的平均值

> 注意：只能在训练样本上估计平均值，而不使用测试数据，原因很明显：应该像不知道目标一样对待测试数据。

举个简单的例子
```python
import pandas as pd

df = pd.DataFrame({
    'x_0': ['a'] * 5 + ['b'] * 5,
    'x_1': ['a'] * 9 + ['b'] * 1,
    'y': [1, 1, 1, 1, 0, 1, 0, 0, 0, 0]
})
```
![](http://img.77qingliu.com/post/2019-05-12-034418.jpg)


计算 $x_0$对应目标变量的平均值.
```python
means = df.groupby('x_0')['y'].mean().to_dict()
```

从而得到下面mapping字典
```python
{
    'a': 0.8,
    'b': 0.2
}
```

将$x_0$的值用目标变量的平均值替代
```python
df['x_0'] = df['x_0'].map(means)
```
于是就得到了变量$x_0$的Mean Target Encoding
![](http://img.77qingliu.com/post/2019-05-12-034832.jpg)

对每个分类变量重复上面的操作，就可以得到所有变量的Mean Target Encoding。

Mean Target Encoding之所有能够有效，是因为通过这一转换建立了特征和标签之间的线性关系，从而获得了可以解释目标变量的信息。

对于树模型来说，这意味着更少分裂，更快的学习速率。特别在处理高基数分类特征时，如果使用one-hot之类的编码，模型很难把每个小类别到一个单独的桶，但通过Mean Target Encoding，很多小类别可以基于他们Mean Target值放在一个桶内，从而降低了分类特征的基数，使得模型的泛化能力更好。

### 过拟合风险
上面的例子显示了简单的Mean Target Encoding，但是在实际过程中，特别是处理高基数特征时，这样简单的处理会增加`过拟合`的风险。因为在高基数的特征内，很容易存在一些看起来预测能力很强的类别。

假设现在某个类别内我们有5个样本(从伯努利分布(0.5)中抽取5次)，那么什么样的概率是一个好的预测器呢?得到5个1或5个0的概率是0.0625。这样的概率看似很低，但是当基数很大，比如有100个这样的类别，5个样本，0或强预测能力，预计至少有6个类别的目标都是0或者目标都是1，但是这样的类别本身对未来是`没有预测能力`的。

然后，假如加上目标的四个值相同的组合(看起来仍然是一个很好的预测器)，发生这种情况的概率等于0.375！超过三分之一的类别本身是预测能力为0，但在5个样本的小样本规模上看起来将是一个不错的预测器。

树模型会将把这些小但类别放在单独的叶子中，并学会预测这些类别的极值。然后当我们在测试数据中得到相同的类别时，它们中的大多数不会有相同的目标分布，模型预测将是错误的！这就是过拟合！

### 基于先验概率的正则化
为了解决过拟合的问题，最简单的正则化技术是将稀有类别的编码移动到更接近数据集目标均值的位置。这样，我们希望模型就不太可能对小类别学习非常高或非常低的概率：它们的编码更接近于中间均值，并与平均值目标值更小的类别的编码混合在一起。
我们可以使用以下公式

$$
label_c = \frac{(p_c*n_c + p_{global}*\alpha)}{(n_c+\alpha)}
$$

其中$p_c$是一个类别的目标均值，$n_c$是一个类别的样本数量,$p_{global}$是所有样本的目标均值，α是一个正则化参数，可以看成对类别的目标均值的信任度。

这样的处理还存在一个缺点，获得的编码仍然是`伪连续的`，每个类别都将用一个不同的实数编码，这仍然会允许树模型将任何类别放在一个不同的叶子中，并为叶子设置一个极端的目标概率。

为了使得编码连续，我们需要添加一些随机性，目标是在一个类别中以某种方式随机编码，但仍然让模型知道类别编码和目标变量之间存在相关性。

### 基于K-fold的正则化
k折正则化背后的思想是仅使用类别示例的一部分来估计该类别的编码。通过将数据分割成k-fold，对于每个待编码的样本，使用除待编码样本之外的所有fold样本来估计它的编码。通过`全局均值正则化`和`k-折叠`相结合的方法，我们可以实现更健壮的编码。

k折正则化分为三步
1. 将数据分为K组
2. 排除待编码组
3. 在排除编码组的数据上，使用上述全局均值正则化公式，获得每个类别的编码，将编码应用到待编码组之后

示例如下：

1. 对于训练集，这里使用5-K，将数据分成5组
2. 对于第一折，使用除第一折之外的数据进行Mean Target Encoding进行编码![](http://img.77qingliu.com/post/2019-05-12-044643.jpg)
3. 对其他折，重复步骤2的过程![](http://img.77qingliu.com/post/2019-05-12-044957.jpg)，这样就获得了所有训练集数据的编码
4. 对于测试数据集，对训练集的编码取均值，作为其编码![](http://img.77qingliu.com/post/2019-05-12-045125.jpg)

### How good is it?
那么Mean Target Encoding对模型效果的提升到底有多少呢？

Kaggle上面有研究者在5个数据集上对Mean Target Encoding做了实验：[Mean (likelihood) encoding for categorical variables with high cardinality and feature interactions: a comprehensive study with Python](https://www.kaggle.com/vprokopev/mean-likelihood-encodings-a-comprehensive-study)，在其中一个数据集上，Mean Target Encoding在α取值为5，采用5-fold时得到了最好的效果
![](http://img.77qingliu.com/post/2019-05-12-051218.jpg)

同时作者也推荐：
* 使用4或5-fold和α=5进行Mean Target Encoding，因为这样的组合几乎总是显示了良好的结果。
* α取0的编码比其他取任何值的α编码都**差**。
* Mean Target Encoding让模型收敛得更快(就迭代次数而言)。

[H2O.AI](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-munging/target-encoding.html)内也有Mean Target Encoding的实现，它们在cleaned lending club data数据上做了实验
![](http://img.77qingliu.com/post/2019-05-12-053158.png)

显示使用Mean Target Encoding对模型有明显的提升

### 实现
这里采用类似sklearn API的实现方式
```python
class KFoldTargetEncoderTrain(base.BaseEstimator,
                               base.TransformerMixin):
    def __init__(self,colnames,targetName,
                  n_fold=5, verbosity=True,
                  discardOriginal_col=False):
        self.colnames = colnames
        self.targetName = targetName
        self.n_fold = n_fold
        self.verbosity = verbosity
        self.discardOriginal_col = discardOriginal_col
    def fit(self, X, y=None):
        return self
        
    def transform(self,X):
        assert(type(self.targetName) == str)
        assert(type(self.colnames) == str)
        assert(self.colnames in X.columns)
        assert(self.targetName in X.columns)
        mean_of_target = X[self.targetName].mean()
        kf = KFold(n_splits = self.n_fold,
                   shuffle = False, random_state=2019)
        col_mean_name = self.colnames + '_' + 'Kfold_Target_Enc'
        X[col_mean_name] = np.nan
        for tr_ind, val_ind in kf.split(X):
            X_tr, X_val = X.iloc[tr_ind], X.iloc[val_ind]
            X.loc[X.index[val_ind], col_mean_name] =
            X_val[self.colnames].map(X_tr.groupby(self.colnames)
                                     [self.targetName].mean())
            X[col_mean_name].fillna(mean_of_target, inplace = True)
        if self.verbosity:
            encoded_feature = X[col_mean_name].values
            print('Correlation between the new feature, {} and, {}
                   is {}.'.format(col_mean_name,self.targetName,
                   np.corrcoef(X[self.targetName].values,
                               encoded_feature)[0][1]))
        if self.discardOriginal_col:
            X = X.drop(self.targetName, axis=1)
        return X
targetc = KFoldTargetEncoderTrain('Feature','Target',n_fold=5)
new_train = targetc.fit_transform(train)
```

```python
class KFoldTargetEncoderTest(base.BaseEstimator, base.TransformerMixin):

    def __init__(self,train,colNames,encodedName):

        self.train = train
        self.colNames = colNames
        self.encodedName = encodedName

    def fit(self, X, y=None):
        return self
    def transform(self,X):
        mean =  self.train[[self.colNames,
                self.encodedName]].groupby(
                                self.colNames).mean().reset_index()

        dd = {}
        for index, row in mean.iterrows():
            dd[row[self.colNames]] = row[self.encodedName]
        X[self.encodedName] = X[self.colNames]
        X = X.replace({self.encodedName: dd})
   return X

  test_targetc = KFoldTargetEncoderTest(new_train,
                                      'Feature',
                                      'Feature_Kfold_Target_Enc')
new_test = test_targetc.fit_transform(test)
```

另外除了[H2O.AI](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-munging/target-encoding.html)上Target Encoding的实现，GitHub上也有一些库内有成熟的实现：
* xam - [Bayesian target encoding](https://github.com/MaxHalford/xam/blob/master/docs/feature-extraction.md#bayesian-target-encoding)
* Category Encoders - [Target Encoder](http://contrib.scikit-learn.org/categorical-encoding/targetencoder.html)

这些实现在计算上有一些差别，具体到哪一个比较实用还有待研究。


### 结论
众所周知，机器学习领域内没有一种方法能解决所有问题，更多的需要根据数据和需求选择合适的算法，这里也不例外。Mean Target Encoding编码是一种强大且有效的分类编码方法，但在并非所有场景下但最佳方法，具体问题还需具体分析。


### 参考资料
* [Mean (likelihood) encoding for categorical variables with high cardinality and feature interactions: a comprehensive study with Python](https://www.kaggle.com/vprokopev/mean-likelihood-encodings-a-comprehensive-study)
* [Target Encoding Done The Right Way](https://maxhalford.github.io/blog/target-encoding-done-the-right-way/)
* [Target Encoding](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-munging/target-encoding.html)