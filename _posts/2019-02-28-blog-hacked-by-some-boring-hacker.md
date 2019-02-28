---
layout:   "post"
title:    "My blog gets hacked"
date:     "2019-02-28 19:33"
subtitle: ""
author:       "Qing"
header-img:   //img.77qingliu.com/being_hacked.jpg
header-mask:  0.3
catalog:      true
multilingual: true
mathjax: true
tags:
    - life
---
<!-- Chinese Version -->
<div class="zh post-container">
    {% capture about_zh %}{% include_relative blog-hacked-by-some-boring-hacker/zh.md %}{% endcapture %}
    {{ about_zh | markdownify }}
</div>

<!-- English Version -->
<div class="en post-container">
    {% capture about_en %}{% include_relative blog-hacked-by-some-boring-hacker/en.md %}{% endcapture %}
    {{ about_en | markdownify }}
</div>
