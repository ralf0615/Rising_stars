#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:19:05 2017

@author: yuchenli
@content: experiment with reading csv
"""

import csv

# Sniff
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "standard_trials/standard_trials.csv", newline = '', 
          encoding = 'utf-8') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    
# Print out the first two lines
snippet = open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
                  "standard_trials/standard_trials.csv", #newline = '', 
                  encoding = 'utf-8')
reader = csv.reader(snippet)
i = 1
while (i<3):
    print(next(reader))
    i+=1
    
    
# Read in standard - trials line by one and process and one that is completed
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "standard_trials/standard_trials.csv", # newline = '', 
          encoding = 'utf-8') as infile:
    line_count = 0
    with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
              "standard_trials/standard_trials_confirmed.csv", "w", 
              encoding = 'utf-8') as outfile:
        reader = csv.reader(infile)
        fieldnames = next(reader)[0:46]
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(fieldnames)
        for row in reader:
            if (str(row[5]) == 'Confirmed' or str(row[5]) == "Conform"):
                row = row[0:46]
                line_count+=1
                writer.writerow(row)
                

# Count trials
import pandas as pd
trials = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
                     "standard_trials/standard_trials_phase_3_4.csv", sep = ",", 
                     encoding = 'utf-8')

trials_count = dict()
for i in range(len(trials)):
    key = trials.loc[i,"HBE_ID"]
    if key not in trials_count:
        trials_count[key] = 1
    else:
        trials_count[key] += 1
        
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
          "standard_trials/trials_count_3_4.csv", "w") as csvfile:
    fieldnames = ['HBE_ID', "trials_count", "KOL"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in trials_count.items():
        try:
            writer.writerow({'HBE_ID': key, "trials_count": value, 
                             "KOL": KOL_Report_Tags[key]})
        except:
            pass