#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:34:07 2017

@author: yuchenli
@content: benchmarking rising stars based on certain criterion
"""


'''
Benchmarking Rising Stars according to "Non_KOL_with_benchmark_1_15_transpose.csv"
Benchmark 1-15:
            2.633333333	
            3.4	
            4.4	
            5.766666667	
            7.5	
            9.333333333	
            10.93333333	
            12.33333333	
            14.33333333	
            17.6	
            20.03333333	
            22.96666667	
            26.96666667	
            31.53333333	
            37.6
'''
import pandas as pd
df2 = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                  "Truven_rising_stars/oncology_profile/Output_data/"
                  "number_of_publication_1_15.csv")


    
def compare_list(listA, listB):
    result = True
    for i in range(len(listA)):
        result  = result and (listA[i] >= listB[i])
    return result

def benchmarking(df2, age_cutoff):
    age_cutoff = int(age_cutoff)
    benchmark = list([2.633333333	
            ,3.4	
            ,4.4	
            ,5.766666667	
            ,7.5	
            ,9.333333333	
            ,10.93333333	
            ,12.33333333	
            ,14.33333333	
            ,17.6	
            ,20.03333333	
            ,22.96666667	
            ,26.96666667	
            ,31.53333333	
            ,37.6])
    rising_stars = list()
    for i in range(len(df2)):
        birth_year = df2.iloc[i,17]
        KOL = df2.iloc[i,2]
        if pd.isnull(birth_year):
            birth_year = -888888
        list1 = list(df2.iloc[i,[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16]])
        
        if KOL == "No":
            if compare_list(list1, benchmark) and (int(birth_year) >= (2017 - age_cutoff)):
                rising_stars.append("Yes")
            elif compare_list(list1, benchmark) and birth_year == -888888:
                rising_stars.append("Yes iff younger than " + str(age_cutoff))
            else:
                rising_stars.append("No")
        else:
            rising_stars.append("No")
    
    df2["Rising_stars"] = rising_stars
    return df2

df_50 = benchmarking(df2, 50) 
df_45 = benchmarking(df2, 45)
       
df_50.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
           "Truven_rising_stars/oncology_profile/Output_data/"
           "Oncology_profile_rising_stars_age_cutoff_50.csv", index = False) 

df_45.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
           "Truven_rising_stars/oncology_profile/Output_data/"
           "Oncology_profile_rising_stars_age_cutoff_45.csv", index = False) 