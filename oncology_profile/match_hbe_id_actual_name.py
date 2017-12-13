#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:28:40 2017

@author: yuchenli
@content: match HBE_ID with name
"""

# Read in Full pubs with full names
import pandas as pd
Full_pubs = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Rising_stars/"
                        'oncology_profile/Input_data/'
                        'Oncology Profiles - Full pubs.csv', 
                         keep_default_na = False, 
                         encoding = 'utf-8', dtype = 'object')

result = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Rising_stars/"
                        'oncology_profile/Output_data/'
                        'Oncology_profile_rising_stars_age_cutoff_50.csv', 
                         keep_default_na = False, 
                         encoding = 'utf-8', dtype = 'object')


# Create a dictionary for full names
Full_name_dict= dict()
for i in range(len(Full_pubs)):
    key = Full_pubs.iloc[i,0]
    name = Full_pubs.iloc[i,1]
    if key not in Full_name_dict:
        Full_name_dict[key] = set([name])
    else:
        if name in Full_name_dict[key]:
            Full_name_dict[key].add(name)
        else:
            pass


# Match HBE_ID with full names     
Full_name = list()
for i in range(len(result)):
    key = result.iloc[i,0]
    if key in Full_name_dict:
        temp_list = list()
        for i in range(len(Full_name_dict[key])):
            temp_list.append(Full_name_dict[key].pop())
        Full_name.append(temp_list)    
    else:
        Full_name.append("NA")
        
result["Full Name"] = Full_name


# Print to csv
result.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
           "Rising_stars/oncology_profile/Output_data/"
           "Oncology_profile_rising_stars_v1.csv", index = False,
           na_rep = "NA") 