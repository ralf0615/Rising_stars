#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 10:00:55 2017

@author: yuchenli
@content: estimate physician's age
"""

import pandas as pd
import csv

df1 = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                  "Truven_rising_stars/oncology_profile/Input_data/"
                  "profile_education.csv")


def degree_undergraduate(degree_type):
    if pd.isnull(degree_type):
        return False
    
    else:
        found = False
        degree_list = ('B.S', 'A.B.', 'B.A.', 'B.E', 'Bachelor', 'B.Sc.', 'B.E.S')
        for element in degree_list:
            found = found or (element in degree_type)
        return found
    

def degree_graduate(degree_type):
    if pd.isnull(degree_type):
        return False
    
    else:
        found = False
        degree_list = ('M.D.')
        for element in degree_list:
            found = found or (element in degree_type)
        return found
    
   
j = 0
null_list = list()


year_of_school = dict()
for i in range(len(df1)):
    HBE_id = df1.iloc[i,0]
    start_date = df1.iloc[i,6]
    end_date = df1.iloc[i,7]
    education_type = df1.iloc[i,3]
    degree = df1.iloc[i,4]

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
                    
# Estimate age
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
        

# Write to csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/"
          "Truven_rising_stars/oncology_profile/Output_data/"
          "Oncology_profile_year_of_birth.csv", "w") as csvfile:
    fieldnames = ['HBE_ID', "Year_of_birth"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in year_of_birth.items():
        writer.writerow({'HBE_ID': key, 
                         "Year_of_birth": value})  

                
    