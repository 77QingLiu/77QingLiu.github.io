这篇文章参考自外文[learning-path-data-science-python](https://www.analyticsvidhya.com/learning-paths-data-science-business-analytics-business-intelligence-big-data/learning-path-data-science-python/)，知乎大V也曾将其翻译成中文，并曾经在微博上被大量转发、收藏。这里为了给数据分析方面的Python新手提供一个完整的学习路径，我总结自己过去一段时间的学习经验，对所需学习的利用python进行数据分析的所有步骤完整概述。如果你已经有一些相关的背景知识，或者你不需要路径中的所有内容，你可以随意调整你自己的学习路径。

### 步骤1：设置你的机器环境

一个好的机器环境决定了你学习过程中的愉悦程度。最简单的方法就是从Continuum [Anaconda](https://www.anaconda.com/distribution/)上直接下载。Anaconda将你以后可能会用到的大部分的东西进行了打包。采用这个方法的主要缺点是，Python包作者发布的可用底层库的更新，可能不会及时的同步在Anaconda中，你仍然需要等待Continuum去更新Anaconda包。当然如果你是一个初学者，这应该没什么问题。

如果你在安装过程中遇到任何问题，你可以在这里找到不同操作系统下更详细的安装说明。

从Anaconda下载的package里面，包括了一些python中非常给力的工具，比如[Jupyter Notebook](https://jupyter.org/)，[Visual Studio Code](https://code.visualstudio.com/)，[PyCharm](https://www.jetbrains.com/pycharm/)。

对于初学者，我推荐Jupyter Notebook + 任意一款代码编辑器作为日常使用工具。Jupyter Notebook作为一款笔记类编辑器，集成了编辑+学习+记录+分享的功能，是一个初学者理想的学习工具。至于编辑器，这里强烈推荐[Visual Studio Code](https://code.visualstudio.com/)。

对于有经验者，或者将python作为日常工作的同学，我更倾向于一个集成notebook + 编辑的环境，这里我推荐[Atom](https://atom.io/) + [Hydrogen(Atom Package)](https://nteract.gitbooks.io/hydrogen/)的组合
![](https://cloud.githubusercontent.com/assets/13285808/20360886/7e03e524-ac03-11e6-9176-37677f226619.gif)

Atom + Hydrogen的组合，弥补了Jupyter Notebook编辑能力的不足，同时也让数据探索和分析更轻松，更是支持远程连接服务器的功能，极大的提高了实际工作中数据分析+挖掘的效率。


### 步骤2：学习Python语言的基础知识

你应该先去了解Python语言的基础知识、库和数据结构。Codecademy上的Python课程是你最好的选择之一。完成这个课程后，你就能轻松的利用Python写一些小脚本，同时也能理解Python中的类和对象。
如果你不喜欢交互编码这样的学习方式，也可以阅读一些Python的书籍，这里我推荐
* [简明Python教程(A byte of Python)](https://bop.mol.uno/)
* [Dive Into Python3](http://www.ttlsa.com/docs/dive-into-python3/)

具体学习内容有：
* Python中一些常用的数据类型
  * 列表Lists
  * 元组Tuples
  * 字典Dictionaries
* 基本语句 Statement
* 函数 Function
* 类 Class
* 包 Package

![Python in one picture](http://77qingliu-blog.oss-cn-shanghai.aliyuncs.com/py3%20in%20one%20pic.png)

这里重点是接触python中的一些基本概念和操作，以及理解编程中**面向对象编程**的一些思想。
Learning by doing 是最好的学习方式，在学习过程中应该勤动手，解决一些Python教程题，这些题能让你更好的用Python脚本的方式去思考问题。此外，也可以用Python做一些小的项目，或者写一些小的脚本替代日常工作中一些重复的劳动。

### 步骤3：学习Python中的数据科学库—[NumPy](http://www.numpy.org/), [Pandas](https://pandas.pydata.org/), [SciPy](https://www.scipy.org/), [Matplotlib](https://matplotlib.org/)

这里强烈推荐[Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)作为Python数据科学的入门读物，此书对Python 数据相关的库，如Numpy, Pandas, Sklearn等做了深入浅出的介绍，初学者读完此书能对Python Data Ecosystem有较全面的了解。同时，此书的作者不仅是一名数据科学家，更是画图堪比Tableau的Python库[Altair](https://altair-viz.github.io/)的主要开发者。

在阅读这本书的过程中，学习到具体的章节时，推荐进行进一步的练习和扩展阅读。下面的一些资料可以作为一些参照
* Numpy
  * [Numpy Tutorial](https://www.numpy.org/devdocs/user/quickstart.html)
  * [Numpy Notebooks](https://nbviewer.jupyter.org/github/donnemartin/data-science-ipython-notebooks/tree/master/numpy/)
* Pandas
  * [10 Minutes to Pandas](http://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html)
  * [Pandas Exercise](https://nbviewer.jupyter.org/github/guipsamora/pandas_exercises/tree/master/)
  * [Pandas Notebooks](https://nbviewer.jupyter.org/github/donnemartin/data-science-ipython-notebooks/tree/master/pandas/)
* Scipy
  * [SciPy Tutorial](https://docs.scipy.org/doc/scipy/reference/tutorial/)
  * Two exercises
    * [Random Sampling](https://nbviewer.jupyter.org/github/donnemartin/data-science-ipython-notebooks/blob/master/scipy/sampling.ipynb)
    * [Hypothesis Testing](https://nbviewer.jupyter.org/github/donnemartin/data-science-ipython-notebooks/blob/master/scipy/hypothesis.ipynb)
* Matplotlib
  * [Matplotlib Tutorial](https://matplotlib.org/tutorials/index.html)
  * [Matplotlib Notebooks](https://nbviewer.jupyter.org/github/donnemartin/data-science-ipython-notebooks/tree/master/matplotlib/)

这里学习的重点是Numpy和Pandas，Numpy是数学运算的基础，特别要练习数组arrays。这将会为下边的学习旅程打好基础。数据科学的项目，80%的工作量在于数据清洗和整理是工业界的共识，因此，Pandas作为Python中类似SQL的数据框操作框架，作用尤其重要。这里推荐另外一本Pandas的书，由Pandas的作者Wes McKinney写的“[Python for Data Analysis](http://wesmckinney.com/pages/book.html)”，这里有一位国人做了一份中文笔记放在Github上，可以做为[参考](https://nbviewer.jupyter.org/github/LearnXu/pydata-notebook/tree/master/
)

对于我们这里的需求来说，Matplotlib的内容过于广泛，无需学习所有内容，稍作了解即可。根据[帕累托法则(二八原则)](https://zh.wikipedia.org/wiki/%E5%B8%95%E7%B4%AF%E6%89%98%E6%B3%95%E5%88%99)
，Pandas和Numpy这种数据处理工具，应该是你花更多的时间练习的地方，Pandas会成为所有中等规模数据分析的最有效的工具。

在Pandas的文档中，也有很多Pandas教程，你可以在那里查看。

此外，对于数据处理过程中碰到的各种问题，[StackOverFlow](https://stackoverflow.com/tags/pandas/hot)上有各种答案，也可以用作参考。

### 步骤4：学习Scikit-learn库和机器学习的内容

机器学习是一个很大的概念，我认为掌握机器学习的程度应该决定了一个人在数据方向的上限。这里的学习我觉得应该采用理论和实际并重的方式进行学习。一方面应该学习数学，概率统计和机器学习的理论知识，另一方面应该在Python中用一些现有的框架比如[Scikit-learn](https://scikit-learn.org/stable/)进行一些实际的操作。 


Scikit-learn是机器学习领域最有用的Python库。[Scikit-learn Tutorials](https://scikit-learn.org/stable/tutorial/index.html)是该库的简要概述。推荐阅读一些这方面的书来快速入门，比如[Introduction to Machine Learning with Python: A Guide for Data Scientists](https://www.oreilly.com/library/view/introduction-to-machine/9781449369880/)

在理论方面，推荐阅读国内两位大牛的两本书
* 一本是国内机器学习的领军人物，周志华教授的[机器学习](https://book.douban.com/subject/26708119/)
* 另一本是微软研究院李航博士的[统计学习方法](https://book.douban.com/subject/10590856/)

如果数学基础不太好的话，推荐阅读最近微信朋友圈非常火爆的数学读物[Mathematics for Machine Learning](https://mml-book.github.io/)

此外，如果你需要更易懂的机器学习技术的解释，你可以选择来自Andrew Ng的机器学习课程或者台大林轩田的机器学习课程，并且利用Python做相关的课程练习。


### 步骤5：Kaggle：练习，练习，再练习

你现在已经学会了你需要的所有技能。现在就是如何练习的问题了，还有比通过在Kaggle上和数据科学家们进行竞赛来练习更好的方式吗？深入一个当前Kaggle上正在进行的比赛，尝试使用你已经学过的所有知识来完成这个比赛。

Kaggle 是什么？

* Kaggle 是一个数据科学竞赛平台
    >Kaggle是一个数据建模和数据分析竞赛平台。企业和研究者可在其上发布数据，统计学者和数据挖掘专家可在其上进行竞赛以产生最好的模型。作为一个竞赛平台，Kaggle上竞赛获得奖牌会获得丰厚的奖励，其中的一些竞赛有高达 100 万美元的奖金池。
* Kaggle 不止是一个竞赛平台
    >Kaggle对于想要提高技能的人来说是一个知识宝库。 它上面保留着所有历史竞赛的数据和全世界许多无私的数据工作者分享的code和以及idea。初学者可以很快的在一些简单的比赛上快速入门，并通过学习他们分享的notebook提高自己的数据科学技能。

Kaggle 怎么入门？
推荐看这篇知乎文章[Kaggle 怎么入门](https://www.zhihu.com/question/23987009)


### 步骤6：深度学习

现在你已经学习了大部分的机器学习技术，是时候关注一下深度学习了。这方面我自己也是深度学习的新手，所以这方面需要你们自己发挥
