## What is Version Control?
Version control is a system that records changes to a file or set of files over time so that you can recall specific versions later.

## Why Version Control?
Version Control allows you:
* Revert selected files back to a previous state
* Revert the entire project back to a previous state,
* Compare changes over time,
* See who last modified something that might be causing a problem, who introduced an issue and when, and more.
* Version Control also generally means that if you screw things up or lose files, you can easily recover.
* In addition, you get all this for very little overhead.

## A Scenario of Chaos without Version Control
Below is a simple screen shot of a set of files(chaos) to backup projects.
![backup1](img/in-post/git-version-control-integration-with-sas-enterprise-guide/backup1.JPG)
![backup2](img/in-post/git-version-control-integration-with-sas-enterprise-guide/backup2.JPG)

## What is Git
Git is an open source distributed version control system for efficient, high-speed processing of project versions from very small to very large. Git is developed by Linus Torvalds to help manage Linux kernel development.

Some characters of Git
* Speed
* Strong support for non-linear development (thousands of parallel branches)
* Fully distributed
* Able to handle large projects like the Linux kernel efficiently (speed and data size)

## Key concepts with Git

![workspace](img/in-post/git-version-control-integration-with-sas-enterprise-guide/workspace.png)

* **Working directory**: Is the current working directory where you develop you code or write documents.

* **Staging area**: The staging area is a file, generally contained in your Git directory, that stores information about what will go into your next commit. Its technical name in Git parlance is the “index”, but the phrase “staging area” works just as well.

* **Git directory**: The Git directory is where Git stores the metadata and object database for your project. This is the most important part of Git, and it is what is copied when you clone a repository from another computer.

## Git working process flow
![process](img/in-post/git-version-control-integration-with-sas-enterprise-guide/workflow.png)
1. Make your repository(`git init`) or clone repository form somewhere else(`git clone path/to/.git`).

2. Modify files in your working tree. can check the status of current working directory(`git status`).

3. Selectively stage just those changes you want to be part of your next commit, which adds only those changes to the staging area(`git add`).

4. Do a commit, which takes the files as they are in the staging area and stores that snapshot permanently to your Git directory(`git commit`).

## GIT Version Control Integration with SAS Enterprise Guide
The Git working under command line interface(CLI) makes it hard to get start for beginners, though the core concept of Git behind command is very important.
However, For those who don't wnat to touch command line interface(CLI), SAS Enterprise Guide 7.1 is the SAVE!
A major new feature in SAS Enterprise Guide version 7.1 is the capability to retain historical versions of the SAS code by integrating Git.
![eg_git](img/in-post/git-version-control-integration-with-sas-enterprise-guide/eg_git1.png)

#### Commit changes - equal to `git add + git commit`
![commit](img/in-post/git-version-control-integration-with-sas-enterprise-guide/commit.JPG)

#### Tracking changes - equal to `git diff`
![diff](img/in-post/git-version-control-integration-with-sas-enterprise-guide/diff.png)

#### View commit history - equal to `git log`
![log](img/in-post/git-version-control-integration-with-sas-enterprise-guide/log.png)

If you open a Externally Referenced SAS Program(not embeded in EG), the first time you commit would result in the following window.

![window](img/in-post/git-version-control-integration-with-sas-enterprise-guide/window.png)
This is that your program is not in a Git repository. you can init Git repository by submitting `git init` in your current working directory or parent directory.

#### Recommend Reading
* [Pro Git](https://bingohuang.gitbooks.io/progit2/content/01-introduction/1-introduction.html)
* [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
