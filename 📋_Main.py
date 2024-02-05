
import pandas as pd
import missingno as msno
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

st.set_page_config(page_title='San Francisco Salaries', page_icon='🌉', layout='wide')

# Read CSV
df = pd.read_csv('Salaries.csv',low_memory=False)

df1 = df.copy()


### EXPLORATORY ANALISYS OF DATA

df1.info()

for column in df1.columns:
    unique_values = df1[column].unique()
    print(f'Unique values in {column}: {unique_values}')

df1.describe(include="all")

missing_percentage = df1.isnull().mean() * 100
print("Percentage of missing values for each column:")
print(missing_percentage)

### DROPING ROWS WITH NOT VALUABLE INFOS

df1.drop(columns='EmployeeName',inplace=True)
df1.drop(columns='Status',inplace=True)
df1.drop(columns='Notes',inplace=True)
df1.drop(columns='TotalPayBenefits',inplace=True)

### SETUP JOBTITLE COLUMN FOR UPPER

df1["JobTitle"] = df1["JobTitle"].str.upper()

### CLEANING OF NOT PROVIDED AND NAN ROWS

not_provided_jobs = df1['JobTitle'] == 'NOT PROVIDED'

df1.drop(df1[not_provided_jobs].index, inplace=True)

not_provided_basepay = df1['BasePay'] == 'Not Provided'

df1.drop(df1[not_provided_basepay].index, inplace=True)

df1 = df1.dropna(subset=['BasePay'])

### FILLING COLUMNS WITH NAN FOR ZERO

df1['OvertimePay'].fillna(0, inplace=True)
df1['Benefits'].fillna(0, inplace=True)
df1['OtherPay'].fillna(0, inplace=True)

### TRANSFORMING TYPE OF COLUMNS BASEPAY, OVERTIMEPAY, OTHERPAY AND BENEFITS TO FLOAT

df1['BasePay'] = df1['BasePay'].astype(float)

df1['OvertimePay'] = df1['OvertimePay'].astype(float)

df1['OtherPay'] = df1['OtherPay'].astype(float)

df1['Benefits'] = df1['Benefits'].astype(float)

### CHECKING TYPES OF ROWS

#df1.dtypes


## -------------------------------------------- MAINLY QUESTIONS ------------------------------------------------ #### 

#### One way to understand how a city government works is by looking at who it employs and how its employees are compensated. This data contains the names,job title, and compensation for San Francisco city employees on an annual basis from 2011 to 2014.

# What the average of total pay, overtime pay and benefits by year?

# How is the total of overtime pay by year?

# How much is the total of benefits by year?

# Which job that have gained most overtime pay by year?

# What jobs that have gained more benefits by year?

# What relative and accumulated percentage of the 20 biggest jobs represent of the total value?

# What the most frequent of range pay by year?

# What the count of each job?

# What the average of payment by job and year?

# Which jobs have debts with the government?



st.image('sf.jpeg', use_column_width='auto', channels="RGB", output_format="JPEG")

st.header('Salaries of Government San Francisco in 2011 at 2014 🌉')

st.divider()

st.subheader('Introduction')

st.write(' This page is made with the purpose of show some analysis of the salaries paid in government of San Francisco between 2011 and 2014..')
st.write('In the main page, you see some descriptive data about the payment in the years.')

st.subheader('How to use this Dashboard')

st.write('In the sidebar, there are pages separated in category of payments and Job Title, there are filters that are possible choose the Title of Job or the Year.')

st.write('In the Side Bar are these pages:')
st.write(' 💼 Job Title: There are some analysis made with the name of the jobs, there are possible to understand how many jobs there in SF, and others analysis.')
st.write(' 📉 Benefits: Information about of Benefits payment through the years and Jobs.')
st.write(' 📊 Total Pay: Information about of total payment of the salaries through the years, and the percentages of the distribuition by Job')
st.write(' 📋 Overtime Pay: Information about of overtime payment through the years and Jobs')
st.write('📍 Contact: Here you can find my contact information')

'---'
st.subheader('Source of Data')
st.write('The data csv used is public and are available to download in this link: (https://www.kaggle.com/datasets/kaggle/sf-salaries)')
st.write('The data cleaned are available for download in the page contact in the sidebar.')

