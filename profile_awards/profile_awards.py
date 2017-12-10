#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 13:44:39 2017

@author: yuchenli
"""

import pandas as pd
award = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/profile_awards/profile_awards.csv", sep = ",", encoding = 'ISO-8859-1')

award_count = dict()
for i in range(len(award)):
    key = award.loc[i,"HBE_ID"]
    if key not in award_count:
        award_count[key] = 1
    else:
        award_count[key] += 1
        
# Mark KOL among Report-Tags
name_standard = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/education_manual_annotation/Profile_Education_Institution_Standard_UTF-8.csv", sep = ",", encoding = 'ISO-8859-1')
target = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/education_manual_annotation/profile_education_Report-Tags.csv", sep = ",", encoding = 'utf-8')

KOL_Report_Tags = dict()
KOL_HBE_ID_set = set(name_standard.loc[:,'HBE_ID'])

for i in set(target.loc[:,'HBE_ID']):
    if i in KOL_HBE_ID_set:
        KOL_Report_Tags[i] = 1
    else:
        KOL_Report_Tags[i] = 0

# Write to csv
import csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/profile_awards/awards_count.csv", "w") as csvfile:
    fieldnames = ['HBE_ID', "awards_count", "KOL"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in award_count.items():
        try:
            writer.writerow({'HBE_ID': key, "awards_count": value, "KOL": KOL_Report_Tags[key]})
        except:
            pass