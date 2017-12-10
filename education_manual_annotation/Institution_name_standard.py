#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 11:51:02 2017

@author: yuchenli
"""

# Check how many institution from Report-Tags appear in KOL's institution
import pandas as pd
name_standard = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                            "Truven_rising_stars/education_manual_annotation/"
                            "Profile_Education_Institution_Standard_UTF-8.csv",
                            sep = ",", encoding = 'ISO-8859-1')
target = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                     "Truven_rising_stars/education_manual_annotation/"
                     "profile_education_Report-Tags.csv", 
                     sep = ",", encoding = 'utf-8')

set_1 = set(name_standard.loc[:,'Institution_Name'])
len(set_1)
set_2 = set(target.loc[:,'Institution_Name'])
len(set_2)

match = list()
for i in range(len(target)):
    if (target.loc[i,"Institution_Name"] in set_1):
        match.append(int(1))
    else:
        match.append(int(0))
        
sum(match)

# KOL institution score
institution_score = dict()

for i in range(len(name_standard)):
    key = name_standard.loc[i,'Institution_Name_Standard']
    value = float(1/len(name_standard))
    if pd.isnull(value) == False:
        if (key in institution_score):
            institution_score[key] = institution_score[key] + value
        else:
            institution_score[key] = value
            
# Mapping KOL institution names with their standard names
KOL_institution_name_standard = dict()

for i in range(len(name_standard)):
    key = name_standard.loc[i,'Institution_Name']
    value = name_standard.loc[i,'Institution_Name_Standard']
    if pd.isnull(value) == False:
        if (key not in KOL_institution_name_standard):
            KOL_institution_name_standard[key] = value

# Generate education_score for Report-Tags's HBE_ID
education_score = dict()
for i in range(len(target)): # read target one line at a time
    key = target.loc[i,'HBE_ID'] # set "HBE_ID" as key
    
    # set "HBE_ID" corresponding "Institution_Name" as key_1
    key_1 = target.loc[i,'Institution_Name'] 
    
    if (key not in education_score):
        education_score[key] = 0
    else:
        if key_1 in KOL_institution_name_standard:
            standard_name = KOL_institution_name_standard[key_1]
            value = institution_score[standard_name]
            education_score[key] = education_score[key] + value

len(set(target['HBE_ID']))

# Mark KOL among Report-Tags
KOL_Report_Tags = dict()
KOL_HBE_ID_set = set(name_standard.loc[:,'HBE_ID'])

for i in set(target.loc[:,'HBE_ID']):
    if i in KOL_HBE_ID_set:
        KOL_Report_Tags[i] = 'Yes'
    else:
        KOL_Report_Tags[i] = 'No'
        
# Write to csv
import csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "education_manual_annotation/education_score.csv", "w") as csvfile:
    fieldnames = ['HBE_ID', "Education_score", "KOL"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in education_score.items():
        writer.writerow({'HBE_ID': key, 
                         "Education_score": value,
                         "KOL": KOL_Report_Tags[key]})
        
   
