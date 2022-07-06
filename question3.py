import requests
import pandas as pd
from pandas import json_normalize 

def get_val_result(valcode):
  response = requests.get('https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&sort=exchangedate&order=desc&json')
  nbu_json = response.json()
  df = json_normalize(nbu_json)

  #1) дати із найнижчим та найвищим курсом цієї валюти до гривні
  val_df = df[df['cc'] == valcode]
  max_rate = val_df[val_df['rate_per_unit'] == val_df['rate_per_unit'].max()]['exchangedate'].values[0]
  min_rate = val_df[val_df['rate_per_unit'] == val_df['rate_per_unit'].min()]['exchangedate'].values[0]

  #2)середньорічний курс цієї валюти до гривні
  mean_year_rate = val_df['rate_per_unit'].mean()

  #3)стандратне відхилення
  year_std = val_df['rate_per_unit'].std()

  #4)середьорічний крос-курс до євро через гривню
  eur_df = df[df['cc'] == 'EUR'][['exchangedate','rate_per_unit']]
  val_df = pd.merge(val_df, eur_df, how='left', on='exchangedate',suffixes=('','_eur'))
  val_df['cross_rate'] = val_df['rate_per_unit'] / val_df['rate_per_unit_eur']
  year_cross_rate = val_df['cross_rate'].mean()

  #5) код валюти яка має найближчий середьорічний курс  до обраної валюти у порівняннї з гривнею
  mean_year_rate_all = df[df['cc'] != valcode].groupby('cc')['rate_per_unit'].mean().reset_index()
  closest_val = mean_year_rate_all.iloc[(mean_year_rate_all['rate_per_unit']-mean_year_rate).abs().argsort()[:1]]['cc'].values[0]

  result = {
      'max_rate':max_rate,
      'min_rate':min_rate,
      'mean_year_rate':mean_year_rate,
      'year_std':year_std,
      'year_cross_rate':year_cross_rate,
      'closest_val':closest_val
  }
  
  return result
