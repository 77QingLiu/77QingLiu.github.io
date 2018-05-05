> A follow up for [my paper in PharmaSUG China 2017](https://www.lexjansen.com/pharmasug-cn/2017/AD/PharmaSUG-China-2017-AD02.pdf)

SAS提供了很多方法来执行表查找操作，例如使用`if-then`语句，`format`语句，`merge`语句，甚至是`PROC SQL`。这里介绍一种通过哈希实现的表查询方法，不仅快速，而且简洁方便。

## 什么是表查找？
熟悉数据分析或者数据库的人应该不会陌生，所谓的表查找通常指的是通过一定的键组合，在另外的数据表里面查找对应的值。   
比如说一个表里面只有每个省的**简称**，例如湘，但是并不知道每个省的**全称**。省的全称存储在另外一个表中，这时候我们可以通过省的**简称**当做键值，通过表查找的方法从另外一个表中取得**全称**。   
用文字描述可能有点抽象，具体看下图。
![](http://p7ffgka2w.bkt.clouddn.com/18-5-3/91788580.jpg)


## 常用表查找方法
1. if-then statement      
  最简单的方法莫过于用if-then语句直接指定了。
  ```sas
  data states;
      if state = 'Virginia' then capital = 'Richmond';
      else if state = 'Georgia' then capital = 'Atlanta';
      ...
  ```
  但是这个方法不是很灵活，一旦数据更新，程序便要修改。
2. Merge statement      
  另外一个常见的操作是通过`merge`语句，通过键，将数据合并过来。
  ```sas
  proc sort data = StatesCapital; by state;run;
  proc sort data = States; by state;run;
  data new;
      merge StatesCapital States;
      by state;
  run;
  ```
  这个语句大概是每个SAS程序员最常用的方法了。但是，用`merge`比较烦人的一点，每次在数据合并之前，都要按键对数据进行排序。
3. PROC SQL       
  高级的SAS程序员可能会用SQL实现，代码如下
  ```sas
  proc sql;
      create table new as
      select a.state, b.capital
      from States as a, StatesCapital as b
      where a.state = b.state;
  quit;
  ```
  我个人是非常喜欢这种写法的，这样的写法既不用提前排序，也比较直观。

以上是SAS里面比较经典的表查找方法，也是程序里面用得比较多的方法，其他例如format之类的就不一一例举了。

---

## 哈希实现地表查找方法
喜欢折腾的人可能会用如下的方法
```sas
data new;
    if 0 then set work.StatesCapital;
    if _n_ = 1 then do;
        declare hash hh (dataset: "work.StatesCapital");
        hh.definedata("capital");
        hh.definekey("state");
        hh.definedone();
    end;
    set States;
        rc =hh.find();
        if rc = 0 then capital = capital;
run;
```
**如果不懂怎么使用SAS中的哈希表，可以参见[A Hands-on Introduction to SAS® DATA Step Hash Programming Techniques](https://www.lexjansen.com/mwsug/2016/HW/MWSUG-2016-HW02.pdf)**

在data步里面嵌入Hash语句，实现非常高效的表查找。这样的写法对于广大SAS用户来说，确实有点难以接受。一是因为其逻辑跟一般的SAS编程不一样，二是因为需要的语句较多，写起来费劲，维护起来也难。至于对于提高的那一丁点效率。大多数人是不在乎的，毕竟行业的数据量就那么多，少个0.1秒差别不是很大。

那么，有什么改进的办法呢？
在介绍改进方法之前，先简要介绍一下哈希表算法。

> 哈希表算法

[散列表（Hash table，也叫哈希表）](https://www.zhihu.com/question/20820286)，是根据关键码值(Key：value)而直接进行访问的数据结构。也就是说，它通过把关键码值映射到表中一个位置来访问记录，以加快查找的速度。通过哈希表，查找效率可以提升至$$O(1)$$

哈希表类似于字典里面的索引，通过索引我们能快速找到我们要查找的单词。也可以将哈希表理解成文章的摘要，通过摘要我们能快速查找到对应的文章。
![](http://p7ffgka2w.bkt.clouddn.com/18-5-3/28909375.jpg)

> 哈希表实现的自定义函数

上文中，在DATA步中使用哈希表实现表查找的方法，有点笨拙，恐怕大多数SAS用户无法接受这样的写法。那么，有什么办法可以改进呢？   

从SAS9.2开始，自定义函数模块[PROC FCMP](http://documentation.sas.com/?docsetId=proc&docsetVersion=9.4&docsetTarget=n0pio2crltpr35n1ny010zrfbvc9.htm&locale=en)里可以嵌套哈希表，从而实现自定义的表查找函数，具体的实现如下。

##### 首先我们自定义一个SAS函数，将哈希表查找嵌入函数中。
  ```sas
  proc fcmp outlib=work.functions.samples;
      * 这里定义函数的名字，以及表查找的key(同时需要制定key的类型)。
      注意如果返回值是字符型变量，则需要制定返回值长度以及类型(用$表示);
      function hash_fcmp(state $) $25;
      * 指定查找表的位置;
      declare hash hh(dataset: "work.StatesCapital");
      * 指定查找返回的变量;
      rc=hh.definedata("capital");
      * 指定查找的键
      rc=hh.definekey("state");
      rc=hh.definedone();
      * 如果找到键对应的值，则返回值，否则返回指定的值;
      rc=hh.find();
      if rc eq 0 then return(capital);
      else return('Not Found');
      endsub;
  quit;
  * 指定SAS调用自定义函数的位置；
  options cmplib=work.functions;
  ```
#####  然后便可以在DATA步或者SQL中直接调用     
  ```sas
  * In Data Step;
  data new;
      set states;
      capital = hash_fcmp(state);
  run;

  * In Proc SQL;
  proc sql;
      create table new as select *,hash_fcmp(state) as capital
      from states;
  quit;
  ```

这样一来，复杂的哈希语句就被嵌套在一个SAS自定义函数当中，使用者只需简单的调用这个函数，便可实现表查找操作。    


#### 下表给出了在`PROC FCMR`中调用`HAHS`的基本语法

Method | Syntax | Description
------ | ------ | -----------
DECLARE | DECLARE hash object-name | Create a new instance of hash object, create at parse time.
DEFINEKEY | rc = object.DEFINEKEY('key 1','key n') | Set up key variables for hash object
DEFINEDATA | rc = object.DEFINEDATA('dataset 1','dataset n') | Define data to be stored in hash object
DEFINEDONE | rc = object.DEFINEDONE() | Indicate the key and data specification is completed
DELETE | rc = object.DELETE() | Delete the hash object and free any resources allocated
FIND | rc = object.FIND('key1','keyn') | Search a hash object based on the values of defined key, If look up is successful, defined data variable are updated
CHECK | rc = object.CHECK() | Search a hash object based on the values of defined key, data will not be updated whether If look up is successful
NUM_ITEMS| rc = object. NUM_ITEMS()|  Return the number of items in hash object
ADD | rc = object.ADD(key: value1, key: value n) | Add data with associated key to hash object
REMOVE | rc = object.REMOVE(key: value1, key: value n) | Remove data with associated key to hash object

> 为什么要使用哈希表实现的自定义函数?

原因很简单，因为这种用法很简单、高效！

# 实践
前面讲了这么多原理，下面讲一个有意思地应用。通过自定义哈希表函数，实现一些平时在SAS中不太容易实现的操作。

#### 给定字符与每个字符对应的数值，此数值存放在表CharNum中。

char | val
---  | ---
a    | 1
b    | 2
c    | 3
d    | 4
...  | ...
z    | 26

给定一个字符串，求字符串对应的数值的总和？例如，字符串'abc'对应的数值为：1 + 2 + 3 = 6

### SAS实现

要解决这个问题，普通的SAS实现方法有一定的难度。但是通过哈希表自定义函数，可以很快地解决这个问题。    

首先定义一个哈希函数。
```sas
proc fcmp outlib=width.functions.GetNum;
    function GetNum(char $);
    * Define Hash Table with Character Width Dataset;
    declare hash Calculate(dataset: "work.CharNum");
    rc = Calculate.defineKey("char");
    rc = Calculate.defineData("val");
    rc = Calculate.defineDone();

    * Retrieve Data from Hash and Sum up;
    rc = Calculate.find();
    if rc eq 0 then return(val);
    endsub;
run;
```

在定义好函数之后是，直接调用这个函数便可得到字符串值。
```sas
data _null_;
    string = 'abc';
    num = 0;
    do i = 1 to lengthn(string);
        char = substr(string,i,1);
        num = num + GetNum(char);
    end;
    put num =;
run;
>> 6
```

你甚至可以将循环嵌入自定义函数中，这样使用起来更方便
```sas
proc fcmp outlib=width.functions.GetNum;
    function GetNum(char $);
    * Define Hash Table with Character Width Dataset;
    declare hash Calculate(dataset: "work.CharNum");
    rc = Calculate.defineKey("char");
    rc = Calculate.defineData("val");
    rc = Calculate.defineDone();
    val_tot = 0;
    * Retrieve Data from Hash and Sum up;
    do i = 1 to lengthn(string);
        char = substr(string,i,1);
        rc = Calculate.find();
        if rc eq 0 then val_tot = val_tot+val;
    end;     
    return(val_tot);
    endsub;
run;
```
可以在DATA步中直接调用
```sas
data _null_;
    string = 'abc';
    num = GetNum(string);
    put num =;
run;
>> 6
```

因为SAS中缺少一些高级的数据结构，因此想要实现上述功能确实有点绕。下面给出Python中的实现方式，大家可以体会到Python的强大之处。
```python
HashTable = {'a':1, 'b':2, ..., 'z':26}
num = 0
string = 'abc'
for char in string:
    num += HashTable[char]
print(num)
>> 6
```

# 总结
通过在PROC FCMP中嵌入Hash进行表格查找并不是简单地提高查询效率，而是为了简化日常工作，增强程序可读性。另外，这种新的写法一定程度上也扩展了SAS的功能。    
有兴趣的可以参阅一下文档，了解更多。   
[Hashing in PROC FCMP to Enhance Your Productivity](http://www.lexjansen.com/wuss/2013/141_Paper.pdf)     
[Load a SAS data set into a Hash Object using PROC FCMP](http://support.sas.com/kb/47/224.html)      
[PROC FCMP and DATA Step Component Objects](http://documentation.sas.com/?docsetId=proc&docsetVersion=9.4&docsetTarget=n03uc8c8fkguxqn1i5iapv1auqrz.htm&locale=en)    
