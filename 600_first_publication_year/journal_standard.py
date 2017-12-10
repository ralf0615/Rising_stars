#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-09-11 09:25:15

@author: yuchenli
"""

# Import standard_pubs_confirmed.csv
import pandas as pd
df = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
                 "600_first_publication_year/standard_pubs_confirmed.csv", 
                 keep_default_na=False, encoding = 'utf-8', dtype = 'object')

# Modify Publication_date
from dateutil.parser import parse
df_temp = df.copy(deep = True)

# Regular expression matching
import re

match = df_temp['Publication_date'].str.contains('\A[a-zA-Z]{3}[-]\d{2}', regex = True)
match_df = df_temp['Publication_date'][match == True] # Print out "Publication_date" with "MMM-YY" format

match_2 = df_temp['Publication_date'].str.contains("\A\d{4}", regex = True)
match_2_df = df_temp['Publication_date'][match_2 == True]
match_2_df.dtype
match_2_df = pd.DataFrame(match_2_df)

def parse_Year(string):
    initial_string = string
    pattern1 = re.compile("\A[a-zA-Z]{3}[-]\d{2}") # "MMM-YY"
    pattern2 = re.compile("\A\d{4}") # "YYYY"
    pattern3 = re.compile("\A\d{4}[-]\d{4}")
    pattern4 = re.compile("\A\d{2}[-][a-zA-Z]{3}") # "YY-MMM"
    #pattern4 = re.compile("\d{2}[-]\A{3}")
    """
    if math.isnan(string):
        string = string
    """
    if pattern1.match(string):
        if int(string.split("-")[1]) <= 17: # For instance like "MMM-YY" where YY less than 2017
            string = str("20" + string.split("-")[1]) # "MMM-YY"
        else:
            string = str("19" + string.split("-")[1]) # "MMM-YY"        
    elif pattern2.match(string):
        string = string.split(" ")[0] # "1974 Jul-Sep"
        if string == initial_string and (len(string) == 4 or len(string) == 10): # "YYYY-mm-dd" or "YYYY"
            string = str(parse(string, fuzzy = True).year)
        elif pattern3.match(string):
            string = string.split("-")[0]
    elif pattern4.match(string) and len(initial_string) <= 6: # '18-Mar-16' was matched, wrongly: # '10-Jun'
        if int(string.split("-")[0]) <= 17: # For instance like "YY-MMM" where YY less than 2017
            string = str("20" + string.split("-")[0]) 
        else:
            string = str("19" + string.split("-")[0])
    else:
        try:
            string = str(parse(string, fuzzy = True).year)
        except (ValueError, TypeError): string = string   
    return string

match_2_df["After Match"] = match_2_df['Publication_date'].map(parse_Year)
        
df_temp['Publication_year'] = df_temp['Publication_date'].map(parse_Year)
df_temp = df_temp.loc[:,('HBE_ID', 'Publication_date', 'Publication_year', 
                         'Unique_hash_value', 'Journal_Name')]
df_temp.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
               "600_first_publication_year/600_with_publication_year.csv", 
               sep = ",", encoding = 'utf-8', index = False)    

    
# Compile first publication year for 600 Report-Tags
publication_year_600 = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                                   "Truven_rising_stars/"
                                   "600_first_publication_year/"
                                   "600_with_publication_year.csv", 
                                   sep = ",", encoding = 'utf-8')

first_pub_600 = dict()

for i in range(len(publication_year_600)):
    key = publication_year_600.loc[i,'HBE_ID']
    value = publication_year_600.loc[i,'Publication_year']
    if pd.isnull(value) == False:
        if (key in first_pub_600):
            try:
                if (int(first_pub_600[key]) > int(value)):
                    first_pub_600[key] = value
            except ValueError:
                pass
        else:
            first_pub_600[key] = value

import csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "600_first_publication_year/600_first_publication_year.csv", "w")\
as csvfile:
    fieldnames = ['HBE_ID', "First_publication_year"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in first_pub_600.items():
        writer.writerow({'HBE_ID': key, "First_publication_year": value})