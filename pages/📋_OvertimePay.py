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

df1['Year'] = df1['Year'].astype(int)


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

with col1:
    ###3. How is the total of overtime pay by year?

   def graph_sum ( df1, group_col='Year', value_col='OvertimePay', palette='mako', figsize=(10,6), width=0.4, title='OvertimePay By Year',orient='v'):

    sum_overtime = df1[[group_col,value_col]].groupby(group_col).sum().reset_index()
    plt.figure(figsize=figsize)
    ax = sns.barplot(x=group_col, y=value_col, data=sum_overtime, palette=palette,orient=orient, width=width)
    # Adicionando rótulos de dados nos pontos
    for p in ax.patches:
          ax.annotate("{:.2f}".format(height), 
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='center', fontsize=12, color='black', xytext=(0, 8),
                textcoords='offset points')

    plt.title(title)
    plt.tight_layout()
    plt.show()

    st.pyplot(plt, use_container_width=True)

   graph_sum ( df1, group_col='Year', value_col='OvertimePay', palette='mako', figsize=(10,6), title='OvertimePay By Year',orient='v',width=0.6)

 ####. Which job that have gained most overtime pay by year?
 
   with col2:
   
        job_overtime = df1.loc[df1.groupby('Year')['OvertimePay'].idxmax(), ['Year', 'JobTitle', 'OvertimePay']]


        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x='Year', y='OvertimePay', hue='JobTitle', data=job_overtime, palette='viridis',orient='v', width=0.6, dodge=False)
        for p in ax.patches:
          ax.annotate("{:.2f}".format(height), 
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='center', fontsize=12, color='black', xytext=(0, 8),
                textcoords='offset points')
        plt.title('Top OvertimePay by Job and Year')
        plt.tight_layout()
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), fancybox=True, shadow=True, ncol=5)


        st.pyplot(plt, use_container_width=True)
      
    
