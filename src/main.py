# -*- coding: utf-8 -*-
import os
try:
    os.chdir('src')
except:
    pass
from scrape import linkedinJob

if __name__ == "__main__":
    homePath           = r'C:\Users\chase\Documents\GitHub\job\job_scraper'
    driver             = "Chrome"
    email              = "chaseliu1992@outlook.com"
    password           = "qingqing1992"
    job_keyword        = "SAS Programmer"
    location           = "China"
    sleep_sec_interval = 10
    job_scrape         = linkedinJob(homePath, driver, email, password, job_keyword, location, sleep_sec_interval)
    job_scrape.logIn()
    job_scrape.navigate2Job()
    job_scrape.customSearch()
    job_scrape.scroll()
    job_scrape.job_list.toJSON()
    job_scrape.job_list.toMarkdown()
