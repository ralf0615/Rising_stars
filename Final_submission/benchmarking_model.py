#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 15:16:13 2018

@author: yuchenli
@content: identify rising stars by comparing to benchmark
@note: please replace xxxxxx with your own directory
@benchmark: 
    step1: order KOL by the number of publication published during their first 
           15 years since first year of publication
    step2: ping down a group of bottom 30% KOL from step1
    step3: calculate average accumulative number of publication published 
           during their first to first 15 years since first year of publication
    step4: result of step3 is the benchmark
"""

# import package
import pandas as pd


# @input: 
#        "listA", "listB":  two lists of numbers
#         "x": a number between 0 and 1
# Create a function named "compare_list", which compare two list of numbers, 
# if x percentage of number in listA is greater than or equal to the number
# on the same position index of listB, return True, else, return False
# @output, a boolean value
def compare_list(listA, listB, x):
    import math
    result_list = list()
    for i in range(len(listA)):
        result_list.append(listA[i]>=listB[i])
    if result_list.count(True) >= math.floor(float(x) * len(listA)):
        return True
    else:
        return False


# import "number_of_publication_1_15.csv", which is the product of 
# accumulative_number_of_publication.py
df_1 = pd.read_csv("xxxxxx/number_of_publication_1_15.csv")

# @input: 
#        df2
#        age_cutoff: if physician is older than age_cutoff as of today, he/she
#                    is disqualified for rising stars
#        name: generic 
#        
def benchmarking(df, age_cutoff):
    cols = [col for col in df.columns if col not in ["KOL", "Birth_year", "HBE_ID"]]
    df_3 = df.copy(deep = True) # Make a deep copy of df2
    df_3 = df_3[cols] 
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
        birth_year = df.loc[i,"Birth_year"]
        KOL = df.loc[i,"KOL"]
        if pd.isnull(birth_year):
            birth_year = -888888
        list1 = list(df_3.loc[i,])
        
        if KOL == "No":
            if compare_list(list1, benchmark, 0.9) and (int(birth_year) >= (2017 - age_cutoff)):
                rising_stars.append("Yes")
            elif compare_list(list1, benchmark, 0.9) and birth_year == -888888:
                rising_stars.append("Yes iff younger than " + str(age_cutoff))
            else:
                rising_stars.append("No")
        else:
            rising_stars.append("No")
    
    df_3["Rising_stars"] = rising_stars
    return df_3

# Run benchmarking on df_1 with age_cutoff = 50
df_50 = benchmarking(df_1, 50) 
 

# Write to csv      
df_50.to_csv("xxxxxx/Oncology_profile_rising_stars_age_cutoff_50.csv", 
             index = False, na_rep = "NA") 
