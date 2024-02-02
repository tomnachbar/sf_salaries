import pandas as pd
import missingno as msno
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st


# Read CSV
df = pd.read_csv('Salaries.csv')

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


## ----------------------------------------- SIDEBAR ------------------------------------ ##

with st.sidebar:

   st.sidebar.title('Navigation Bar')
   st.sidebar.markdown(""" ___ """)
   st.sidebar.header('FILTERS')

# FILTER of YEAR

# ==================================================================== #
st.sidebar.markdown('**YEAR FILTER:**')   
year = st.sidebar.slider('Choose the Year:', df1['Year'].min(), df1['Year'].max(), (df1['Year'].min(), df1['Year'].max()))

# FILTER of JOB
# ==================================================================== #
st.sidebar.markdown('**JOB FILTER:**')   
job = st.sidebar.multiselect(label='Choose the Job Title:',
                          options=df1.loc[:,'JobTitle'].unique().tolist(),
                                default=['TRANSIT OPERATOR', 'REGISTERED NURSE', 'FIREFIGHTER', 'POLICE OFFICER 3', 
                                         'DEPUTY SHERIFF', 'ATTORNEY (CIVIL/CRIMINAL)', 'SPECIAL NURSE', 'SERGEANT 3', 
                                         'POLICE OFFICER 2', 'CUSTODIAN', 'POLICE OFFICER', 'EMT/PARAMEDIC/FIREFIGHTER', 
                                         'LIEUTENANT, FIRE SUPPRESSION', 'POLICE OFFICER III', 'PATIENT CARE ASSISTANT',
                                           'TRANSIT SUPERVISOR', 'NURSE PRACTITIONER', 'ENGINEER', 'GENERAL LABORER', 
                                           'STATIONARY ENGINEER'])   



# DATAFRAME FILTERED
# ==================================================================== #
df1_filtered = df1[(df1['Year'] >= year[0]) & (df1['Year'] <= year[1])]

df1 = df1_filtered[df1_filtered['JobTitle'].isin(job)]


# ------------------------------------------- ANALYSE ------------------------------------- ##

st.container()
col1, col2 = st.columns(2)

with col1:
### What the most frequent of range pay by year?
    
    ranges = [0, 10000, 35000, 50000, 90000, 120000, float('inf')]
    labels = ['Range 1', 'Range 2', 'Range 3', 'Range 4', 'Range 5', 'Range 6']

    df1['Range Payment'] = pd.cut(df1['BasePay'], bins=ranges, labels=labels, right=False)

    count_ranges = df1.groupby(['Year', 'Range Payment']).size().reset_index(name='Count')

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Range Payment', y='Count', hue='Year', data=count_ranges, palette='viridis')

    ranges_label = {
        'Range 1': '< $10,000',
        'Range 2': '$10,000 - $35,000',
        'Range 3': '$35,000 - $50,000',
        'Range 4': '$50,000 - $90,000',
        'Range 5': '$90,000 - $120,000',
        'Range 6': '>= $120,000',
    }

    plt.title('Count of Total Pay by Range and Year')
    plt.xlabel('Range of Total Pay')
    plt.ylabel('Count')
    plt.xticks(ticks=range(6), labels=[ranges_label[label] for label in count_ranges['Range Payment'].unique()])
    plt.legend(title='Year')

    st.pyplot(plt,use_container_width=True)

with col2:
        
    ### What the count of each job?

    job_counts = df1['JobTitle'].value_counts().head(10)

    plt.figure(figsize=(10,6))
    barplot = sns.barplot(x=job_counts.index, y=job_counts)
    plt.xlabel('Name of Job')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.title('Count of Qty of Job')

    # Annotate each bar with its count
    for i in range(len(job_counts)):
        plt.text(i, job_counts[i], str(job_counts[i]), ha='center', va='bottom')

    st.pyplot(plt,use_container_width=True)

st.container()

### Which jobs have debts with the government?

count_zero= df1.loc[:,'TotalPay'] <= 0

count_debt = df1.loc[count_zero, ['JobTitle','TotalPay','Year','BasePay']].groupby(['JobTitle','Year']).min().sort_values(['TotalPay','BasePay'],ascending=True).reset_index()

st.subheader('Job that have debts or zero payments')
st.dataframe(count_debt, use_container_width=True)

