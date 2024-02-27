#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

col1,col2, col3 = st.columns(3)

col5,col6, col7 = st.columns(3)

role_list = ['Software Engineer', 'Data Scientist']
industry_list = ['Technology', 'Retail', 'FinTech', 'Recruiting', 'Medical']
location_list = ['Boston', 'Chicago', 'San Francisco']

with col1:
    input_city = st.multiselect('Select the Location:',['Select All'] + location_list, default = ['Select All'])
with col2:
    role = st.multiselect('Enter the Role',['Select All'] + role_list, default = ['Select All'])
with col5: 
    industry = st.multiselect('Enter the Industry', ['Select All'] + industry_list, default = ['Select All'])
with col6: 
    salary = st.text_input('Enter the minimum salary', 0)

if "Select All" in input_city:
    input_city = location_list

if "Select All" in industry:
    industry = industry_list

if "Select All" in role:
    role = role_list
    

data_science_boston = pd.read_csv('LinkedIn_Data_Scientist_Boston.csv')
data_science_chicago = pd.read_csv('LinkedIn_Data_Scientist_Chicago.csv')
data_science_sf = pd.read_csv('LinkedIn_Data_Scientist_San_Francisco.csv')
software_engineer_boston = pd.read_csv('../LinkedIn_Software_Engineer_Boston.csv')
software_engineer_chicago = pd.read_csv('LinkedIn_Software_Engineer_Chicago.csv')
software_engineer_sf = pd.read_csv('LinkedIn_Software_Engineer_San_Francisco.csv')

data_science_boston['Job_Role'] = 'Data Scientist'
data_science_chicago['Job_Role'] = 'Data Scientist'
data_science_sf['Job_Role'] = 'Data Scientist'
software_engineer_boston['Job_Role'] = 'Software Engineer'
software_engineer_chicago['Job_Role'] = 'Software Engineer'
software_engineer_sf['Job_Role'] = 'Software Engineer'
data_science_boston['City'] = 'Boston'
data_science_chicago['City'] = 'Chicago'
data_science_sf['City'] = 'San Francisco'
software_engineer_boston['City'] = 'Boston'
software_engineer_chicago['City'] = 'Chicago'
software_engineer_sf['City'] = 'San Francisco'

boston_data_science_salary = [80000,85000,100000,120000,160000,200000,220000,250000,300000]
chicago_data_science_salary = [60000,90000,130000,145000,170000,200000, 250000]
sf_data_science_salary = [75000,90000,95000,130000,155000,180000,220000, 280000,330000]
boston_software_engineer_salary = [100000,125000,165000,210000,240000, 280000]
chicago_software_engineer_salary = [120000,150000,170000,220000, 280000,300000]
sf_software_engineer_salary = [130000,170000,190000,220000, 250000,290000,310000,340000]

data_science_boston['Salary'] = [random.choice(boston_data_science_salary) for _ in range(len(data_science_boston))]
data_science_chicago['Salary'] = [random.choice(chicago_data_science_salary) for _ in range(len(data_science_chicago))]
data_science_sf['Salary'] = [random.choice(sf_data_science_salary) for _ in range(len(data_science_sf))]
software_engineer_boston['Salary'] = [random.choice(boston_software_engineer_salary) for _ in range(len(software_engineer_boston))]
software_engineer_chicago['Salary'] = [random.choice(chicago_software_engineer_salary) for _ in range(len(software_engineer_chicago))]
software_engineer_sf['Salary'] = [random.choice(sf_software_engineer_salary) for _ in range(len(software_engineer_sf))]

jobs_data = pd.concat([data_science_boston, data_science_chicago, data_science_sf, software_engineer_boston, software_engineer_chicago, software_engineer_sf], ignore_index=True)


jobs_data_industries = ['Technology', 'Retail', 'FinTech', 'Recruiting', 'Medical']
jobs_data['Industries'] = [random.choice(jobs_data_industries) for _ in range(len(jobs_data))]

jobs_data = jobs_data[(jobs_data['Salary'] >= float(salary))
                      & (jobs_data['City'].isin(input_city)) 
                      & (jobs_data['Industries'].isin(industry))
                      & (jobs_data['Job_Role']).isin(role)]


salary_ranges = [0,50000,100000,150000,200000,250000,300000]
fig, ax = plt.subplots()
n, bins, patches = ax.hist(jobs_data['Salary'], bins=salary_ranges, color='lightblue', edgecolor='black', alpha=0.75)

counts = [int(count) for count in n]

# Annotate each bar with its count
for count, x, patch in zip(counts, bins, patches):
    ax.text(x + (bins[1] - bins[0]) / 2, count, str(count), ha='center', va='bottom')


ax.set_xlabel('Salary')
ax.set_ylabel('Count')
ax.set_title('Company Salary Distribution')

st.pyplot(fig)

grouped = jobs_data['Industries'].value_counts()

fig, ax = plt.subplots()
ax.pie(grouped, labels=None, autopct='', startangle=90, colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'green'])
ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

legend_labels = [f'{label} ({percentage:.1f}%)' for label, percentage in zip(grouped.index, grouped / grouped.sum() * 100)]
plt.legend(legend_labels, title='Distribution of Job Industries', loc='upper left', bbox_to_anchor=(1, 1))

plt.title('Distribution of Company Indusries')

st.pyplot(fig)

average_salaries = jobs_data[['Job_Role', 'City', 'Industries', 'Salary']]
grouped_avg_salaries = average_salaries.groupby(['City','Job_Role', 'Industries'])['Salary'].mean().reset_index()
grouped_avg_salaries = grouped_avg_salaries.sort_values(by=['Salary'], ascending = [False])
st.markdown("<h3 style='text-align: center;'>Grouped Data by City, Role and Industries on Salary</h3>", unsafe_allow_html=True)
st.table(grouped_avg_salaries)

columns_for_table = ['Company','Link','Location','Title', 'Salary', 'Industries']
jobs_data_table = jobs_data[columns_for_table]

jobs_data_table = jobs_data_table.sort_values(by=['Salary'], ascending = [False])

st.markdown("<h3 style='text-align: center;'>Top 10 Companies with Highest Salaries</h3>", unsafe_allow_html=True)
st.table(jobs_data_table.head(10))








