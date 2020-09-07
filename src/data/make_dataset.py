#Libraries for data processing
import numpy as np
import pandas as pd

#Opening the data
#----------------
#unemp : US Unemployment data by county from 1990-2016
#funding : US Public Food Assistance from 1969-2019
#min_wage : US Minimum Wage by State from 1968-2017

unemp = pd.read_csv('../../data/external/output.csv')
funding = pd.read_csv('../../data/external/datasets_10128_1434247_SNAP_history_1969_2019.csv')
min_wage = pd.read_csv('../../data/external/datasets_46796_84992_Minimum Wage Data.csv',encoding='iso-8859-1')

#Grouping by year and averaging all of the county rates into one
#central value for approximation of the entire US unemployment rate
unemp.groupby('Year').mean().to_csv('../../data/interim/unemployment by year.csv')

#Removing unnecessary data, restricting to the 1990-2016 Fiscal Years and Total Benefits
funding = funding[21:48].loc[:,['Fiscal Year','Total Benefits(M)']]
funding['Total Benefits(M)'] = funding['Total Benefits(M)'].str.replace(',','')
funding.to_csv('../../data/interim/benefits by uear.csv')

#Pull the CPI information, average it across the year for all states, trim year down to 1990-2016
min_wage.groupby('Year').mean()['CPI.Average'][22:-1].to_csv('../../data/interim/cpi average by year.csv')

#Open all generated CSVs
benefits = pd.read_csv('../../data/interim/benefits by year.csv')
cpi = pd.read_csv('../../data/interim/cpi average by year.csv')
unemp = pd.read_csv('../../data/interim/unemployment by year.csv')

#Concatenate horizontally
df = pd.concat([benefits['Total Benefits(M)'],cpi['CPI.Average'],unemp['Rate']],axis=1)

#Rename the index to reflect the year the data relates to
df.index = pd.Series(range(1990,2017))

#Output final combined dataset in CSV
df.to_csv('../../data/processed/benefits_cpi_unemprate_dataset.csv')