#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:34:07 2017

@author: yuchenli
@content: benchmarking rising stars based on certain criterion
"""


'''
Benchmarking Rising Stars according to "Non_KOL_with_benchmark_1_15_transpose.csv"
Benchmark 1-15: bottom 30%
2.5,
3.2,
4.133333333,
5.266666667,
6.966666667,	
8.666666667,
10.16666667,
11.56666667,	
13.56666667,	
16.73333333,	
19.3,	
22.23333333,	
26.5,
31.36666667,	
37.6
'''

import pandas as pd
df2 = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                  "Rising_stars/oncology_profile/Output_data/"
                  "number_of_publication_1_15.csv")


    
def compare_list(listA, listB):
    result = True
    for i in range(len(listA)):
        result  = result and (listA[i] >= listB[i])
    return result

def benchmarking(df2, age_cutoff):
    df = df2.copy(deep = True)
    age_cutoff = int(age_cutoff)
    benchmark = list([2.5,
                        3.2,
                        4.133333333,
                        5.266666667,
                        6.966666667,	
                        8.666666667,
                        10.16666667,
                        11.56666667,	
                        13.56666667,	
                        16.73333333,	
                        19.3,	
                        22.23333333,	
                        26.5,
                        31.36666667,	
                        37.6])
    rising_stars = list()
    for i in range(len(df)):
        birth_year = df.iloc[i,17]
        KOL = df.iloc[i,2]
        if pd.isnull(birth_year):
            birth_year = -888888
        list1 = list(df.iloc[i,[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16]])
        
        if KOL == "No":
            if compare_list(list1, benchmark) and (int(birth_year) >= (2017 - age_cutoff)):
                rising_stars.append("Yes")
            elif compare_list(list1, benchmark) and birth_year == -888888:
                rising_stars.append("Yes iff younger than " + str(age_cutoff))
            else:
                rising_stars.append("No")
        else:
            rising_stars.append("No")
    
    df["Rising_stars"] = rising_stars
    return df

df_50 = benchmarking(df2, 50) 
df_45 = benchmarking(df2, 45)
       
df_50.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
           "Rising_stars/oncology_profile/Output_data/"
           "Oncology_profile_rising_stars_age_cutoff_50.csv", index = False,
           na_rep = "NA") 

df_45.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
           "Rising_stars/oncology_profile/Output_data/"
           "Oncology_profile_rising_stars_age_cutoff_45.csv", index = False,
           na_rep = "NA") 