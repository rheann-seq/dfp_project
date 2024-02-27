import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

# Function to scrape LinkedIn job data
def linkedInScraper(scraping_option, max_jobs=10):
    # URL based on scraping option
    urls = {
        'Boston Software Engineer': 'https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Boston%2C%20Massachusetts%2C%20United%20States&geoId=102380872&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
        'Boston Data Scientist': 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Boston&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
        'Chicago Software Engineer': 'https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Chicago%2C%20Illinois%2C%20United%20States&geoId=103112676&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
        'Chicago Data Scientist': 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Chicago%2C%20Illinois%2C%20United%20States&geoId=103112676&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
        'San Francisco Software Engineer': 'https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
        'San Francisco Data Scientist': 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
        'SDE San Francisco': 'https://www.linkedin.com/jobs/search/?currentJobId=3818332011&keywords=sde%20san%20francisco&origin=SWITCH_SEARCH_VERTICAL'
    }
    url = urls.get(scraping_option, '')

    if url:
        driver = webdriver.Chrome()
        driver.get(url)

        # Scroll to load more jobs
        while len(driver.find_elements(By.CSS_SELECTOR, 'li')) < max_jobs:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Extract job details
        job_lists = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
        jobs = job_lists.find_elements(By.TAG_NAME, 'li')

        job_data = []
        for job in jobs[:max_jobs]:
            job_title = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
            company_name = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
            location = job.find_element(By.CSS_SELECTOR, '[class="job-search-card__location"]').get_attribute('innerText')
            date = job.find_element(By.CSS_SELECTOR, 'div>div>time').get_attribute('datetime')
            job_link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            salary = job.find_element(By.CSS_SELECTOR, '[class="job-search-card__salary-info"]').get_attribute('innerText')
            print("salary for:"+company_name+" is: "+salary)
            #added skills
            # job_skills = ""
            # try:
            #     job_skills =  job.find_element(By.CSS_SELECTOR, 'button[aria-label="View strong skill match modal"]').text
            #     print("skills:",job_skills)
            # except:
            #     print("Couldn't find skills")

            skills = []
            example_skills = ['Java', 'Cloud', 'SQL', 'Node']
            print("job element:", job)
            salary_elements = job.find_elements(By.XPATH, "//*[contains(text(), '$')]")
            print("size of salary_els", len(salary_elements))
            for i in salary_elements:
                if '$' in i.text:
                    print("salary element is:"+ i.text)
            # if salary_elements:
            #     print("The page contains the word 'Java'")
            #     print(salary_elements[0].text)
            #     salary_element = salary_elements[0]

                # Find the next sibling element
                # next_sibling_element = salary_element.find_element(By.XPATH, "following-sibling::*")
                # print(next_sibling_element.text)
                # third_sibling_element = next_sibling_element.find_element(By.XPATH, "following-sibling::*")
                # print("third:"+third_sibling_element.text)

            job_data.append({'Title': job_title, 'Company': company_name, 'Location': location, 'Date': date, 'Link': job_link, 'Skills': ""})

            # salary_el = job.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/ul/li[1]	')
            # print("found salary:::"+salary_el.text)
        # Save data to CSV
        filename = f'LinkedIn_{scraping_option.replace(" ", "_")}.csv'
        job_df = pd.DataFrame(job_data)
        job_df.to_csv(filename, index=False)

        st.success(f"Scraping done for {scraping_option}, Data stored in CSV File: {filename}")
    else:
        st.error('Invalid scraping option')

# Streamlit UI
st.title('LinkedIn Job Scraper')
scraping_option = st.selectbox('Select an option:', [
    'Boston Software Engineer',
    'Boston Data Scientist',
    'Chicago Software Engineer',
    'Chicago Data Scientist',
    'San Francisco Software Engineer',
    'San Francisco Data Scientist',
    'SDE San Francisco'
])

if st.button('Scrape Jobs'):
    linkedInScraper(scraping_option, max_jobs=50)