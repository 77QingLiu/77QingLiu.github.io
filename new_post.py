import datetime
import re
import os

main_template = """
---
layout:   "post"
title:    "{title}"
date:     "{date}"
subtitle: ""
author:       "Qing"
header-img:   //img.77qingliu.com/header/
header-mask:  0.3
catalog:      true
multilingual: true
mathjax: true
tags:
    -
---
<!-- Chinese Version -->
<div class="zh post-container">
    {{% capture about_zh %}}{{% include_relative {title_file}/zh.md %}}{{% endcapture %}}
    {{{{ about_zh | markdownify }}}}
</div>

<!-- English Version -->
<div class="en post-container">
    {{% capture about_en %}}{{% include_relative {title_file}/en.md %}}{{% endcapture %}}
    {{{{ about_en | markdownify }}}}
</div>
"""



def generate_file(title):
    home = '/Users/liuqing/github/77QingLiu.github.io'
    now = datetime.datetime.now()
    year = now.year

    title_file = re.sub('[^0-9a-zA-Z]+', '-', title)
    file_name = now.strftime('%Y-%m-%d') + '-' + title_file
    file_path = home + '/_posts/{year}/'.format(year=year)

    if not os.path.exists(file_path + title_file):
        os.makedirs(file_path + title_file)

    main_file = main_template.format(title=title, date=now.strftime('%Y-%m-%d %H:%M'), title_file=title_file)

    with open(file_path + file_name, 'w') as f:
        f.write(main_file)

    open(file_path + title_file + '/en.md', 'a').close()
    open(file_path + title_file + '/zh.md', 'a').close()

generate_file('aaa')
