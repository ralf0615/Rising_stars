#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 11:27:10 2017

@author: yuchenli
@content: compile the first year of publication
"""


import pandas as pd

# Import data
nonKOL = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                     'Truven_rising_stars/data_seperate_sheet/'
                     'pubs_nonKOL.csv', sep = ",", encoding = 'utf-8')
kol = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                  'Truven_rising_stars/data_seperate_sheet/'
                  'pubs_KOL.csv', sep = ",", 
                  encoding = 'utf-8', dtype = {'Year': object})

kol = kol.iloc[:,[0,3,16]]
nonKOL = nonKOL.iloc[:,[0,1,3]]

first_pub_nonKOL = dict()

for i in range(len(nonKOL)):
    key = nonKOL.iloc[i,0]
    value = nonKOL.iloc[i,2]
    if pd.isnull(value) == False:
        if (key in first_pub_nonKOL):
            if (int(first_pub_nonKOL[key]) > int(value)):
                first_pub_nonKOL[key] = value
        else:
            first_pub_nonKOL[key] = value
            
            
first_pub_KOL = dict()

for i in range(len(kol)):
    key = kol.iloc[i,0]
    value = kol.iloc[i,2]
    if pd.isnull(value) == False:
        if (key in first_pub_KOL):
            if (int(first_pub_KOL[key]) > int(value)):
                first_pub_KOL[key] = value
        else:
            first_pub_KOL[key] = value

import csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "data_seperate_sheet/first_pub_KOL.csv", "w") as csvfile:
    fieldnames = ['HBE Universal Code', "First Publication Year"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in first_pub_KOL.items():
        writer.writerow({'HBE Universal Code': key, 
                         "First Publication Year": value})
        
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "data_seperate_sheet/first_pub_nonKOL.csv", "w") as csvfile:
    fieldnames = ['HBE Universal Code', "First Publication Year"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in first_pub_nonKOL.items():
        writer.writerow({'HBE Universal Code': key, 
                         "First Publication Year": value})
    
# Compile year of first publication for "Oncology Profiles - Full pubs.csv"
df = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                  'Truven_rising_stars/oncology_profile/'
                  'Full_pubs_with_year.csv', sep = ",", 
                  encoding = 'utf-8', dtype = {'Year': object})

# Subset 3 columns
df = df.iloc[:,[0,3,16]]

Full_pubs_year_first_publication = dict()

for i in range(len(df)):
    key = df.iloc[i,0]
    value = df.iloc[i,2]
    if pd.isnull(value) == False:
        try: 
            if (key in Full_pubs_year_first_publication):
                if (int(Full_pubs_year_first_publication[key]) > int(value)):
                    Full_pubs_year_first_publication[key] = value
            else:
                Full_pubs_year_first_publication[key] = value
        except:
            continue
            
import csv
with open("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "oncology_profile/Full_pubs_year_first_publication.csv", "w") as csvfile:
    fieldnames = ['HBE Universal Code', "First Publication Year"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in Full_pubs_year_first_publication.items():
        writer.writerow({'HBE Universal Code': key, 
                         "First Publication Year": value})