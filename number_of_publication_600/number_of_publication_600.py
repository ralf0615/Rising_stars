#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:07:09 2017

@author: yuchenli

@content: compile the number of publications per year
"""

import pandas as pd
df = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
                 "number_of_publication_600/600_with_publication_year.csv", 
                 keep_default_na = False, encoding = 'utf-8', dtype = 'object')

# Compile first publication year as a reference
first_pub_600 = dict()

for i in range(len(df)):
    key = df.loc[i,'HBE_ID']
    value = df.loc[i,'Publication_year']
    if pd.isnull(value) == False:
        if (key in first_pub_600):
            try:
                if (int(first_pub_600[key]) > int(value)):
                    first_pub_600[key] = value
            except:
                pass
        else:
            first_pub_600[key] = value

def publication(benchmark, name):
    temp = dict()
    for i in range(len(df)):
        #print(i)
        key = df.loc[i,'HBE_ID']
        value = df.loc[i, 'Journal_Name']
        year = df.loc[i, 'Publication_year']
        if (len(year) <= 4):
            first_publication_year = int(first_pub_600[key])
            if ((int(year) - first_publication_year) <= benchmark):
                if key in temp:
                    temp[key].append(str(value))
                else:
                    temp[key] = [str(value)]
            else:
                pass 
        else:
            pass
        
    import csv
    csv_name = "/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
    "number_of_publication_600/" + name + '.csv'
    with open(csv_name, "w", encoding = 'utf-8') as csvfile:
        fieldnames = ['HBE_ID', "Journal_name"]
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for key, value in temp.items():
            for element in value:
                writer.writerow({'HBE_ID': key, "Journal_name": element})  
    
# Accumulative number of publications
publication(1, "number_of_publication_year_1")
publication(2, "number_of_publication_year_2")
publication(5, "number_of_publication_year_5")
publication(10, "number_of_publication_year_10")
publication(20, "number_of_publication_year_20")



        