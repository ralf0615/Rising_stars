#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:51:41 2017

@author: yuchenli
"""

import pandas as pd
SJR_weighted = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                           "Truven_rising_stars/SJR_education_clustering/"
                           "600_SJR_weighted.csv", sep = ",", encoding = 'utf-8')
education = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                        "Truven_rising_stars/SJR_education_clustering/"
                        "education_score.csv", sep = ",", encoding = 'utf-8')

# Convert them to dictionaries
SJR_dict = dict(zip(SJR_weighted.ID, SJR_weighted.score))

import csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "SJR_education_clustering/SJR_education.csv", "w") as csvfile:
    fieldnames = ['HBE_ID', "Education_score", "SJR", "KOL"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    i = 0
    for i in range(len(education)):
        HBE_ID = education.loc[i,"HBE_ID"]
        Education_score = education.loc[i, "Education_score"]
        KOL = education.loc[i, "KOL"]
        try:
            SJR = SJR_dict[HBE_ID]
            writer.writerow({'HBE_ID': HBE_ID, "Education_score": Education_score, 
                             "SJR": SJR, "KOL": KOL})
            
        except:
            i=+1
            pass  

# Test: Temp_2972_1004       
test = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                   "Truven_rising_stars/SJR_education_clustering/"
                   "SJR_education.csv", sep = ",", encoding = 'utf-8')
set_1 = set(test.HBE_ID)
set_2 = set(education.HBE_ID)
set_2.difference(set_1)

# Plot test in 2-D
import matplotlib.pyplot as plt

# Take outlier
test = test[test['HBE_ID'] != 'HBE_ONC_1000335']

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.scatter(test[test['KOL']=='No']['SJR'], \
            test[test['KOL']=='No']['Education_score'], 
            s=10, c='b', marker='s', label='Non')

ax1.scatter(test[test['KOL']=='Yes']['SJR'], \
            test[test['KOL']=='Yes']['Education_score'], 
            s=10, c='r', marker='o', label='KOL')
plt.xlabel('SJR')
plt.ylabel('Education_score')
plt.legend(loc='upper right')
plt.show()
