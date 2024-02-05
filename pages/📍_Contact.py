
import pandas as pd
import missingno as msno
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
import base64

# Read CSV
df1 = pd.read_csv('Salaries.csv')


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

st.header('📍You can find me here:')

st.markdown("""   """)

st.markdown("""   """)

st.markdown("""   """)


st.markdown(
    """
 **Portfólio:** http://tomnachbar.github.io/portfolio 


**Linkedin:** https://www.linkedin.com/in/elitonnachbar/


**GitHub:** https://github.com/tomnachbar


**E-mail:** nachbars@msn.com


**Instagram:** https://www.instagram.com/tom_nachbar


**Discord:** @tomnachbar

"""


)

# Download Button
def download_df1(df1):
    csv = df1.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data_clean.csv">Download Here</a>'
    return href

# Streamlit app
def main():
    st.markdown('### Clean Data')

    st.markdown(download_df1(df1), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
    
