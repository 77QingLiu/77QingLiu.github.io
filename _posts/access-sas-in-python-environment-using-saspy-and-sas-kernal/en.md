In early 2017, [SAS announce](https://communities.sas.com/t5/Base-SAS-Programming/Announcing-SASPy-programming-SAS-from-Python/td-p/343050) the release of [SASPy](https://github.com/sassoftware/saspy) from [SAS on Github](https://github.com/sassoftware). The SASPy is a Python package enables you to connect to and run your analysis code from SAS 9.4.

> SASPy brings a "Python-ic" sensibility to this approach for using SAS. That means that all of your access to SAS data and methods are surfaced using objects and syntax that are familiar to Python users.
>This is a fantastic expansion of functionality and a huge step forward for those interested in Open Source Integration with SAS.

In a word, SASPy translates the python objects and methods into the SAS code, send the translated SAS code to SAS 9.4 and execute, then return the results to Python environment.
This means a SAS software should be installed locally or remotely, and **SAS Base** is needed. **You must buy a SAS licence before using SASPy.**

In the comming paragraphs, I will outlines how to setup SASPy **on Windows client** to connect two types of SAS using **IOM method**:
* **local SAS** in **Windows environment**
* **remote SAS** in **Linux environment([SAS Grid Manager](https://www.sas.com/en_us/software/foundation/grid-manager.html))**

## Prerequirement
* Python3 or higher.
* SAS 9.4 or higher.
* Requires Java on the client
* Requires four JAR files from SAS Integration Technologies Client(can be found in your SAS installation or [download here](https://support.sas.com/downloads/package.htm?pid=607)).

## Install the Package
* Install in command line
```python
# using pip
pip install saspy
# or using conda(if you install python by Anaconda)
conda install
```
* Or download package and install
  1. download the Python package from [SAS Github](https://github.com/sassoftware/saspy)
  2. extract the package, change to the package folder, and execute `python setup.py install` in command line

## Setting The SASpy
#### Configuration
SASPy support connect to SAS on Unix, Mainframe, and Windows. It can connect to a local SAS session or remote session. **Different environment has different settings.** So you should determine your access type before configuration. Two access method will be explained in this article:
1. Connect **local Windows SAS**
2. Connect **remote Linux SAS(a SAS metadataserver)**
both method using [IOM connection](https://sassoftware.github.io/saspy/troubleshooting.html#iom)

###### Find the configuration file
The configuration file called `sascfg.py` is located in where you SASPy package is located.
For Anaconda installation, the config generally located in `Continuum\anaconda3\Lib\site-packages\saspy`.
Your can also find the package by `import saspy`. Then, simply submit `saspy.SAScfg`. Python will show you where it found the module.

###### Copy a sascfg_personal.py
Since the `saspy.cfg` file is in the saspy repo, as an example configuration file, it can be updated on occasion or be replaced.
To avoid file lose, simply copy the `sascfg.py` and rename to `sascfg_personal.py`. saspy will always try to import `sascfg_personal.py` first, and only if that fails will it try to import sascfg.py.

###### Setting in sascfg_personal.py
1. Include only two SAS_config_names `SAS_config_names=['winiomlinux', 'winlocal']`
    - `winlocal` for local Windows connection
    - `winiomlinux` for remote Linux connection
2. Setting CLASSPATH to access the SAS Java IOM Client JAR files. Total five Java JAR files are requited - four (4) JAR files are available from your existing SAS installation, and one JAR file that is provided with SASPy package: saspyiom.jar. These five JAR files must be provided (fully qualified paths) in a CLASSPATH environment variable. This is done in a very simple way in the sascfg.py file, like so:
    ```python
    # Four SAS installation JAR files
    cpW  =  r"C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
    cpW += r";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\log4j.jar"
    cpW += r";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
    cpW += r";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94420__prt__xx__sp0__1\deploywiz\sas.core.jar"
    # One come from SASPy package (located in your python package location)
    cpW += r";C:\Users\qing\AppData\Local\Continuum\anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"
    ```

3. Setting different parameter for local and remote connection
    - *access local Windows SAS.*
      ```python
      winlocal = {'java'      : r'C:\Program Files (x86)\Java\jre7\bin\java',
            'encoding'  : 'windows-1252',
            'classpath' : cpW
            }
      ```
      **java** - (Required) The path to the Java executable to use. On Windows, you might be able to simply enter java. If that is not successful, enter encoding - the fully qualified path.

      **encoding** - This is the Python encoding value that matches the SAS session encoding of the IOM server to which you are connecting. WLATIN1 are the default encodings for running SAS on Windows. Those map to Python encoding values: windows-1252.

      **classpath** - The five JAR files specified in previous step

    - *access remote Linux SAS.*
      ```python
      winiomlinux = {'java'   : r'C:\Program Files (x86)\Java\jre7\bin\java',
            'iomhost'   : 'server.domain.address.com',
            'iomport'   : 8597,
            'encoding'  : 'latin1',
            'classpath' : cpW,
            'authkey'   : 'IOM_Prod_Grid1'
            }
      ```
      **java** - same as local Windows

      **iomhost** - (Required) The resolvable host name, or IP address to the IOM Linux Server.

      **iomport** - (Required) The port that object spawner is listening on for workspace server connections.
      `iomhost address` and `iomport number` can be got with the following SAS statement.
      ```sas
      proc iomoperate
        uri='iom://metadataserver.com:8564;Bridge;USER=my_user,PASS=my_pass';
        list DEFINED FILTER='Workspace';
      quit;
      # metadataserver address can be found by:
          click Tools -> click Connections -> Profiles in SAS EG
      ```
      **encoding** - same as local Windows

      **classpath** - same as local Windows

      **authkey** - The keyword that starts a line in the authinfo file containing user and or password for this connection.

      > The IOM access method has support for getting the required user/password from an authinfo file in the user’s home directory instead of prompting for it. on windows, it's name is _authinfo. The format of the line in the authinfo file is as follows.
      The first value is the authkey value you specify for authkey. Next is the 'user' key followed by the value (the user id) and then 'password' key followed by its value (the user’s password). Note that there are permission rules for this file. On Windows, the file should be equally locked down to where only the owner can read and write it.
      For example, The authinfo file in the home directory for user Bob, with a password of BobsPW1 would have a line in it as follows:
      `IOM_Prod_Grid1 user Bob password BobsPW1`


## Getting start
Once you have already done the installation and configuration, you can use the package in Python.
#### Initial import
```Python
import saspy
import pandas as pd
from IPython.display import HTML
```

#### Start a SAS session
In the following code we start a SAS session named sas using the winlocal configuration. You can ignore the cfgname option, SAS will pop up a window with connection method
After a connection is made and a SAS session is started, a note that is similar to the the one below is displayed.
![sassession](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/sassession.png)

#### Begin data analysis
There are 3 ways to make you analysis code:
1. With built-in SASPy Method.
2. With Pandas by converting SAS dataset to Pandas Dataframe
3. Submitting SAS Code directly


###### Analysis with SASPy built-in Method
* Data inspection
![SASPy_1](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-1.png)
* Descriptive Statistics
![SASPy_2](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-2.png)
*  Simple bar chart
![SASPy_3](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-3.png)

###### Analysis with Pandas
* SAS dataset to Pandas Dataframe & data inspection
![SASPy_4](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-4.png)
* Correlation matrix
![SASPY_5](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-5.png)
* Correlation heat map
![SASPy_8](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-8.png)

###### Analysis by Submitting SAS Code directly
* A simple scatter chart
![SASPy_6](/img/in-post/access-sas-in-python-environment-using-saspy-and-sas-kernal/saspy-6.png)

## Conclusion
 For more background, refer the documentation for the package: [saspy](https://sassoftware.github.io/saspy/)
