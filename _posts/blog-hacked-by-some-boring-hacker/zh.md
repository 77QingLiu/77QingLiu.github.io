It's been a while since I last blogged. Many things happened in this time and it's difficult for me to write just a single word.

而就在最近，当我打开博客的时候，发现一片漆黑，原来的博客不见了，只剩下下面漆黑一片，再加上印尼猴子留下的几个字。
![](http://77qingliu-blog.oss-cn-shanghai.aliyuncs.com/hacked.png)
很明显，我的博客被黑客攻击了，也不知道是哪个无聊的人干的破事，之前从没遇到过这种情况，对此我是很头大。

由于我的博客是托管在GitHub上面，并通过阿里云上购买的域名定制custom domain，因此，黑客攻击的方式很可能是两个地方：

* Github 个人仓库（篡改服务器数据）
* 阿里云域名解析（DNS劫持，转向黑客网站）

这里我首先下意识的排除了GitHub个人仓库被黑的可能性（GitHub还是比较安全的），至于阿里云方面，我首先通过dig命令检查了网站的域名解析
![](http://77qingliu-blog.oss-cn-shanghai.aliyuncs.com/hacke_commad1.png)，并没有发现问题，域名解析是正确的，为此我不太确信还在阿里云上面提交了工单，阿里云的工程师也没有检测出问题。

好吧，那应该不是阿里云域名解析的问题。

那么难道GitHub的服务器被攻击了？很奇怪的是我访问77qingliu.github.io这个GitHub pages的原始地址是没错的，只有访问77qingliu.com才会转到黑客网站，黑客究竟采用什么样的方法将链接重定向的呢？

突然想到我的个人域名77qingliu.com是通过repository里面的CNAME指定，然后在Custom domain指定个人域名实现的，难道是这里出了问题？
![](http://77qingliu-blog.oss-cn-shanghai.aliyuncs.com/hack_github1.png)

果然，当我检查Custom domain设置时，GitHub提示我`CNAME has already been taken in another repository`，奇怪的是我从没有在其他repository使用过77qingliu.com这个域名，而且这个仓库的CNAME一直没有变过，它怎么会被其他repository占用呢？

很可能是黑客入侵了我的账号，修改过我的CNAME。后来我给GitHub support写了一封邮件，通过证明域名所有人的身份，将77qingliu.com 重新绑定到77qingliu.github.io上，至此问题解决！

好吧，有惊无险问题得到解决，总结这次被黑事件，很可能是因为自己GitHub账号密码泄漏引起的，一是自己的密码有将近一年的时间没有修改了，二是之前在一些网站上用GitHub账号注册过。

现在看来，注意网络安全，定期修改密码还是蛮重要的！