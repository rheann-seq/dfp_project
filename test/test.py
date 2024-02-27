import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('LinkedIn_Data_Scientist_Boston.csv')

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
