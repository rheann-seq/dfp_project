import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import os

# Function to load data
def load_data():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)

    data_science_boston = pd.read_csv('LinkedIn_Data_Scientist_Boston.csv')
    data_science_chicago = pd.read_csv('LinkedIn_Data_Scientist_Chicago.csv')
    data_science_sf = pd.read_csv('LinkedIn_Data_Scientist_San_Francisco.csv')
    software_engineer_boston = pd.read_csv('LinkedIn_Software_Engineer_Boston.csv')
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

    return jobs_data

# Load data
jobs_data = load_data()

# Sidebar UI
st.sidebar.title('Filters')
input_city = st.sidebar.multiselect('Select the Location:', jobs_data['City'].unique(), default=jobs_data['City'].unique())
role = st.sidebar.multiselect('Enter the Role', jobs_data['Job_Role'].unique(), default=jobs_data['Job_Role'].unique())
industry = st.sidebar.multiselect('Enter the Industry', jobs_data['Industries'].unique(), default=jobs_data['Industries'].unique())
salary = st.sidebar.text_input('Enter the minimum salary', '0')

# Apply filters
filtered_data = jobs_data[(jobs_data['Salary'] >= float(salary))
                           & (jobs_data['City'].isin(input_city))
                           & (jobs_data['Industries'].isin(industry))
                           & (jobs_data['Job_Role'].isin(role))]

# Main content UI
st.title('LinkedIn Job Data Analysis')

# Show filtered data table
st.subheader('Filtered Job Data')
st.write(filtered_data)

# Visualizations
st.subheader('Salary Distribution')
fig, ax = plt.subplots()
n, bins, patches = ax.hist(filtered_data['Salary'], bins=10, color='lightblue', edgecolor='black', alpha=0.75)

# Annotate each bar with its count
for count, x, patch in zip(n, bins, patches):
    ax.text(x + (bins[1] - bins[0]) / 2, count, str(count), ha='center', va='bottom')

ax.set_xlabel('Salary')
ax.set_ylabel('Count')
ax.set_title('Company Salary Distribution')
st.pyplot(fig)

st.subheader('Industry Distribution')
industry_counts = filtered_data['Industries'].value_counts()
fig, ax = plt.subplots()
ax.pie(industry_counts, labels=industry_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

st.subheader('Skills Distribution')
# Assume there's a column called 'Skills' in the jobs_data DataFrame
skills_data = pd.Series(['Python', 'Java', 'SQL', 'Python', 'R', 'Python', 'Java', 'Python', 'SQL'])
skills_counts = skills_data.value_counts()
fig, ax = plt.subplots()
skills_counts.plot(kind='bar', ax=ax)
ax.set_xlabel('Skills')
ax.set_ylabel('Count')
ax.set_title('Skills Distribution')
st.pyplot(fig)
