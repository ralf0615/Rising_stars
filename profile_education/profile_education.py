#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 10:17:04 2017

@author: yuchenli
"""

import pandas as pd
education = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                        "Truven_rising_stars/profile_education/"
                        "profile_education_Report-Tags.csv", sep = ",", 
                        encoding = 'ISO-8859-1')

education_count = dict()
for i in range(len(education)):
    key = education.loc[i,"HBE_ID"]
    if key not in education_count:
        education_count[key] = 1
    else:
        education_count[key] += 1
        
# Mark KOL among Report-Tags
name_standard = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                            "Truven_rising_stars/education_manual_annotation/"
                            "Profile_Education_Institution_Standard_UTF-8.csv", 
                            sep = ",", encoding = 'ISO-8859-1')
target = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                     "Truven_rising_stars/education_manual_annotation/"
                     "profile_education_Report-Tags.csv", sep = ",", 
                     encoding = 'utf-8')

KOL_Report_Tags = dict()
KOL_HBE_ID_set = set(name_standard.loc[:,'HBE_ID'])

for i in set(target.loc[:,'HBE_ID']):
    if i in KOL_HBE_ID_set:
        KOL_Report_Tags[i] = 1
    else:
        KOL_Report_Tags[i] = 0

# Write to csv
import csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "profile_education/education_count.csv", "w") as csvfile:
    fieldnames = ['HBE_ID', "education_count", "KOL"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in education_count.items():
        try:
            writer.writerow({'HBE_ID': key, "education_count": value, 
                             "KOL": KOL_Report_Tags[key]})
        except:
            pass