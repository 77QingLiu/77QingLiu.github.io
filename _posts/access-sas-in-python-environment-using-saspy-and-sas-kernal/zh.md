在2017年初，[SAS官方](https://communities.sas.com/t5/Base-SAS-Programming/Announcing-SASPy-programming-SAS-from-Python/td-p/343050)发布了[SASPy ](https://github.com/sassoftware/saspy)从[Github上的SAS](https://github.com/sassoftware)。 SASPy是一个Python包，通过这个包，可以在Python环境中直接运行SAS代码。这对于那些对SAS和开源软件集成感兴趣的用户来说，这是一大进步。

根据我的理解，SASPy将python对象和方法转换为SAS代码，将转换后的SAS代码发送到SAS 9.4并执行，然后将结果返回给Python环境。
因此，你必须有本地或远程安装SAS软件，并且需要** SAS Base **，所以想要使用SASPy，还是必须购买SAS软件。

想要在Python中连接SAS，根据不同的系统SASPy中有不同的方法，接下来，我主要描述在**Windows客户端**上通过使用** IOM方法 **进行连接的两种方法：
* ** Windows环境中的本地SAS **
* ** Linux环境下([SAS Grid Manager](https://www.sas.com/en_us/software/foundation/grid-manager.html)中的远程SAS)**

## 前提配置
* Python3或更高版本。
* SAS 9.4或更高版本。
* 客户端上的Java
* SAS Integration Technologies客户端的四个JAR文件(可在SAS安装中找到或[在此下载](https://support.sas.com/downloads/package.htm?pid=607))。

## 安装软件包
* 在命令行中安装
```Python
# 使用pip
pip安装saspy
# 或使用conda(如果您通过Anaconda安装python)
conda安装
```
* 或下载软件包并安装
  1. 从[SAS Github](https://github.com/sassoftware/saspy)下载Python软件包，
  2. 解压压缩包，切换到包文件夹，然后在命令行中执行`python setup.py install`

## 设置SASpy
#### 配置
SASPy支持连接到Unix，大型机和Windows上的SAS。也可以连接到本地或远程SAS。 **不同的环境有不同的设置**，在配置之前，先确定访问类型。本文将解释两种在Windows环境下的访问方法：
1. 连接**本地Windows SAS **
2. 连接**远程Linux SAS(SAS metadataserver)**

这两种方法都使用[IOM连接](https://sassoftware.github.io/saspy/troubleshooting.html#iom)

###### 找到配置文件
名为`sascfg.py`的配置文件位于SASPy软件包所在的位置。
对于Anaconda安装，配置通常位于`Continuum\anaconda3\Lib\site-packages\saspy`中。
也可以通过`import saspy`找到这个包。然后，只需提交`saspy.SAScfg`。 Python会告诉你它在哪里找到模块。

###### 复制sascfg_personal.py
`saspy.cfg`文件位于saspy repo中，仅仅作为示例配置文件进行更新，或者进行替换。在更新SASPy之后，文件可能会丢失。为了保险起见，复制`sascfg.py`并重命名为`sascfg_personal.py`。 SASPy总是会首先尝试导入`sascfg_personal.py`，并且只有在失败时才会尝试导入sascfg.py。

###### 设置sascfg_personal.py
1. 只包含两个SAS_config_names'SAS_config_names = ['winiomlinux'，'winlocal']`，代表了两种方法。
  - 用于本地Windows连接的`winlocal`
  - 用于远程Linux连接的`winiomlinux`
2. 设置CLASSPATH以访问SAS Java IOM客户机JAR文件。总共五个Java JAR文件 - 可以从现有SAS安装中获得四(4)个JAR文件，以及一个随SASPy包一起提供的JAR文件：saspyiom.jar。必须在CLASSPATH环境变量中提供这五个JAR文件(完全限定路径)。在sascfg.py文件中可以以非常简单的方式完成，如下所示：

```python
    #四个SAS安装JAR文件
    cpW = r"C：\ Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
    cpW + = r"; C：\ Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\log4j.jar"
    cpW + = r"; C：\ Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
    cpW + = r"; C：\ Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\sas.core.jar"
    #一个来自SASPy包
    cpW + = r"; C：\ Users\qing\AppData\Local\Continuum\anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"
```

3. 为本地和远程连接设置不同的参数
  - *访问本地Windows SAS。*
    ```python
    winlocal = {'java'：r'C：\ Program Files(x86)\ Java\jre7\bin\java'，
            'encoding'：'windows-1252'，
            'classpath'：cpW
            }
    ```
    ** java ** - (必需)要使用的Java可执行文件的路径。在Windows命令行内输入java，可以找到java的可执行文件的路径。

      ** encoding ** - Python内的编码值，它跟要连接的IOM服务器的SAS编码一致。 WLATIN1是在Windows上运行SAS的默认编码。映射到Python内的编码值为：windows-1252。

      ** classpath ** - 上一步中指定的五个JAR文件

     - *访问远程Linux SAS。*
      ```python
      winiomlinux = {'java'：r'C：\ Program Files（x86）\ Java \ jre7 \ bin \ java'，
            'iomhost'：'server.domain.address.com'，
            'iomport'：8597，
            'encoding'：'latin1'，
            'classpath'：cpW，
            'authkey'：'IOM_Prod_Grid1'
            }
      ```
      ** java ** - 与本地Windows配置一样
      ** iomhost ** - （必需）可解析的主机名或IOM Linux服务器的IP地址。
      ** iomport ** - （必需）对象spawner侦听工作区服务器连接的端口。
      `iomhost address`和`iomport number`可以通过提交下面SAS语得到。
      ```SAS
      proc iomoperate
        URI = 'IOM：//metadataserver.com：8564;桥; USER = my_user，PASS = MY_PASS';
        list DEFINED FILTER ='Workspace';
      quit;
      ＃ metadataserver地址可以通过下面的方式找到：
          单击工具 - >单击连接 - >在SAS EG中的配置文件
      ```
      **编码** - 与本地Windows配置一样

      ** classpath ** - 与本地Windows配置一样

      ** authkey ** - 用户名和密码。

      > IOM访问方法支持从用户主目录中的authinfo文件获取所需的用户/密码，而不是提示用户/密码输入。在Windows上，它的名字是_authinfo。 authinfo文件中行的格式如下。
      第一个值是您为authkey指定的authkey值。接下来是'用户'键，后面是值（用户ID），然后是'密码'键，后面跟着它的值（用户的密码）。注意该文件有权限。在Windows上，这个文件应锁定在只有所有者可以读写的位置。
      例如，用户Bob的主目录中的authinfo文件的密码为BobsPW1将在其中包含一行，如下所示：
      `IOM_Prod_Grid1用户Bob密码BobsPW1`


## 开始
一旦完成安装和配置，就可以在Python中直接使用这个包。

#### 初始化
```Python
import saspy
import pandas as pd
from IPython.display import HTML
```

#### 启动SAS会话
下面使用winlocal配置开始一个名为sas的SAS会话。如果忽略cfgname选项，SAS弹出一个窗口，让你输入config信息。
建立连接并启动SAS会话后，将显示与下面类似的注释。
![sassession](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/sassession.png)

#### 开始数据分析
有三种方法进行分析：
1.通过内置SASPy方法。
2.将SAS数据集转换为Pandas Dataframe，通过pandas进行分析
3.通过SASPy直接提交SAS代码


###### 使用SASPy内置方法进行分析
* Data inspection
![SASPy_1](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-1.png)
* Descriptive Statistics
![SASPy_2](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-2.png)
*  Simple bar chart
![SASPy_3](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-3.png)

###### 使用pandas进行数据分析
* SAS dataset to Pandas Dataframe & data inspection
![SASPy_4](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-4.png)
* Correlation matrix
![SASPY_5](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-5.png)
* Correlation heat map
![SASPy_8](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-8.png)

###### 直接提交SAS代码进行分析
* A simple scatter chart
![SASPy_6](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-6.png)

## 结论
 更多的文字，参阅该软件包的文档：[saspy](https://sassoftware.github.io/saspy/)
