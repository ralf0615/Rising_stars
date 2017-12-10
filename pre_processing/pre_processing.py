#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:34:50 2017

@author: yuchenli
"""

import pandas as pd

"""
Profile_Trials_Local, Profile_Trials_Standard, Profile_Press, 
Profile_Sanctions, Profile_Payments
"""

# Import and merge tab 9
tab_9 = []
    
for i in range(1,5):
    
    tab_9.append(pd.read_excel("TOP_ONCOLOGY_Existing_Data_pt" + str(i) + 
                               ".xlsx", sheetname = "Profile_Trials_Local"))
    
tab_9_df = pd.concat(tab_9)
del tab_9
tab_9_df.to_csv('Profile_Trials_Local.csv', sep = ",", index = False)

# Import and merge tab 10
tab_10 = []
    
for i in range(1,5):
    
    tab_10.append(pd.read_excel("TOP_ONCOLOGY_Existing_Data_pt" + str(i) + 
                                ".xlsx", sheetname = "Profile_Trials_Standard"))
    
tab_10_df = pd.concat(tab_10)
del tab_10
tab_10_df.to_csv('Profile_Trials_Standard.csv', sep = ",", index = False)

# Import and merge tab 11
tab_11 = []
    
for i in range(1,5):
    
    tab_11.append(pd.read_excel("TOP_ONCOLOGY_Existing_Data_pt" + str(i) + 
                                ".xlsx", sheetname = "Profile_Press"))
    
tab_11_df = pd.concat(tab_11)
del tab_11
tab_11_df.to_csv('Profile_Press.csv', sep = ",", index = False)

# Import and merge tab 12
tab_12 = []
    
for i in range(1,5):
    
    tab_12.append(pd.read_excel("TOP_ONCOLOGY_Existing_Data_pt" + str(i) + 
                                ".xlsx", sheetname = "Profile_Sanctions"))
    
tab_12_df = pd.concat(tab_12)
del tab_12
tab_12_df.to_csv('Profile_Sanctions.csv', sep = ",", index = False)

# Import and merge tab 13
tab_13 = []
for i in range(1,5):
    
    tab_13.append(pd.read_excel("TOP_ONCOLOGY_Existing_Data_pt" + str(i) + 
                                ".xlsx", sheetname = "Profile_Payments"))
    
tab_13_df = pd.concat(tab_13)
del tab_13
tab_13_df.to_csv('Profile_Payments.csv', sep = ",", index = False)



