#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:49:03 2017

@author: yuchenli
@content: extract publication year from "Publication Date" variable
"""
  
# New "Oncology Profiles - Full pubs" data
import pandas as pd
df = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                 'Rising_stars/oncology_profile/Input_data/'
                 'Oncology Profiles - Full pubs.csv', keep_default_na = False)
# Import "Oncology Profiles - Full pubs.csv", name it as df

# Check the data type of each column
df.dtypes

# Modify "Publication Date"
from dateutil.parser import parse
df_temp = df.copy(deep = True) # Make a copy of df


# Regular expression matching
import re 

# Print out "Publication Date" with "MMM-YY" format
match = df_temp['Publication Date'].str.contains('\A[a-zA-Z]{3}[-]\d{2}', 
               regex = True)

match_df = df_temp['Publication Date'][match == True] 

# Print out "Publication Date" with "YYYY" format
match_2 = df_temp['Publication Date'].str.contains("\A\d{4}", regex = True)
match_2_df = df_temp['Publication Date'][match_2 == True]
match_2_df.dtype
match_2_df = pd.DataFrame(match_2_df)


# Define parse_year function
# @input: individual "Publication Date" string
# @output: a string of YYYY format
def parse_year(string):
    initial_string = string
    pattern1 = re.compile("\A[a-zA-Z]{3}[-]\d{2}") # "MMM-YY"
    pattern2 = re.compile("\A\d{4}") # "YYYY"
    pattern3 = re.compile("\A\d{4}[-]\d{4}") # "YYYY-" + any sequence of 4 digits
#    pattern4 = re.compile("\d{2}[-]\A{3}")

#    if math.isnan(string):
#        string = string

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
    else:
        try:
            string = str(parse(string, fuzzy = True).year)
        except (ValueError, TypeError): string = string   
    return string

match_2_df["After Match"] = match_2_df['Publication Date'].map(parse_year)
        
df_temp['Year'] = df_temp['Publication Date'].map(parse_year)
#df_temp.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/'
#               'oncology_profile/Outpt_data/Full_pubs_with_year.csv', sep = ",", 
#               encoding = 'utf-8', index = False)

# df_temp['Year'] = df_temp['Year'].astype('category')
year_frequency = df_temp['Year'].value_counts()

