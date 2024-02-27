import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import matplotlib.pyplot as plt

# Function to scrape LinkedIn job data

def linkedInScraper(scraping_option, max_jobs):
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


            job_data.append({'Title': job_title, 'Company': company_name, 'Location': location, 'Date': date, 'Link': job_link})

        # Save data to CSV
        filename = f'LinkedIn_{scraping_option.replace(" ", "_")}.csv'
        job_df = pd.DataFrame(job_data)
        job_df.to_csv(filename, index=False)

        st.success(f"Scraping done for {scraping_option}, Data stored in CSV File: {filename}")
    else:
        st.error('Invalid scraping option')



def plotGraph(filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Count the occurrences of each location
    location_counts = df['Location'].value_counts()

    # Plot the locations
    plt.figure(figsize=(12, 6))
    location_counts.plot(kind='bar', color='skyblue')
    plt.title('Job Postings by Location')
    plt.xlabel('Location')
    plt.ylabel('Number of Job Postings')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Display the plot in Streamlit
    st.pyplot(plt)


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
    linkedInScraper(scraping_option, max_jobs=10)

filename = f'LinkedIn_{scraping_option.replace(" ", "_")}.csv'
plotGraph(filename)