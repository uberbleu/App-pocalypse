# Libraries and Data

from google.colab import drive
drive.mount('/content/drive')

%cd /content/drive/MyDrive/Statistics with Python/Regression Analysis/Capstone Project_ Surviving the App-pocalypse

! pip install lifelines

# Libraries
import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("googleplaystore.csv")
df.head()

len(df)

# Data Cleaning

# df info
df.info()

# Dropping the first variable
df = df.iloc[:,1:]
df.head()

# Category variable
df.Category.value_counts()

# Remove the '1.9' category
df = df[df['Category'] != '1.9']

# Reviews variable to Numeric
df['Reviews'] = pd.to_numeric(df['Reviews'])

# Size variable
df.Size.value_counts()

# Function to convert size to numerical value
def convert_size(size):
  if 'M' in size:
    return float(size.replace('M', ''))
  elif 'k' in size:
    return float(size.replace('k', '')) / 1000
  elif size == 'Varies with device':
    return np.nan
  else:
    return size

df['Size'] = df['Size'].apply(convert_size)
df['Size'] = df['Size'].fillna(df['Size'].mean())

# Install variable
df.Installs.value_counts()

# Remove commas and plus signs, then convert to integers
df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '').astype(int)

df.head()

df.Type.value_counts()

# Price variable
df.Price.value_counts()

# Remove the dollar sign and convert to float
df['Price'] = df['Price'].str.replace("$", '', regex=False).astype(float)

# Content Rating
df['Content Rating'].value_counts()

# Remove categories with low count
categories_to_remove = ['Adults only 18+', 'Unrated']

# Keep only the rows that do not contain the specified categories
df = df[~df['Content Rating'].isin(categories_to_remove)]
df['Content Rating'].value_counts()

# Genre
df.Genres.value_counts()

# Picking the variables
df_select = df.drop(columns = ['Genres', 'Current Ver', 'Android Ver'])

df_select.head()

# Dependent variable

# App churn is when the app was not updated in 6 months
df_select['Last Updated']

# Convert 'Last Updated' to datetime
df_select['Last Updated'] = pd.to_datetime(df_select['Last Updated'])

# Get the maximum date
max_date = df_select['Last Updated'].max()

# Calculate the date 6 months before the maximum date
threshold_date = max_date - pd.DateOffset(months=6)

# Create a 'churn' variable, 1 if the last updated was before the threshold date, 0 otherwise
df_select['churn'] = (df_select['Last Updated'] < threshold_date).astype(int)

# Display the new column to verify
df_select[['Last Updated', 'churn']].head()

# Mean of the churn variable
df_select.churn.mean()

df_select.churn.value_counts()

# Create a new variable with the duration in days since the last update compared to the max date
df_select['days_since_last_update'] = (max_date - df_select['Last Updated']).dt.days

# Display the new column to verify
df_select[['Last Updated', 'days_since_last_update']].head()

# Data
df_select.head()

# Remove last updated variabel
df_final = df_select.drop(columns=['Last Updated'])

# KME comparing Free vs Paid apps

from lifelines import KaplanMeierFitter

# Create a Kaplan-Meier fitter
kmf = KaplanMeierFitter()

# Divide the data into free and paid apps
free_apps = df_final[df_final['Type'] == 'Free']
paid_apps = df_final[df_final['Type'] == 'Paid']

# Fit the estimator to the free apps
kmf.fit(free_apps['days_since_last_update'],
        event_observed=free_apps['churn'],
        label='Free Apps')
ax = kmf.plot()

# Fit the estimator to the paid apps
kmf.fit(paid_apps['days_since_last_update'],
        event_observed=paid_apps['churn'],
        label='Paid Apps')
kmf.plot(ax=ax)

plt.title('Survival Curve - Free vs Paid Apps')
plt.xlabel('Days since last update')
plt.ylabel('Survival Probability')
plt.show()

# Cox Model creation and assessment

df.head()

# Remove NaN
df_final = df_final.dropna()

# Import necessary libraries
from sklearn.model_selection import train_test_split

# Transform categorical variables into dummy variables
df_final_dummies = pd.get_dummies(df_final, columns=['Category',
                                                     'Type', 'Content Rating'],
                                  drop_first=True)

# Split data into training and testing sets
train, test = train_test_split(df_final_dummies,
                               test_size=0.2,
                               random_state=1502)

# Create an instance of the Cox Proportional Hazards fitter
cph = CoxPHFitter()

# Fit the CoxPH model to the training dataset
cph.fit(train, duration_col='days_since_last_update', event_col='churn')
cph.print_summary()

# Plot the coefficients
plt.figure(figsize=(8, 10))
cph.plot()
plt.show()

# Assesing model on the test set using Concordance Index
c_index = concordance_index(test['days_since_last_update'],
                            -cph.predict_partial_hazard(test),
                            test['churn'])
print(f"Concordance Index on the Test set: {c_index}")

# Check the proportional hazards assumption
cph.check_assumptions(train)
