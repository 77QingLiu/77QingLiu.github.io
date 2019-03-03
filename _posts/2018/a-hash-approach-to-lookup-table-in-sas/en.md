> A follow up for [my paper in PharmaSUG China 2017](https://www.lexjansen.com/pharmasug-cn/2017/AD/PharmaSUG-China-2017-AD02.pdf)

SAS provides many ways to perform table lookups operation, such as using `if-then` statement in DATA step, or `format` statement, or `merge` statement, and  even `PROC SQL`. Here, I'll introduce a new approach to look-up table which utilizes the HASH function. It's not only efficient but also simple and convenient.

## What is table lookup？
Table lookup should be familiar to anyone with data analysis or database. The so-called table lookup usually refers to finding corresponding values in another data table through certain key combinations. For example, there is one table called A and there is only state ID in this dataset and there is another table called B which have both state ID and state capital, and I'd like to know the corresponding capital for each state in table A. How can we achieve this? The answer is table look up. The text description may be a little abstract, see the figure below.
![](http://img.77qingliu.com/18-5-3/91788580.jpg)


## Frequently used table lookup methods
1. if-then statement
The simplest way is the use the `if-then` statement directly.
```sas
data states;
    if state = 'Virginia' then capital = 'Richmond';
    else if state = 'Georgia' then capital = 'Atlanta';
    ...
```
However, this way is not very flexible as the program must be modified once data is updated.
2. Merge statement
Another common operation is to use the `merge` statement.
```sas
proc sort data = StatesCapital; by state;run;
proc sort data = States; by state;run;
data new;
    merge StatesCapital States;
    by state;
run;
```
This statement is probably the most common method in SAS programmers daily life. A annoying part is that dataset should be sorted before merge operation.

3. PROC SQL
Advanced SAS programmers may use SQL
```sas
proc sql;
    create table new as
    select a.state, b.capital
    from States as a, StatesCapital as b
    where a.state = b.state;
quit;
```
Personally, I prefer this way. In this way, there is no need to sort the data in advance, and it is also intuitive.


These examples cited above are some classic table lookup table method in SAS, and it is also the most often used in SAS program.

---

## Hash way to table lookup
People who like tossing may use the following method
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
**if you do not know the hash method, you can see[A Hands-on Introduction to SAS® DATA Step Hash Programming Techniques](https://www.lexjansen.com/mwsug/2016/HW/MWSUG-2016-HW02.pdf)**

Hash in data step is very efficient. But it's a bit difficult to adult for the majority of SAS users. The first reason is that the program logic behind hash is not the same as general SAS programming, and the second is that more statements are required compared with `merge` or `SQL` and thus the program is harder to maintain.

As for the slightes improvement in efficiency, most people do not care.

So, how can we improve？
let's get familiar with the hash table algorithm before introducing the improved methods.

> Hash Table algorithm

A HASH table is a data structure that enables you to accessed value quickly according to a key value.
That is, it accesses records by mapping key values to a location in the table to speed up the search. Through the hash table, the search efficiency can be improved to$$O(1)$$

The Hash table is similar to the index in the dictionary. Through the index we can quickly find the word we are looking for.   
You can also compare the hash table to the summary of the article. Through the summary, we can quickly find the corresponding article.
![](http://img.77qingliu.com/18-5-3/28909375.jpg)

> Hash table in FCMP

in the above, we use Hash in DATA step to implement table lookup. it's a little clumsy, and I am afraid that most SAS users cannot accept such a wording. So, how can we improve it?

Starting from SAS9.2，Hash statement can be embedded in [PROC FCMP](http://documentation.sas.com/?docsetId=proc&docsetVersion=9.4&docsetTarget=n0pio2crltpr35n1ny010zrfbvc9.htm&locale=en) to define a customed table lookup function. The specific implementation is as follows.

* Firstly, we define a customized SAS function through FCMP, and then embeded the Hash statement in the function.
  ```sas
  proc fcmp outlib=work.functions.samples;
      * Define function name as well as the lookup key(the type of key needs to be specified at the same time). Notice that if the return value is character type, you need to specify the length and type of the return value(indicated by $);
      function hash_fcmp(state $) $25;
      * specify location of lookup table;
      declare hash hh(dataset: "work.StatesCapital");
      * specify data variable to be returned;
      rc=hh.definedata("capital");
      * specify the key
      rc=hh.definekey("state");
      rc=hh.definedone();
      * if find the corresponding value then return, otherwise return the specified value
      rc=hh.find();
      if rc eq 0 then return(capital);
      else return('Not Found');
      endsub;
  quit;

  * Don't forget to specify where SAS to call the function
  options cmplib=work.functions;
  ```
*  then we can use this function in data step or SQL directly
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
In this way, complex hash statements are nested within a SAS custom function. Users could simply invoke this function to perform table lookups.  


The following table shows the basic syntax for calling `HAHS` in `PROC FCMP`

Method | Syntax | Description
------ | ------ | -----------
DECLARE | DECLARE hash object-name | Create a new instance of hash object, create at parse time.
DEFINEKEY | rc = object.DEFINEKEY('key 1','key n') | Set up key variables for hash object
DEFINEDATA | rc = object.DEFINEDATA('dataset 1','dataset n') | Define data to be stored in hash object
DEFINEDONE | rc = object.DEFINEDONE() | Indicate the key and data specification is completed
DELETE | rc = object.DELETE() | Delete the hash object and free any resources allocated
FIND | rc = object.FIND('key1','keyn') | Search a hash object based on the values of defined key, If look up is successful, defined data variable are updated
CHECK | rc = object.CHECK() | Search a hash object based on the values of defined key, data will not be updated whether If look up is successful
NUM_ITEMS | rc = object. NUM_ITEMS() | Return the number of items in hash object
ADD | rc = object.ADD(key: value1, key: value n) | Add data with associated key to hash object
REMOVE | rc = object.REMOVE(key: value1, key: value n) | Remove data with associated key to hash object


> Why should we use Hash in FCMP?

The reason is simple, because it's simplicity and efficiency!

# Practice
here's an straightforward and interesting application. By defining hash in FCMP, we can achieve some operations that are usually not easily implemented in SAS.

> Assume that there are corresponding numeric value to each character.

char | val
---  | ---
a    | 1
b    | 2
c    | 3
d    | 4
...  | ...
z    | 26

> Given a string，you are required to sum the numeric value of this string。For example, the corresponding numeric value of 'abc' is：1 + 2 + 3 = 6

* SAS implementation

we can call this function directly to get the numeric value.
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

and the customized function is beening defined like this
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

you can even embed loops in the fuction to make it more simple.
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
and call it directly in data step
```sas
data _null_;
    string = 'abc';
    num = GetNum(string);
    put num =;
run;
>> 6
```

Because of the lack of some advanced data structures in SAS, it is a bit tricky to implement these functions. The following gives the implementation in Python, we can appreciate the power of Python.
```python
HashTable = {'a':1, 'b':2, ..., 'z':26}
num = 0
string = 'abc'
for char in string:
    num += HashTable[char]
print(num)
>> 6
```

# Summary
Table lookup by embedding Hash in PROC FCMP not only simply increase query efficiency, but also simplifies routine work and enhances program readability. In addition, this new style of writing also expands the functionality of the SAS to some extent.
Interested people can refer to the documentation to learn more.   
[Hashing in PROC FCMP to Enhance Your Productivity](http://www.lexjansen.com/wuss/2013/141_Paper.pdf)     
[Load a SAS data set into a Hash Object using PROC FCMP](http://support.sas.com/kb/47/224.html)      
[PROC FCMP and DATA Step Component Objects](http://documentation.sas.com/?docsetId=proc&docsetVersion=9.4&docsetTarget=n03uc8c8fkguxqn1i5iapv1auqrz.htm&locale=en)    
