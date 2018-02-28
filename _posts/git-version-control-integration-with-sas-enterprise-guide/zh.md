## 什么是版本控制？
版本控制是一个系统，记录随着时间​​的推移对文件或文件集的更改，以便稍后可以调用特定版本。

## 为什么需要版本控制？
**版本控制允许你：**
* 将选定的文件恢复到以前的状态。
* 将整个项目恢复到之前的状态。
* 比较随着时间文件发生的变化。
* 查看谁最后修改了可能导致问题的内容，谁导致了问题以及何时等等。
* 版本控制通常也意味着如果你搞砸了或丢失了文件，你可以轻松恢复。
* 另外，执行这些操作仅需要花费很少的开销。

**没有版本控制的混沌场景**

例如你可能会用下面的方式备份项目。
![backup1](img/in-post/git-version-control-integration-with-sas-enterprise-guide/backup1.JPG)
![backup2](img/in-post/git-version-control-integration-with-sas-enterprise-guide/backup2.JPG)

## 什么是Git
Git是一个开源的分布式版本控制系统，用于对从非常小到非常大的项目进行高效，高速的版本控制。 Git由Linus Torvalds开发，最开始用于帮助管理Linux内核开发。

Git的一些特点
* 速度
* 强力支持非线性开发(数千个并行分支)
* 完全分布式
* 能够高效地处理Linux内核等大型项目

## Git的关键概念

![workspace](img/in-post/git-version-control-integration-with-sas-enterprise-guide/workspace.png)

*  **工作目录**：是你开发代码或写入文档的当前工作目录。

*  **临时区域**：临时区域是一个文件，通常包含在你的Git目录中，用于存储将进入下一个提交的内容信息。在Git中它的技术名称是“索引”，但有时也被称作“暂存区”。

*  **Git目录**：Git目录是Git存储项目元数据和对象数据库的地方。这是Git最重要的部分，它是从另一台计算机克隆存储库时复制的内容。

## Git工作流程
![process](img/in-post/git-version-control-integration-with-sas-enterprise-guide/workflow.png)

1.首先，初始化仓库(`git init`d)或克隆放在其他地方的仓库(`git clone path/to/.git`d)。

2.修改工作树中的文件。你可以通过(`git status`)检查当前工作目录的状态。

3.有选择性地改变的一部分的文件，通过(`git add`)提交那些改变到暂存区域。

4.通过(`git commit`)提交一次，它会将文件保存在暂存区域中，并将该快照永久存储到你的Git目录。

尽管Git命令背后的核心概念非常重要，但是在命令行界面(CLI)下，初学者很难入门。
因此，对于那些不想触摸命令行界面(CLI)的用户，可以通过一系列GUI工具(比如[GitHub桌面客户端](https://desktop.github.com/))入门。

## GIT版本控制与SAS企业版集成
好消息！
从SAS Enterprise Guide 7.1开始，能够在SAS中集成Git，从而实现保留SAS代码的历史版本。SAS已将其做成了功能按键，用户只需简单点击按键，及可实现SAS的版本控制！
![eg_git](img/in-post/git-version-control-integration-with-sas-enterprise-guide/eg_git1.png)

#### 提交更改 - 等同于`git add + git commit`
![commit](img/in-post/git-version-control-integration-with-sas-enterprise-guide/commit.JPG)

#### 跟踪更改 - 等同于`git diff`
![diff](img/in-post/git-version-control-integration-with-sas-enterprise-guide/diff.png)

#### 查看提交历史记录 - 等同于`git log`
![log](img/in-post/git-version-control-integration-with-sas-enterprise-guide/log.png)

> 我还需要安装Git吗？
SAS Enterprise Guide 7.1仅仅是将外部的Git命令做成了内部的功能按键，因此，**你需要在电脑上安装Git**

> 我打开程序后，你第一次提交出现了以下窗口。
![window](img/in-post/git-version-control-integration-with-sas-enterprise-guide/window.png)
这是因为你的程序不在Git仓库下，需要通过在当前工作目录或父目录中提交`git init`来初始化Git存储库。


## 推荐阅读
* [Pro Git](https://bingohuang.gitbooks.io/progit2/content/01-introduction/1-introduction.html)
* [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
