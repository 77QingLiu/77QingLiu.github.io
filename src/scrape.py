# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import bs4
from bs4 import BeautifulSoup

from time import sleep
import chromedriver_binary
import datetime
from urllib.parse import urljoin

from jobs import job
from jobs import jobs


class linkedinJob():
    def __init__(self, homePath, driver, email, password, job_keyword, location, sleep_sec_interval):
        if driver.upper() == 'CHROME':
            self.driver = webdriver.Chrome()
        else:
            raise "Only CHROME is supported now"

        self.homePath           = homePath
        self.email              = email
        self.password           = password
        self.job_keyword        = job_keyword
        self.location           = location
        self.sleep_sec_interval = sleep_sec_interval
        self.wait               = WebDriverWait(self.driver, self.sleep_sec_interval)
        self.id                 = 0
        self.job_list           = jobs(self.homePath, self.job_keyword, self.location)



    # Log in
    def logIn(self):
        """ Login to the website"""
        self.driver.get("https://www.linkedin.com/uas/login")

        # fill in username
        email_elem = self.wait.until(EC.presence_of_element_located((By.ID, 'session_key-login')))
        email_elem.clear()
        email_elem.send_keys(self.email)

        # fill in password
        pass_elem = self.wait.until(EC.presence_of_element_located((By.ID, 'session_password-login')))
        pass_elem.clear()
        pass_elem.send_keys(self.password)

        # sign in button
        self.driver.find_element_by_id("btn-primary").click()

    def driverQuit(self):
        """ Quit driver """
        self.driver.quit()

    def navigate2Job(self):
        """ navigate to job finding panel, enter search keyword and location """
        sleep(self.sleep_sec_interval)
        jobPanel = self.wait.until(EC.presence_of_element_located((By.ID, 'jobs-tab-icon')))
        jobPanel.click()

        # fill in search keyword
        keyword_search = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search jobs"]')))
        keyword_search.send_keys(self.job_keyword)

        # fill in location
        location_search = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search location"]')))
        location_search.clear()
        location_search.send_keys(self.location)

        # search
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="jobs-search-box__submit-button button-secondary-large-inverse"]'))).click()


    def customSearch(self, filterByDate='Any Time', sortBy='relevance'):
        """custom search results by either filter date posted or sort criteria"""
        # custom filter criteria by date
        keylist = {'Past 24 hours':0, 'Past Week':1, 'Past Month':2, 'Any Time':3}
        if filterByDate not in keylist.keys():
            print("filterByDate not in ('Past 24 hours' 'Past Week' 'Past Month')\nusing default filter: Any Time")
        else:
            num = keylist[filterByDate]
            if num == 3:
                pass
            else:
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="search-s-facet__name-wrap search-s-facet__name-wrap--pill button-secondary-medium-muted"]'))).click()
                self.driver.find_elements_by_css_selector('li[class="search-s-facet-value"]')[num].click()
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="button-primary-medium facet-collection-list__apply-button"]'))).click()

        # custom sort criteria
        if sortBy == "relevance":
            pass
        elif sortBy == 'post date':
            self.driver.find_element_by_css_selector('p[class*="jobs-search-dropdown__label"]').click()
            self.driver.find_element_by_css_selector('button[class="jobs-search-dropdown__option-button jobs-search-dropdown__option-button--date "]').click()
        else:
            print("sortBy not in ('relevance' 'post date')\nusing default sort: relevance")
        sleep(5)

    def scroll(self):
        """
            scroll every job finding page to get all job search result
            results are stored in jobs object
        """

        remain = True
        self.screened = ['1']

        while remain == True:
            remain = False

            # parse current job
            self.scrape()

            # parse jobs in whole page
            buttonList = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="occludable-update card-list__item jobs-search-two-pane__search-result-item ember-view"]/following-sibling::li')))
            print(len(buttonList))
            n = 1
            for button in buttonList:
                n+=1
                print(n)
                button.click()
                sleep(2)
                self.scrape()

            # to next page
            # page = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="page-list"]/ol/li/button')))
            # for i in range(len(page)):
            #     if page[i].text not in self.screened:
            #         remain = True
            #         self.screened.append(page[i].text)
            #         page[i].send_keys("\n")
            #         break

    def scrape(self):
        """ scrape job information from the current page """
        try:
            view_more = self.driver.find_element_by_css_selector('button[class*="view-more-icon"]').text.split('\n')[1]
            while view_more != 'View less':
                self.driver.find_element_by_css_selector('button[class="view-more-icon"]').click()
                view_more = self.driver.find_element_by_css_selector('button[class*="view-more-icon"]').text.split('\n')[1]
        except NoSuchElementException:
            return

        sleep(2)
        content                    = self.driver.page_source
        soup                       = BeautifulSoup(content, 'lxml')
        parseTopCard               = self.parseTopCard(soup)
        parseJobDetails            = self.parseJobDetails(soup)
        parseJobDescriptionDetails = self.parseJobDescriptionDetails(soup)

        self.id += 1
        key = "Linkedin-{date}[{id:03d}]".format(date=datetime.date.today().strftime("%Y-%m-%d"), id=self.id)
        JOB = job(parseTopCard['Job Title'], parseTopCard['url'], parseTopCard['Company Name'], parseTopCard['Company Location'], parseTopCard['Post Date'],
                  parseJobDescriptionDetails['Seniority Level'], parseJobDescriptionDetails['Industry'], parseJobDescriptionDetails['Employment Type'], parseJobDescriptionDetails['Job Functions'],
                  parseJobDetails[0], parseJobDetails[1], parseJobDetails[2])
        self.job_list.addJob(key, JOB)
        sleep(4)


    def parseTopCard(self, soup):
        job_top_card            = soup.find(class_='jobs-details-top-card__content-container mt6 pb5')
        out                     = {}
        out['url']              = urljoin('https://www.linkedin.com', job_top_card.find(class_='jobs-details-top-card__job-title-link').get('href', ''))
        out['Job Title']        = job_top_card.find(class_='jobs-details-top-card__job-title').text.strip()
        out['Company Name']     = job_top_card.find(class_='jobs-details-top-card__company-info').text.split('\n')[2].strip()
        out['Company Location'] = job_top_card.find(class_='jobs-details-top-card__bullet').contents[-1].string.strip()
        dateitem                = job_top_card.find(class_='jobs-details-top-card__job-info').text.split('\n')

        date = [item for item in dateitem if item][2].strip()
        if date.find('hours'):
            out['Post Date'] = datetime.date.today().strftime("%Y-%m-%d")
        else:
            daten = [int(s) for s in date.split() if s.isdigit()][0]
            out['Post Date'] = (datetime.date.today() + datetime.timedelta(days=daten)).strftime("%Y-%m-%d")
        return out

    def parseJobDetails(self, soup):
        keyWordList = ['']
        job_details          = soup.find(id='job-details')
        job_details_text     = list(job_details.stripped_strings)
        job_details_html     = job_details.prettify()
        sibling              = job_details.find(class_='jobs-description-content__title jobs-box__title')
        out                  = {'Job Description':[]}
        keyword              = 'Job Description'
        while sibling:
            if type(sibling) == bs4.element.Comment:
                pass
            elif type(sibling) == bs4.element.NavigableString:
                string = sibling.string.strip()
                if string and string.upper() != "JOB DESCRIPTION":
                    for str_ in string.split('\n'):
                        out[keyword].append(str_.strip())
            else:
                text = sibling.text.strip()
                if text:
                    if sibling.find('strong') or sibling.name == 'strong':
                        keyword = text
                        out[keyword] = []
                    elif text.upper() == "JOB DESCRIPTION":
                        pass
                    elif sibling.find('li'):
                        for content in sibling.contents:
                            if type(content) == bs4.element.NavigableString:
                                if content.string.strip():
                                    out[keyword].append(content.string.strip())
                            elif type(content) == bs4.element.Tag:
                                out[keyword].append(content.text.strip())
                    else:
                        for str_ in text.split('\n'):
                            out[keyword].append(str_.strip())
            sibling = sibling.next_sibling
        return (out, job_details_text, job_details_html)

    def parseJobDescriptionDetails(self, soup):
        jobs_description_details          = soup.find(class_="jobs-description-details pt5 ember-view")
        sibling                           = jobs_description_details.find(class_='jobs-box__sub-title js-formatted-exp-title')
        out                               = {'Seniority Level':[]}
        lookList                          = ['Seniority Level', 'Industry', 'Employment Type', 'Job Functions']
        keyword                           = 'Seniority Level'

        while sibling:
            if type(sibling) == bs4.element.Comment or type(sibling) == bs4.element.NavigableString:
                pass
            elif sibling.text.strip() in ['Seniority Level', 'Industry', 'Employment Type', 'Job Functions']:
                keyword = sibling.text.strip()
                out[keyword] = ''
            else:
                out[keyword] = sibling.text.strip().split('\n')
            sibling = sibling.next_sibling
        return out
