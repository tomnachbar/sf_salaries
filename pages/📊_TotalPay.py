
import pandas as pd
import missingno as msno
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st



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


## ----------------------------------------- SIDEBAR ------------------------------------ ##

with st.sidebar:

   st.sidebar.title('Navigation Bar')
   st.sidebar.markdown(""" ___ """)
   st.sidebar.header('FILTERS')

# FILTER of YEAR

# ==================================================================== #
st.sidebar.markdown('**YEAR FILTER:**')   
#year = st.sidebar.slider('Choose the Year:', df1['Year'].min(), df1['Year'].max(), (df1['Year'].min(), df1['Year'].max()))

year = st.sidebar.slider('Choose the year:', min_value=2011,
                max_value=2014,
                value=int(df1['Year'][0]),
                step=1)


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
#df1_filtered = df1[(df1['Year'] >= year[0]) & (df1['Year'] <= year[1])]
df1_filtered = df1[(df1['Year'] >= year) & (df1['Year'] <= year)]

df1 = df1_filtered[df1_filtered['JobTitle'].isin(job)]


# ------------------------------------------- ANALYSE ------------------------------------- ##
st.container()
col1, col2 = st.columns(2)

### What the average of total pay, overtime pay and benefits by year?

with col1:
  def avg_totalpay(df1):
    avg_totalpay = df1[['TotalPay', 'Year', 'OvertimePay', 'Benefits']].groupby('Year').mean().reset_index()
    avg_totalpay_long = avg_totalpay.melt(id_vars='Year', var_name='Category', value_name='Average')

    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(x='Year', y='Average', hue='Category', data=avg_totalpay_long, palette='viridis', marker='o', sort=False)
    ax.grid(False)
    plt.rcParams['font.family'] = 'Calibri'
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    for line in ax.lines:
        x_data, y_data = line.get_data()
        for x, y in zip(x_data, y_data):
            ax.annotate("{:.2f}".format(y), 
                        (x, y), 
                        textcoords="offset points",
                        xytext=(0,12), 
                        ha='center')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=1, fontsize='medium')

    plt.title('Average of TotalPay, OvertimePay and Benefits by Year')
    plt.xlabel('Year')
    plt.ylabel('Average')

    st.pyplot(plt, use_container_width=True)
avg_totalpay(df1)
  
### What relative and accumulated percentage of the 20 biggest jobs represent of the total value?

 with col2:

    st.markdown('**Top 20 Percentage Relative and Accumulated of Total Value**')

    percent = df1[['JobTitle', 'TotalPay', 'Year']].groupby('JobTitle')['TotalPay'].sum().reset_index()
    percent['Percentage'] = percent['TotalPay'] / percent['TotalPay'].sum() * 100

    top_20_percent = percent.nlargest(20, 'Percentage').reset_index()

    top_20_percent['Percentage Accumulated'] = top_20_percent['Percentage'].cumsum()

    st.dataframe(top_20_percent, use_container_width=True)

### What the average of payment by job and year?

avg_job_year= df1[['JobTitle','BasePay','Year']].groupby(['JobTitle','Year']).mean().sort_values('Year', ascending=False).reset_index()

avg_job_year.head(20)
