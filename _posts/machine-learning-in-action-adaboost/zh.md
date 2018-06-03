## 集成学习
集成学习(ensemble learning)通过构建并结合多个学习器来完成学习任务，有时也被称为多分类器。

下图显示出集成学习的一般结构：先产生一组“个体学习器”，再用某种策略将它们结合起来。
![](http://p7ffgka2w.bkt.clouddn.com/18-5-29/28078382.jpg)
个体学习器通常由一个现有的学习算法从训练数据产生，例如决策树算法、BP神经网络算法等等。    
若个体学习器都属于同一类别，例如都是决策树或都是神经网络，则称该集成为同质的（homogeneous）;若个体学习器包含多种类型的学习算法，例如既有决策树又有神经网络，则称该集成为异质的（heterogenous）。
>同质集成：个体学习器称为“基学习器”（base learner），对应的学习算法为“基学习算法”（base learning algorithm）。        
>异质集成：个体学习器称为“组件学习器”（component learner）或直称为“个体学习器”。

集成学习通过将多个学习器进行结合，常可获得比单一学习器显著优越的泛化性能。这对“弱学习器”尤为明显，因此集成学习的很多理论研究都是针对弱学习器进行的，而基学习器又被称为弱学习器。但需要注意的是，虽然从理论上来说使用弱学习器集成足以获得好的性能，但在实践中出于种种考虑，例如希望使用较少的个体学习器，或是重用关于常见学习器的一些经验等，人们往往会使用比较强的学习器。

上面我们已经提到要让集成起来的泛化性能比单个学习器都要好，虽说团结力量大但也有木桶短板理论调皮捣蛋，那如何做到呢？这就引出了集成学习的两个重要概念：准确性(accuracy)和多样性（diversity）。准确性指的是个体学习器不能太差，要有一定的准确度；多样性则是个体学习器之间的输出要具有差异性。通过下面的这三个例子可以很容易看出这一点，准确度较高，差异度也较高，可以较好地提升集成性能。
![](http://p7ffgka2w.bkt.clouddn.com/18-5-29/49443636.jpg)

我们做个简单分析。考虑二分类问题$$y\in\{-1,+1\}$$和真实函数$$f$$，假定基分类器的错误率为$$\epsilon$$，即对每个基分类器$$h_i$$有
\\[
P(h_i(x)\ne f(x)) = \epsilon
\\]
假设集成通过简单投票法结合T个基分类器，若有超过半数的基分类器正确，则集成分类就正确：
\\[
H(x) = sign\left(\sum_{i=1}^Th_i(x)\right)
\\]
假设基分类器的错误率互相独立，则由 **[Hoeffding](https://blog.csdn.net/z_x_1996/article/details/73564926)** 不等式可知，集成的错误率为：
\\[
\begin{aligned}
P(h_i(x)\ne f(x)) &= \sum_{k=0}^{\lfloor T/2\rfloor}\binom{T}{k}(1-\epsilon)^k{\epsilon}^{T-k} \\\\ &=exp\left(-\frac{1}{2}T(1-2\epsilon)^2\right)
\end{aligned}
\\]
上式显示出，随着集成个体数目T的增大，集成的错误率将指数级下降，最终趋向于零。      
但是上面的分析有一个关键假设：基学习器的误差相互独立。在现实任务中，个体学习器是为解决同一个问题训练出来的，它们显然不可能互相独立！事实上，个体学习器的“准确性”和“多样性”本身就存在冲突。一般，准确性很高之后，要增加多样性就需牺牲准确性。事实上，如何产生并结合“好而不同”的个体学习器，恰是集成学习研究的核心。      
根据个体学习器的生成方式，目前的集成学习方法大致分为两大类：

1. 个人学习器之间存在强依赖关系、必须串行生成的序列化方法。代表算法是Boosting；
2. 以及个体学习器间不存在强依赖关系，可同时生成的并行化方法。代表算法是Bagging和“随机森林”。

## 提升方法与AdaBoost算法
提升方法(Boosting)是一族可将所分类器提升为强学习器的算法，这族算法的工作机制类似：

* 先从初始训练集训练一个基学习器。
* 再根据基学习器的表现对训练样本分布进行重调，使得先前基学习器做错的样本在后续受到更多的关注
* 然后，基于调整后的样本分布来训练下一个基学习器
* 一直重复上述步骤，直到基学习器的个数达到train前的指定数T，然后将这T个基学习器进行加权

对提升方法来说，有两个问题需要回答：一是在每一轮如何改变训练数据的权值或概率分布；二是如何将弱分类器组合成一个强分类器。关于这两个问题，Boosting族算法中最著名AdaBoost的做法是，提高那些被前一轮弱分类器错误分类样本的权值，而降低那些被正确分类样本的权值。至于第二个问题，即弱分类器的组合，AdaBoost算法采用加权多数表决的方法。具体地，加大分类错误率小的弱分类器的权值，使其在决定中起较大的作用，减少分类误差率大的弱分类器的权值，使其在表决中起较小的作用。下面介绍AdaBoost算法的基本思路。

## Adaboost算法的基本思路
现在叙述AdaBoost算法。假设给定一个二类分类的训练数据集
\\[
T = \{(x_1,y_1),(x_2,y_2),\cdot\cdot\cdot,(x_n,y_n)\}
\\]
其中，每个样本点由实例与标记组成。实例$$x_i\in\chi\subseteq R^n$$，标记$$y_i\in Y=\{-1,+1\}$$，
AdaBoost算法利用下列算法，从训练数据集中学习一系列弱分类器或基分类器，并将这些弱分类器线性组合成为一个强分类器。

输入：训练集 $$D=((x_1,y_1),(x_2,y_2),...,(x_m,y_m))$$ ，训练轮数T，和一个基学习算法$$G$$

输出：最终分类器$$G(x)$$

1. 初始化训练数据的权值分布：\\[D_1=(w_{11},\cdot\cdot\cdot,w_{1i},\cdot\cdot\cdot,w_{1N}), w_{1i}=\frac{1}{N}, i = 1,2,\cdot\cdot\cdot,N\\]
2. 对$$m=1,2,\cdot\cdot\cdot,M$$
    1. 使用具有权值分布$$D_m$$的训练数据集学习，得到基本分类器\\[G_m(x):\chi\to{-1,+1}\\]
    2. 计算$$G_m(x)$$在训练数据集上的分类误差率\\[e_m=P(G_m(x_i)\ne y_i) = \sum_{i=1}^Nw_{mi}I(G_m(x_i)\ne y_i)\\]
    3. 计算$$G_m(x)$$的系数\\[\alpha_m = \frac{1}{2}log\frac{1-e_m}{e_m}\\]
    4. 更新训练数据集的权值分布\\[D_{m+1}=(w_{m+1,1},\cdot\cdot\cdot,w_{m+1,i},\cdot\cdot\cdot,w_{m+1,N}) \\\\ w_{m+1,i} = \frac{w_{m,i}}{Z_m}exp(-\alpha_my_iG_m(x_i)), i=1,2,\cdot\cdot\cdot,N\\]这里，$$Z_m$$是规范化因子\\[Z_m=\sum_{i=1}^Nw_{m,i}exp(-\alpha_my_iG_m(x_i))\\]它使得$$D_{m+1}$$成为一个概率分布。
3. 构建基本分类器的线性组合\\[f(x) = \sum_{m=1}^M\alpha_mG_m(x)\\]得到最终分类器\\[G(x) = sign(f(x))=sign\left(\sum_{m=1}^M\alpha_mG_m(x)\right)\\]
这里说明以下3个方面：

* 计算基本分类器$$G_m(x)$$的系数$$\alpha_m$$，$$\alpha_m$$表示$$G_m(x)$$在最终分类器中的重要性。当$$e_m \le \frac{1}{2}$$时，$$\alpha_m \gt 0$$，并且$$\alpha_m$$随机$$e_m$$的减小而增大，所以分类误差越小的基本分类器在最终分类器中的作用越大。
* 式$$w_{m+1,i} = \frac{w_{m,i}}{Z_m}exp(-\alpha_my_iG_m(x_i))$$可以写成:\\[w_{m+1, i} = \begin{cases}&\frac{w_{m,i}}{Z_m}e^{-\alpha_m},\qquad G_m(x_i)=y_i\\\\&\frac{w_{m,i}}{Z_m}e^{\alpha_m}, \qquad   G_m(x_i) \ne y_i\end{cases}\\]由此可知，被基本分类器$$G_m(x)$$误分类样本的权值得以扩大，而被正确分类样本的权值却得以缩小。因此，误分类样本在下一轮学习中起更大的作用，不改变所给的训练数据，而不断改变训练数据权值的分布，使得训练数据在基本分类器的学习中起不同的作用。
* 最终分类器的生成是M个基分类器的加权表决。系数$$\alpha_m$$表示了基本分类器$$G_m(x)$$的重要性，这里，所有的$$\alpha_m$$之和并不为1。


## Adaboost算法的推导
Adaboost算法有多种推导方式，比较容易理解的是基于“加性模型”，即基学习器的线性组合\\[G(x) = \sum_{m=1}^M\alpha_mG_m(x)\\]来最小化指数损失函数\\[\ell_{exp}(G|D)=E_{x\sim D}[e^{-yG(x)}]\\]
其中$$y$$是样本的实际类别，$$G(x)$$是预测的类别，样本$$x$$的权重服从$$D$$分布，$$E$$代表求期望。

### 损失函数的定义
那么损失函数为什么这样定义呢？下面证明：
若$$G(x)$$能使损失函数最小化，那我们考虑上式对$$G(x)$$的偏导为零：
\\[\frac{\alpha \ell_{exp}(G|D)}{\alpha G(x)}=-e^{-G(x)}P(y=1|x)+e^{G(x)}P(y=-1|x)\\]

令上式为零，得：
\\[G(x)=\frac{1}{2}ln\frac{P(y=1|x)}{P(y=-1|x)} \\]

因此，有
\\[sign(G(x))=sign(\frac{1}{2}ln\frac{P(y=1|x)}{P(y=-1|x)})\\]

当$$P(y=1\vert x)>P(y=-1\vert x)$$时，$$sign(f(x))=1$$
当$$P(y=1\vert x)>P(y=-1\vert x)$$时，$$sign(f(x))=-1$$

这样的分类规则正是我们所需要的，若指数函数最小化，则分类错误率也最小，它们俩是一致的。所以我们的损失函数可以这样定义。

### 基分类器权重系数$$\alpha_{i}$$ 的求取

接下来，我们看一下基类器 $$G_m(x)$$ 和系数 $$\alpha_{i}$$ 的求取。

在Adaboost算法中，第一个分类器$$G1(x)$$是直接将基学习算法用于初始数据分布求得，之后不断迭代，生成 $$\alpha_m$$ 和 $$G_m$$ 。当第m个基分类器产生后,我们应该使得其在数据集第m轮样本权重基础上的指数损失最小，即:
\\[
\begin{aligned}
L(\alpha_m,G_m(x))&=argmin  E_{x\sim D_m}\left[ {exp(-y\alpha_mG_m(x))} \right] \\\\ &=E_{x\sim D_m}\left[ \sum_{y_i=G_m(x_i)}{e^{-\alpha_m}}+\sum_{y_i\ne G_m(x_i)}{e^{\alpha_m}} \right] \\\\ &=e^{-\alpha_m}P(y_i=G_m(x_i))+e^{\alpha_m}P(y_i\ne G_m(x_i)) \\\\ &=e^{-\alpha_m}(1-e_m)+e^{\alpha_m}e_m \\\\
\end{aligned}
\\]
考虑指数损失函数的导数为零
\\[
\frac{\alpha L(\alpha_m,G_m(x))}{\alpha\alpha_m}=-e^{-\alpha_{m}}(1-e_m)+e^{\alpha_{m}}e_m=0
\\]
可解得
\\[
\alpha_m=\frac{1}{2}ln(\frac{1-e_m}{e_m})
\\]
这恰是分类器权重更新公式

### 如何更新样本权重D?
这一部分比较长，在周志华老师《机器学习》P175有详细的推导，感兴趣的读者可以自行查阅。这里直接给出 $$D_m$$ 的迭代公式。
\\[
\begin{equation}\begin{aligned}
D_{m}&=(w_{m,1},w_{m,2},...w_{m,N}) \\\\ D_{m+1}&=(w_{m+1,1},w_{m+1,2},...w_{m+1,N}) \\\\ w_{m+1,i}&=\frac{w_{mi}exp(-\alpha_my_iG_m(x_i))}{Z_m}
\end{aligned}\end{equation}
\\]
其中 $$Z_m=\sum_{i=1}^{N}{w_{mi}exp(-\alpha_my_iG_m(x_i))}$$ ，是一个常数。

## AdaBoost算法的误差
随着集成学习中个体分类器数目的增加，其集成的错误率将成指数级下降，最终趋向于零。     
李航老师《统计学习方法》有详细的证明。这里就不再赘述了。

## 总结
这里对AdaBoost算法的优缺点做一个总结。    

AdaBoost的主要优点有：

1. AdaBoost作为分类器时，分类精度很高
2. 在AdaBoost的框架下，可以使用各种回归分类模型来构建弱学习器，非常灵活。
3. 作为简单的二元分类器时，构造简单，结果可理解。
4. 不容易发生过拟合

AdaBoost的主要缺点有：

1. 对异常样本敏感，异常样本在迭代中可能会获得较高的权重，影响最终的强学习器的预测准确性。

## 参考文档
[机器学习-周志华](https://book.douban.com/subject/26708119/)        
[统计学习方法-李航](https://book.douban.com/subject/10590856/)       
[集成学习之Adaboost算法原理小结](http://www.cnblogs.com/pinard/p/6133937.html)        