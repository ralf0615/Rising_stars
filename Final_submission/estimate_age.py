#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:28:48 2018

@author: yuchenli
@content: estimate physician's age
@note: replace xxxxxx with your own directory
"""

# Import packages
import pandas as pd
import csv

# import "profile_education.csv", the file we received has following variables:
# HBE_ID, Institution_Name, Education_Type, Degree, Honors
# Start_Date, End_Date, Profile_Education_Code
df1 = pd.read_csv("xxxxxx/profile_education.csv")


# Define degree_undergraduate function that marks a string as True if it is an 
# undergraduate degree
# @input: a string, found in "profile_education.csv"
# @output: a boolean, tells whether the string is a undergraduate degree
def degree_undergraduate(degree_type):
    if pd.isnull(degree_type):
        return False
    
    else:
        found = False
        degree_list = ('B.S', 'A.B.', 'B.A.', 'B.E', 'Bachelor', 'B.Sc.', 'B.E.S')
        for element in degree_list:
            found = found or (element in degree_type)
        return found
    

# Define degree_graduate function that marks a string as True if it is an 
# graduate degree
# @input: a string, found in "profile_education.csv"
# @output: a boolean, tells whether the string is a graduate degree
def degree_graduate(degree_type):
    if pd.isnull(degree_type):
        return False
    
    else:
        found = False
        degree_list = ('M.D.')
        for element in degree_list:
            found = found or (element in degree_type)
        return found
    

# Construct a dictionary named "year_of_school", 
# @key: "HBE_ID"
# @value: "Date", "Date_Type" and "Type"

year_of_school = dict()
for i in range(len(df1)):
    HBE_id = df1.loc[i,"HBE_ID"]
    start_date = df1.loc[i,"Start_Date"]
    end_date = df1.loc[i,"End_Date"]
    education_type = df1.loc[i,"Education_Type"]
    degree = df1.loc[i,"Degree"]

    date_type = 0
    
    # No start_date nor end_date
    if pd.isnull(start_date) and pd.isnull(end_date):
        date_type = 1
        continue
    
    # With start_date and end_date
    elif (not pd.isnull(start_date)) and (not pd.isnull(end_date)):
        date_type = 2
        
    # With start_date no end_date
    elif (not pd.isnull(start_date)) and pd.isnull(end_date):
        date_type = 2
        
    # Without start_date but end_date
    else:
        date_type = 4
    
    if education_type == "Undergraduate" and degree_undergraduate(degree):
        if HBE_id not in year_of_school:
            if date_type == 2:
                # ### for undergraduate
                year_of_school[HBE_id] = {"Date": int(start_date),
                                     "Type": "### " + education_type + ":" + degree,
                                     "Date_type": 'Start'}
               
            if date_type == 4:
                year_of_school[HBE_id] = {"Date": int(end_date),
                                     "Type": "### " + education_type + ":" + degree,
                                     "Date_type": 'End'}
        else:
            if date_type == 2:
                if int(start_date) < year_of_school[HBE_id]['Date']:
                    year_of_school[HBE_id]['Date'] = int(start_date)
                    year_of_school[HBE_id]['Date_type'] = "Start"                  
                    
            if date_type == 4:
                if int(end_date) < year_of_school[HBE_id]['Date']:
                    year_of_school[HBE_id]['Date'] = int(end_date)
                    year_of_school[HBE_id]['Date_type'] = "End"
                    
    
    elif education_type == "Graduate" and degree_graduate(degree):
        if HBE_id not in year_of_school:
            # +++ for graduate
            if date_type == 2:
                year_of_school[HBE_id] = {"Date": int(start_date),
                                     "Type": "+++ " + education_type + ":" + degree,
                                     "Date_type": 'Start'}
               
            if date_type == 4:
                year_of_school[HBE_id] = {"Date": int(end_date),
                                     "Type": "+++ " + education_type + ":" + degree,
                                     "Date_type": 'End'}

        else:
            if date_type == 2:
                if int(start_date) < year_of_school[HBE_id]['Date']:
                    year_of_school[HBE_id]['Date'] = int(start_date)
                    year_of_school[HBE_id]['Date_type'] = "Start"                  
                    
            if date_type == 4:
                if int(end_date) < year_of_school[HBE_id]['Date']:
                    year_of_school[HBE_id]['Date'] = int(end_date)
                    year_of_school[HBE_id]['Date_type'] = "End"
     
               
# Estimate age, construct a dictionary named "year_of_birth",
# @key: "HBE_ID"
# @value: "Year_of_birth"
## +++ for M.D and ### for undergraduate
year_of_birth = dict()
for HBE_ID, value in year_of_school.items():
    if value['Date_type'] == 'End' and "+++" in value['Type']:
        year_of_birth[HBE_ID] = value["Date"] - 26
    elif value['Date_type'] == 'Start' and "+++" in value['Type']:
        year_of_birth[HBE_ID] = value["Date"] - 22
    elif value['Date_type'] == 'Start' and "###" in value['Type']:
        year_of_birth[HBE_ID] = value["Date"] - 18
    elif value['Date_type'] == 'End' and "###" in value['Type']:
        year_of_birth[HBE_ID] = value["Date"] - 22
        

# Write "year_of_birth" to csv
with open("xxxxxx/Oncology_profile_year_of_birth.csv", "w") as csvfile:
    fieldnames = ['HBE_ID', "Year_of_birth"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in year_of_birth.items():
        writer.writerow({'HBE_ID': key, 
                         "Year_of_birth": value}) 

