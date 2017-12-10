#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:49:03 2017

@author: yuchenli
@content: extract publication year from "Publication Date" variable
"""

# Check working directory
import os

# Import Profile_Publications_Standard
import pandas as pd
df = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                 'Truven_rising_stars/data_seperate_sheet/'
                 'Profile_Publications_Standard.csv', keep_default_na=False)
df.dtypes # Check the data type of each column

# Modify Publication Date
from dateutil.parser import parse
df_temp = df.copy(deep = True)

# Regular expression matching
import re

match = df_temp['Publication Date'].str.contains('\A[a-zA-Z]{3}[-]\d{2}', regex = True)
match_df = df_temp['Publication Date'][match == True] # Print out "Publication Date" with "MMM-YY" format

match_2 = df_temp['Publication Date'].str.contains("\A\d{4}", regex = True)
match_2_df = df_temp['Publication Date'][match_2 == True]
match_2_df.dtype
match_2_df = pd.DataFrame(match_2_df)

def parse_Year(string):
    initial_string = string
    pattern1 = re.compile("\A[a-zA-Z]{3}[-]\d{2}") # "MMM-YY"
    pattern2 = re.compile("\A\d{4}") # "YYYY"
    pattern3 = re.compile("\A\d{4}[-]\d{4}")
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
    else:
        try:
            string = str(parse(string, fuzzy = True).year)
        except (ValueError, TypeError): string = string   
    return string

match_2_df["After Match"] = match_2_df['Publication Date'].map(parse_Year)
        
df_temp['Year'] = df_temp['Publication Date'].map(parse_Year)
df_temp.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/'
               'data_seperate_sheet/pubs_KOL.csv', sep = ",", 
               encoding = 'utf-8', index = False)

# df_temp['Year'] = df_temp['Year'].astype('category')
year_frequency = df_temp['Year'].value_counts()


# Import "SJR_Rank_2016" and "Profile"
SJR_Rank = pd.read_excel("data_seperate_sheet/SJR Ranking 2016.xlsx", 
                         keep_default_na = False)
Profile = pd.read_csv("data_seperate_sheet/Pos_profile.csv", 
                      keep_default_na = False)

# Subset "Profile", keep "HBE Universal Code", "First_Name", and "Last_Name"
Profile.rename(columns = {"HBE_ID" : "HBE Universal Code"}, inplace = True)
Profile_temp = Profile[["HBE Universal Code", "First_Name", "Last_Name"]].copy()
Profile_temp_drop = Profile_temp.drop_duplicates(subset='HBE Universal Code') # Dedup

# Merge 'df_temp' with 'Profile_temp_drop'
Standard_1 = df_temp.merge(Profile_temp_drop, on = "HBE Universal Code", 
                           how = 'left')
# Standard.shape
# df_temp.shape

# Merge 'Standard_1' with 'SJR_Rank_2016'
SJR_Rank.rename(columns = {"Title" : "Journal Name"}, inplace = True)
SJR_Rank_temp = SJR_Rank[["Journal Name", "H index", "SJR"]].copy().drop_duplicates(subset = 'Journal Name')
Standard_2 = Standard_1.merge(SJR_Rank_temp, on = 'Journal Name', how = 'left')
Standard_2.drop(['Full Name', 'Author Match', 'URL', 'Verification Status',
                 'Query Type', 'Query Used', 'Affiliation'], 
                 axis = 1, inplace = True)
    
    
""" Non - KOLs """
# Read in standard_pubs_3.csv, which compiled from R
df_nonKOL = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                        'Truven_rising_stars/data_seperate_sheet/'
                        "standard_pubs_3.csv", keep_default_na=False)
nonKOL_match_2 = df_nonKOL['Publication_date'].str.contains('\A[a-zA-Z]{3}[-]\d{2}', regex = True)
nonKOL_match_2_df = df_nonKOL['Publication_date'][nonKOL_match_2 == True]
nonKOL_match_2_df.dtype
nonKOL_match_2_df = pd.DataFrame(nonKOL_match_2_df)

nonKOL_match_2_df["After Match"] = nonKOL_match_2_df['Publication_date'].map(parse_Year)

# Parse year
df_nonKOL_temp = df_nonKOL.copy(deep = True)
df_nonKOL_temp['Year'] = df_nonKOL_temp['Publication_date'].map(parse_Year)
year_frequency_nonKOL = df_nonKOL_temp['Year'].value_counts()
df_nonKOL_temp.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                      "Truven_rising_stars/data_seperate_sheet/"
                      "pubs_nonKOL.csv", sep = ",", encoding = 'utf-8', 
                      index = False)
