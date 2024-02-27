#!/usr/bin/env python3
# -- coding: utf-8 --

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random
import matplotlib.pyplot as plt
import streamlit as st

import os

script_directory = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_directory)


def linkedInScraper(scraping_option):
    if scraping_option == 'Boston Software Engineer':
        url = 'https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Boston%2C%20Massachusetts%2C%20United%20States&geoId=102380872&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    elif scraping_option == 'Boston Data Scientist':
        url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Boston&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    elif scraping_option == 'Chicago Software Engineer':
        url = 'https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Chicago%2C%20Illinois%2C%20United%20States&geoId=103112676&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    elif scraping_option == 'Chicago Data Scientist':
        url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Chicago%2C%20Illinois%2C%20United%20States&geoId=103112676&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    elif scraping_option == 'San Francisco Software Engineer':
        url = 'https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    elif scraping_option == 'San Francisco Data Scientist':
        url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    elif scraping_option == 'SDE San Francisco':
        url = 'https://www.linkedin.com/jobs/search/?currentJobId=3818332011&keywords=sde%20san%20francisco&origin=SWITCH_SEARCH_VERTICAL'
    else:
        url = 'https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Boston%2C%20Massachusetts%2C%20United%20States&geoId=102380872&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

    driver = webdriver.Chrome()
    driver.get(url)

    no_of_jobs = (driver.find_element(By.CSS_SELECTOR, 'h1>span').get_attribute('innerText'))

    no_of_jobs = no_of_jobs.replace('+', '')
    no_of_jobs = int(no_of_jobs.replace(',', ''))

    st.write("Starting Scraping for " + scraping_option)

    print('Starting Scraping')

    i = 2
    while i <= 10:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i = i + 1
        try:
            x = driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
            driver.execute_script("arguments[0].click();", x)
            time.sleep(5)
        except:
            pass
            time.sleep(5)

    job_lists = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    jobs = job_lists.find_elements(By.TAG_NAME, 'li')  # return a list

    job_id = []
    job_title = []
    company_name = []
    location = []
    date = []
    job_link = []
    i = 0
    for job in jobs:
        i = i + 1
        job_id.append(i)

        job_title0 = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
        job_title.append(job_title0)

        company_name0 = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
        company_name.append(company_name0)

        location0 = job.find_element(By.CSS_SELECTOR, '[class="job-search-card__location"]').get_attribute('innerText')
        location.append(location0)

        date0 = job.find_element(By.CSS_SELECTOR, 'div>div>time').get_attribute('datetime')
        date.append(date0)

        job_link0 = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        job_link.append(job_link0)

    if scraping_option == 'Boston Software Engineer':
        filename = '../LinkedIn_Software_Engineer_Boston.csv'
    elif scraping_option == 'Boston Data Scientist':
        filename = 'LinkedIn_Data_Scientist_Boston.csv'
    elif scraping_option == 'Chicago Software Engineer':
        filename = 'LinkedIn_Software_Engineer_Chicago.csv'
    elif scraping_option == 'Chicago Data Scientist':
        filename = 'LinkedIn_Data_Scientist_Chicago.csv'
    elif scraping_option == 'San Francisco Software Engineer':
        filename = 'LinkedIn_Software_Engineer_San_Francisco.csv'
    elif scraping_option == 'San Francisco Data Scientist':
        filename = 'LinkedIn_Data_Scientist_San_Francisco.csv'
    elif scraping_option == 'SDE San Francisco':
        filename = 'LinkedIn_San_Francisco_SDE.csv'
    else:
        filename = '../LinkedIn_Software_Engineer_Boston.csv'

    job_data = pd.DataFrame({'ID': job_id,
                             'Date': date,
                             'Company': company_name,
                             'Title': job_title,
                             'Location': location,
                             'Link': job_link
                             })
    current_directory = os.getcwd()
    print("Current directory:", current_directory)
    job_data.to_csv(current_directory+"/"+filename, index=False)

    st.write("Scraping done, Data stored in CSV File")
    print('Scraping done, Data stored in CSV File')


if st.button("Boston Software Engineer"):
    linkedInScraper('Boston Software Engineer')

if st.button("Boston Data Scientist"):
    linkedInScraper('Boston Data Scientist')

if st.button("Chicago Software Engineer"):
    linkedInScraper('Chicago Software Engineer')

if st.button("Chicago Data Scientist"):
    linkedInScraper('Chicago Data Scientist')

if st.button("San Francisco Software Engineer"):
    linkedInScraper('San Francisco Software Engineer')

if st.button("San Francisco Data Scientist"):
    linkedInScraper('San Francisco Data Scientist')

if st.button("SDE San Francisco"):
    linkedInScraper('SDE San Francisco')