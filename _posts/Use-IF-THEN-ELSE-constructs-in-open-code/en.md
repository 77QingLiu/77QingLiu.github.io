SAS programmers have long wanted the ability to control the flow of their SAS programs without having to resort to complex SAS macro programming. With **SAS 9.4 Maintenance 5**, use `%IF-%THEN-%ELSE` constructs in open code is now supported! 

Prior to this change, the following error would raise if someone use macro control statement in the open SAS code.
```
ERROR: The %IF statement is not valid in open code.
```

And if one have to nest the macro control flow statement within a macro routine:
![](http://img.77qingliu.com/18-8-21/69075612.jpg)

with the new SAS realease, we can simplify this code to remove the `%MACRO/%MEND` wrapper and the macro call:
![](http://img.77qingliu.com/18-8-21/66970828.jpg)

# Some additional ideas for how to use this feature. 

### Run "debug-level" code only when in debug mode
When developing your code, it's now easier to leave debugging statements in and turn them on with a simple flag.
![](http://img.77qingliu.com/18-8-21/87343127.jpg)

### Run code only on a certain day of the week
I have batch jobs that run daily, but that send e-mail to people only one day per week. Now this is easier to express inline with conditional logic.
![](http://img.77qingliu.com/18-8-21/35865536.jpg)

### Check a system environment variable before running code
For batch jobs especially, system environment variables can be a rich source of information about the conditions under which your code is running. You can glean user ID information, path settings, network settings, and so much more. 
![](http://img.77qingliu.com/18-8-21/58142359.jpg)

# Limitations of %IF/%THEN in open code
As awesome as this feature is, there are a few rules that apply to the use of the construct in open code. These are different from what's allowed within a %MACRO wrapper.

* `%IF/%THEN` must be followed by a `%DO/%END` block for the statements. The same is true for any statements that follow the optional %ELSE branch of the condition.
* No nesting of multiple `%IF/%THEN` constructs in open code.
* the MLOGIC Option does NOT show any execution trace information in the SAS log for the `%IF %THEN` statement when used in Open Code.

# Is it too late? 
> Am I the only one who feels like this is around 20 years late?
Are we so excited about this simply because the SAS base language has lacked modern programming constructs for so long? - Scott Bass

Scott Bass comments that SAS has been lack of modern programming constructs for a long time. such as this:
```python
def foo(a,b);
   return a**b;

data foo;
   do x=1 to 10;
      do y=1 to 5;
         z=foo(x,y);  
         # not proc fcmp...a "proper" support of open code function definitions 
      end
   end;
run;

if foo.nobs = 0 then do:
   print("foo is empty";)
end;

name_lst = ["class","stocks","shoes"]
for name in name_lst:
   data.output=catx(".","work",name);
      set.input=catx(".","sashelp",name);
   run;
end; 
```

I totally agree with him!

SAS, a typical Process-oriented programming, although the data step language is great for data processing, has been outdated for a long time compared with modern object-oriented languages like Python, Java, C#. I sometimes just feel tired as the same as Scott Bass.

Considering the following scenario, I'd like to construct control flow depending on the observation of dataset. In normal SAS code, I would write like this:
![](http://img.77qingliu.com/18-8-21/22622999.jpg)
This is a very typical style of Process-oriented programming, and the process can be divided into three process.
![](http://img.77qingliu.com/18-8-21/53101903.jpg)

But, how can we construct this control flow in modern programming languages?
Ideally, it would look like this:
![](http://img.77qingliu.com/18-8-21/25705243.jpg)
```

I know SAS is married to the idea that 40-year-old code still runs, but I wish there are some `resolution`, not some slight modification!