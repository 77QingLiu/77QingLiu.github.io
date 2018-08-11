在现实世界里，数据的获取有时候是一个比较难的点，这时候就需要通过各种黑科技来获取正常途径得不到的数据源来，比如爬虫。

最近工作需要从百科以及CFDA上面爬取一些数据，这里记录一下自己爬过的坑～

# 什么爬虫
简而言之，爬虫是使用任何技术手段，批量获取网站信息的一种方式。
而爬虫与普通爬取不同在于：是否**批量**。

# 爬虫的原理
当我们在浏览器中输入一个url后回车，后台会发生什么？比如说你输入http://www.baidu.com/
![此处输入图片的描述][1]
简单来说这段过程发生了以下四个步骤：

* 查找域名对应的IP地址。
* 向IP对应的服务器发送请求。
* 服务器响应请求，发回网页内容。
* 浏览器解析网页内容。

而网络爬虫的本质在于模拟这一系列的操作，即通过程序批量实现，进而获得浏览器返回的数据。

通常，爬虫有两种实现形式：

1. 模拟浏览器操作
2. 模拟http请求

# 如何编写简单爬虫

通常编写爬虫需要经过这么几个过程：

* 分析页面数据格式
* 创建合适的http请求
* 批量发送http请求，获取数据

### 如何分析页面数据格式？
以百科为例，
![](http://p7ffgka2w.bkt.clouddn.com/18-8-9/18470634.jpg)

这里进入百科关键词页面，按下F12或者右键点击`检查`之后，浏览器右边便会展现网页的源代码。

我们需要从这些html源代码里面找到我们需要的信息。
这些源代码虽然有一定的规则，但是里面含有太多我们不关注的信息，而如何从这些不相关信息里面找到我们想要的数据是一个难题。

最粗暴的办法是使用字符串匹配（如[正则表达式](https://zh.wikipedia.org/zh-hans/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F)）将数据提取出来，但这样做很麻烦，好在前人已经帮我们写好了大量的html解析工具，例如Python里面比较出名的[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)。


### 如何创建合适的http请求？
这里存在两种办法。

1. 直接向网址发送网络请求([Requests](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html))
2. 模拟浏览器发送请求([Selenium](http://selenium-python.readthedocs.io/))

##### Requests
[Requests](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)，它是 GitHub上关注数最多的 Python 项目之一，Requests 的作者是Python社区中的明星[Kenneth Reitz](https://www.kennethreitz.org/)(PS, 这里还有关于它的小故事，[谁说程序员不是潜力股？](https://zhuanlan.zhihu.com/p/22332669))，具体的使用方法参见知乎上这篇文章[requests:你爬虫的第一步](https://zhuanlan.zhihu.com/p/21976757)。

##### Selenium
[Selenium](https://www.seleniumhq.org/)是一个用于自动化Web应用程序测试的工具，但功能不仅限于此。[Selenium](http://selenium-python.readthedocs.io/)可以直接操作浏览器，就像真正的用户在操作一样，这样就可以获得浏览过的数据。具体使用使用方法参见这篇文章[有了selenium，小白也可以自豪的说：“抓包，cookie，去一边吧！](https://zhuanlan.zhihu.com/p/25981552)。

##### 用Requests还是Selenium？
首先明确一个概念：**网页 = html + javascript + css**。
其中html作为网页的主体，存放着静态数据；而javascript加载动态内容，比如一些图像、动画、视频以及一些动态数据等等；css调整输出的格式。

我们需要的数据要么可以直接在html中找到，要么通过javascript加载。而通过js加载的数据直接使用Requests请求目标网站是得不到的，返回的数据可能是一大堆看不懂的javascript，比如
```javascript
var Monkey=Monkey||{};void function(P){var b=window,D=document,x=encodeURIComponent,r=Math,L=parseInt;if(!document.body.getBoundingClientRect){return}var p=[{getPage:function(){var i;String(D.location).replace(/http:\/\/baike\.baidu\.com\/view\/(\d+)\.htm/i,function(Z,aa){i="view-"+aa});return i},postUrl:"http://nsclick.baidu.com/u.gif",product:103,hid:2254,reports:{click:1,refer:1,staytime:1,pv:1}}],F,V=0;while(F=p[V++]){if(F.page=F.getPage()){break}}if(!F){return}var K=[["mousedown","d"],["scroll","s",b],["resize","e",b],["beforeunload","z",b],["unload","z",b],["focusout","o"],["blur","o",b],["focusin","i"],["focus","i",b]],T,f=(b.ALog&&ALog.t&&ALog.t.st)||new Date,s=(b.ALog&&ALog.sid)
```
让人头痛的是这种情况不在少数，现代网站中都存在大量的动态javascript加载内容。

想要获得动态加载的内容有两种方法：

1. 找到网页中隐藏的数据接口
2. 使用Selenium模拟浏览器操作

第一种方法需要比较懂前端和网络，对于初学者难度很大；而Selenium则给新手提供了一个简单粗暴方便的方法。

但是个人认为，**不到万不得已，不推荐使用Selenium**。
吐槽一下Selenium 的缺点：

1. 速度慢。每次运行爬虫都打开一个浏览器，如果没有设置，还会加载图片、JS等等一大堆东西；使用Selenium的速度至少比Request少一个量级。
2. 占用资源太多。打开一个浏览器
3. 对网络的要求会更高，中间更可能中断。 Selenium 加载了很多可能对您没有价值的补充文件（如css，js和图像文件）。 与仅仅请求您真正需要的资源（使用单独的HTTP请求）相比，这会产生更多的流量。
4. 爬取规模不能太大，效率很低
5. 学习Selenium的成本高，Selenium比Requests复杂

对于两种方法的比较可以参见这篇文章[为什么不推荐Selenium写爬虫](https://zhuanlan.zhihu.com/p/33542626)

因此在选择爬虫方法时，首选requests；如果碰到动态javascript内容，首先考虑有没有隐藏的数据接口（可以翻百度看别人分析出的接口），实在没有其他办法再考虑上Selenium。
选择强迫症患者可以看下这篇文章，[想要用 python 做爬虫， 是使用 scrapy框架还是用 requests, bs4 等库？](https://www.zhihu.com/question/32169632/answer/172230898)

### 如何批量发送http请求？
通过循环即可批量发送http请求，python里面如
```python
for link in links:
    scrape(link)
```

# 爬虫：以百科为例
这里用爬取百度百科页面做一个演示，首先进入需要爬取的页面。
![](http://p7ffgka2w.bkt.clouddn.com/18-8-10/39919199.jpg)

### 分析页面数据格式
确定爬取内容：

* 简介
* 相关关键词

打开网页的源代码，确定爬取目标在html中的位置
![](http://p7ffgka2w.bkt.clouddn.com/18-8-10/75586573.jpg)
例如，可以看到`中文名`这个关键词嵌套在
```html
<dd class="basicInfo-item value">
网络爬虫
</dd>
```
这个tag里面。我们可以通过[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)定位到该元素，并抓取到里面的文本。


### 选择合适的抓取方法
在不确定目标信息是否是动态生成的时候，可以直接使用requests发送http请求，在获得html后直接检查是否含有我们需要的信息
```
import requests
url = 'https://baike.baidu.com/item/网络爬虫'
page_response = requests.get(url, timeout=5)
page_response.content.decode('utf-8')
```
输出
```
<!DOCTYPE html>\n<!--STATUS OK-->\n<html>\n\n\n\n<head>\n<meta charset="UTF-8">\n<meta http-equiv="X-UA-Compatible" content="IE=Edge" />\n<meta name="referrer" content="always" />\n<meta name="description" content="网络爬虫（又被称为网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者），是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。另外一些不常使用的名字还有蚂蚁、自动索引、模拟程序或者蠕虫。...">\n<title>网络爬虫_百度百科</title>\n<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />\n<link rel="icon" sizes="any" mask href="//www.baidu.com/img/baidu.svg">\n\n<meta name="keywords" content="网络爬虫 爬虫 网页蜘蛛 爬虫程序 蜘蛛程序 搜索引擎蜘蛛 蜘蛛 网络蜘蛛 网络爬虫产生背景 网络爬虫面临的问题 网络爬虫分类 网络爬虫抓取目标分类 网络爬虫网页搜索策略 网络爬虫网页分析算法 网络爬虫补充">\n<meta name="image"
```
可以看到request获得的html里面直接有我们想要的信息，所以这里直接用requests就好了～

### 如何批量爬取
检查一下URL的格式`https://baike.baidu.com/item/网络爬虫`，发现搜索的关键词就在URL的最后一位，猜想一下是不是所有的关键词搜索都是这种模式？`https://baike.baidu.com/item/+关键词`，验证之后发现果然是这样！

所以我们可以通过循环进行爬取
```python
keywordlst = [key1, key2, key3, ...]
for key in keywordlst:
    url = "https://baike.baidu.com/item/" + key 
    scrape(url)
```

### 代码
##### 初始化安装包
```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import bs4
from bs4 import BeautifulSoup
import datetime
from urllib.parse import urljoin
import pandas as pd
import re
from fake_useragent import UserAgent
import numpy as np
from random import uniform
from time import sleep
ua = UserAgent()
```

##### 定义一个重试函数
```python
# 重试函数
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,):
    
    session = session or requests.Session()
    retry = Retry(
        total = retries,
        read = retries,
        connect = retries,
        backoff_factor = backoff_factor,
        status_forcelist = status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
```
定义这个函数是因为在批量request的过程中，很可能会出现`no response`的情况，这个函数可以进行间断多次尝试，从而保证爬取到数据。
详见这篇文章[Best practice with retries with requests](https://www.peterbe.com/plog/best-practice-with-retries-with-requests)

##### request函数
```python
def scrape(keyword):
    headers = {'User-Agent': ua.random}
    url = 'https://baike.baidu.com/item/{0}'.format(keyword)
    try:
        page_response = requests_retry_session().get(url, timeout=5, headers=headers)
        if page_response.status_code == 200:
            content = page_response.content.decode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            return soup
        else:
            print(page_response.status_code)
    except (requests.Timeout, ConnectionError) as e:
        print("It is time to timeout")
        print(str(e))
        return False
```
这个函数对目标URL发送请求，并返回爬取经过`BeautifulSoup`解析过对HTML文件。

Tips：这里解析html用的是lxml引擎`BeautifulSoup(content, 'lxml')`，这个引擎解析速度比较快，在大部分网页中这个引擎没有问题；但是本人在使用时发现解析html过程中有部分页面丢失的情况，百度之后，发现用`html5lib`替代`lxml`可以解决此问题。

##### HTML解析函数
```python
def lemma_summary_parse(soup):
    result = OrderedDict()
    # basic-info
    if soup.find(class_='basic-info cmn-clearfix'):
        basic_info = soup.find(class_='basic-info cmn-clearfix')\
                         .find_all(class_ = re.compile("(basicInfo-item name|basicInfo-item value)"))

        item_name, item_value = None, None
        for content in basic_info:
            if content['class'][1] == 'name':
                item_name = re.sub('[^\u4e00-\u9fa5a-z]','', content.text.strip())
            elif content['class'][1] == 'value':
                item_value = re.sub('[\xa0]',' ', content.text.strip())
                result[item_name] = item_value
    return result
```

##### Putting it together
```python
output = {}
for keyword in keywordlst:
        soup = scrape(keword)
        result = lemma_summary_parse(soup)
        outpu[keyword] = reulst
        sleep(uniform(0,0.5))
```

### 流程总结
![](http://p7ffgka2w.bkt.clouddn.com/mermaid-diagram-20180810082825.svg)

---

### 爬虫的最大困难：反爬虫
爬虫单从逻辑上理解，不存在什么困难，也没有太多技术含量。但在实际操作过程中，会遇到各种困难，比如动态页面加载、反爬虫、分布式等问题。其中最让人头疼的当属反爬虫。

##### 反爬虫是什么？
使用任何技术手段，阻止别人批量获取自己网站信息的一种方式。
具体可以看这篇文章[关于反爬虫，看这一篇就够了](https://segmentfault.com/a/1190000005840672)

### 反爬虫：以CFDA为例
最近项目需要从[食品药品监督管理局](http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=124356560303886909015737447882)上爬取一些药品信息。
![](http://p7ffgka2w.bkt.clouddn.com/18-8-11/32485746.jpg)
分析页面后发现单药品信息通过链接`http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=国产药品&Id=29813`即可得到，其中更换`ID=29813`的数字即可得到不同的药品信息。

随即想到直接Request不同的链接，解析得到的html就能得到所有的药品信息。
OK，直接上代码
```python
url = 'http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%E5%9B%BD%E4%BA%A7%E8%8D%AF%E5%93%81&Id=100'
page_response = requests.get(url, timeout=5)
page_response.status_code
```
结果request返回了`202`，返回的页面也是一堆看不懂的文本
```html
'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n</head>\n<body><meta id="9DhefwqGPrzGxEp9hPaoag" content="Lt{ckL\\kM_k~lk|}klNkntkz&gt;k~xk|bk)}klc&amp;Q-agjjm[\\kkgt[:[[_[lm^fgh?j@socREdC&lt;k,nQTFP.MAHLr3DBaKJ4-]qGIe)2uS=\\Nip+O&gt;1btZ/U`0_vxwy !#$%z{|}~(58:;VXY[s[^`dg[^[ngd^`[^ji^\\o[\\):)3)~&amp;&gt;soZtdvUnXN)+WxzqMwO(Z}B{a|ss`v/n\\yr|z(/t=}?/[(sx-uP~y(x|,||}EnRMr~f~mM,|[rCrfumm`Npxp}bRayUzvOVqatUz){Rpx|Y~@%-}+f&gt;].SufpSunS^]Op0?el-I]5HV/ORKvOHV/]O`I^TrT@]0rDQT.dv]Grv.OV6]V6VAmhwnf&gt;]HHPv5Hcs]e_PFC_OJRVW]EjKcHSvmRD]5@/WCHtRO3OwtlD]Okm3Gp&gt;]Cri4Ori?F.w1]5-KWpsvefpmq]Jk6Iq&gt;]CR/2trjRT^].iVH&gt;S^]pStqELPle6bqppP`&gt;n]5Li]VSOBGSOlm&gt;]THK+HjKM]VhT6]VSSd&gt;iuuflGlfin]t_b2t@PbNsc3JMcgtpikeHm3CsQkqAv45AQUOMW]qHW]N`4wN.44qscbtD]eSKtOHo5Jk/iCHVDR_bDR-v5JHm+Jk/DNVPsNjP?0n]...
```
刚开始的时候以为是网络的问题，后来多次尝试一直都是上面的结果。Google之后才发现，原来遇到了反爬虫！网站反爬虫的方式是**JS混淆加密**！

**JS混淆加密**是网站反爬虫的常用手段。大致过程是这样的：首次请求数据时，服务端返回动态的混淆加密过的JS，而这段JS的作用是给Cookie添加新的内容用于服务端验证。浏览器带上新的Cookie再次请求，服务端验证Cookie通过返回数据(这也是为嘛代码不能返回数据的原因)。

那么如何破解呢？想到既然首次请求数据返回的是混淆加密过的JS，而Cookie隐藏在这段代码中，那么我们的爬虫只要能够解析这段JS代码，便可得到cookie，从而完成第二次请求。具体破解过程参见这篇文章[Python爬虫—破解JS加密的Cookie](https://github.com/jhao104/memory-notes/blob/master/Python/Python%E7%88%AC%E8%99%AB%E2%80%94%E7%A0%B4%E8%A7%A3JS%E5%8A%A0%E5%AF%86%E7%9A%84Cookie.md)。

Request包无法解析JS代码，那么什么样的框架能够解析JS呢？这里[Kenneth Reitz](https://www.kennethreitz.org/)大神给我们开发了另一个包，[Requests-HTML](https://html.python-requests.org/)，这个包集http request和html解析于一身，更重要的是它还有解析javascript的功能，例如：

```python
>>> r = session.get('http://howtopython.org')
>>> r.html.render()
>>> r.html.search('Python 2 will retire in only {months} months!')
<Result () {'months': '<time>22</time>'}>
```

试一试用Requests-HTML解析刚才cfda返回的javascript，
```
from requests_html import HTMLSession
url = 'http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=国产药品&Id=100'
session = HTMLSession()
r = session.get(url)
r.html.render()
r.html.html
```
输出
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html><head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n</head>\n<body><!--[if lt IE 9]><script r=\'m\'>document.createElement("section")</script><![endif]-->\n<input type="hidden" id="__onload__" name="Fp8XVuTkBQC5NKiFQOzye1ptDY682drw_laHCobFerpfWVRFTo4FerY_TV5c6n0EMfqBw_rgFA2f.u1YiRNcwMcTxei5u5gd7NfPvDgR_vZ0UsaPFegUjNXw.2YRd.PFPQxZfzR__iKopOd1a3FbbMTemxmKS0ItUYJsq6PrywYSnXf0DIn9wvZhHqiLTWNO8l4y4XP9oPjI0N9EaoYFJi1BBgzfU6GBFUnRQnPHHE6CMhYu45nZ67knVroV34qip9dtNJNoZPN9UWSURomUlRPA5RfNFINJnnSGlOj.rHG" value="BNci6iLb2KjA85PYCZ636a">\n\n<a href="javascript: void(0);" style="display:none" datas-ts="=X+LsK">admin</a><a href="javascript: void(0);" style="display:none" datas-ts="=DK!Ew">wp-admin</a><a href="javascript: void(0);" style="display:none" datas-ts="=~v|B ">backend</a>\n\n</body></html>
```
可以看到里面返回了一对键值：
```
name="Fp8XVuTkBQC5NKiFQOzye1ptDY682drw_laHCobFerpfWVRFTo4FerY_TV5c6n0EMfqBw_rgFA2f.u1YiRNcwMcTxei5u5gd7NfPvDgR_vZ0UsaPFegUjNXw.2YRd.PFPQxZfzR__iKopOd1a3FbbMTemxmKS0ItUYJsq6PrywYSnXf0DIn9wvZhHqiLTWNO8l4y4XP9oPjI0N9EaoYFJi1BBgzfU6GBFUnRQnPHHE6CMhYu45nZ67knVroV34qip9dtNJNoZPN9UWSURomUlRPA5RfNFINJnnSGlOj.rHG"
value="BNci6iLb2KjA85PYCZ636a"
```
其中value对应的是cookie的名字，name对应着cookie的值。接下来可以将这个cookie加入到request的参数中，
```
page_response = requests.get(url, timeout=5, Cookie={"BNci6iLb2KjA85PYCZ636a":, "Fp8XVuTkBQC5NKiFQOzye1ptDY682drw_laHCobFerpfWVRFTo4FerY_TV5c6n0EMfqBw_rgFA2f.u1YiRNcwMcTxei5u5gd7NfPvDgR_vZ0UsaPFegUjNXw.2YRd.PFPQxZfzR__iKopOd1a3FbbMTemxmKS0ItUYJsq6PrywYSnXf0DIn9wvZhHqiLTWNO8l4y4XP9oPjI0N9EaoYFJi1BBgzfU6GBFUnRQnPHHE6CMhYu45nZ67knVroV34qip9dtNJNoZPN9UWSURomUlRPA5RfNFINJnnSGlOj.rHG"})
```
一切顺利的话，request应该能得到正确的html，然而。。。最终还是返回202，可恶的反爬虫。。。可能是cookie加入的方式不对？折腾了很久还是没有找到反爬虫的方法，看来这条路是走不通了。

##### 使用其他端口获得数据
反复搜索之后发现，原来CFDA竟然还有一个手机端的接口[手机端入口](https://link.zhihu.com/?target=http%3A//mobile.cfda.gov.cn/datasearch/QueryRecord%3FtableId%3D63%26searchF%3DID%26searchK%3D1)，这个端口竟然没有反爬虫！！！直接用request就能得到数据，具体方法跟爬百科一样。


# Scrapy 高级的爬虫方法
[Scrapy](http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html)是一个功能非常强大的爬虫框架，它不仅能便捷地构建request，还有强大的selector能够方便地解析response，然而它最受欢迎的还是它的性能，既抓取和解析的速度，它的downloader是多线程的，request是异步调度和处理的。这两点使它的爬取速度非常之快。另外还有内置的logging，exception，shell等模块，为爬取工作带来了很多便利。所以，scrapy >= Requests + lxml/Beautiful Soup + twisted/tornado + threading + Queue。对于初学者，requests+beautifulsoup是个很好的选择，能让你比较深入理解爬虫的原理，后期实践需要爬取大量的真实数据的时候，scrapy是个让人信服的好框架。知乎上这篇文章比较了request和scrapy的区别，[requests 和 scrapy 在不同的爬虫应用中，各自有什么优势？](https://www.zhihu.com/question/23324984)。

个人认为对于一些简单的爬虫，request就够了，不必上Scrapy。


# 总结

* 爬虫是项体力活
* 爬虫想做高级也很难
* 爬虫最大的困难是应对反爬虫
* 爬虫有很多工具和框架，根据场景选择正确的工具是关键
* 一种思路解决不了问题的时候应该换一种思路
* 有些商用爬虫软件（如[集搜客](http://www.gooseeker.com/)，[八爪鱼](http://www.bazhuayu.com/)）也挺好用，适合不会编程的新手

  [1]: https://piaosanlang.gitbooks.io/spiders/photos/01-webdns.jpg