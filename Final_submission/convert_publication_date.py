#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:35:42 2018

@author: yuchenli
@content: convert "Publication Date" in Oncology Profiles - Full pubs" to YYYY
          format
@note: please replace xxxxxx with your own directory
"""

# Import packages
import re
import pandas as pd
from dateutil.parser import parse

# Import "Oncology Profiles - Full pubs.csv", name it as df
df = pd.read_csv('xxxxxxx/Oncology Profiles - Full pubs.csv', keep_default_na = False)

# Make a copy of df as df_temp
df_temp = df.copy(deep = True)


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

df_temp['Year'] = df_temp['Publication Date'].map(parse_year)


# Save as csv
df_temp.to_csv('xxxxxx/Full_pubs_with_year.csv', sep = ",", 
               encoding = 'utf-8', index = False)