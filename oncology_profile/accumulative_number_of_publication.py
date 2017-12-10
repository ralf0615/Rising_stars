#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:07:09 2017

@author: yuchenli

@content: compile the number of publications per year
"""
import pandas as pd

# Read KOL roster
KOL_roster = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                         "Truven_rising_stars/oncology_profile/Input_data/"
                         "pubs_KOL.csv", keep_default_na = False, 
                         encoding = 'utf-8', dtype = 'object')

KOL_roster_list = set(list(KOL_roster['HBE Universal Code']))


# Read year_of_birth
year_of_birth = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                            "Truven_rising_stars/oncology_profile/Output_data/"
                            "Oncology_profile_year_of_birth.csv", 
                            keep_default_na = False, 
                            encoding = 'utf-8', dtype = 'object')

year_of_birth_dict = dict()
for i in range(len(year_of_birth)):
    key = year_of_birth.iloc[i,0]
    value = int(year_of_birth.iloc[i,1])
    year_of_birth_dict[key] = value
    


# Compile accumulative number of publications for "Full_pubs_with_year"
df = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
                 "oncology_profile/Output_data/Full_pubs_with_year.csv", 
                 keep_default_na = False, encoding = 'utf-8', dtype = 'object')

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

def publication(benchmark, name):
    temp = dict()
    for i in range(len(df)):
        #print(i)
        key = df.loc[i,'HBE Universal Code']
        value = df.loc[i, 'PMID']
        year = df.loc[i, 'Year']
        try:         
            if (len(year) <= 4):
                first_publication_year = int(Full_pubs_year_first_publication[key])
                if ((int(year) - first_publication_year) <= benchmark):
                    if key in temp:
                        temp[key]['Count'] = temp[key]['Count'] + 1
                    else:
                        if key in KOL_roster_list:
                            temp2 = {'KOL':'Yes'}                
                        else:
                            temp2 = {'KOL':'No'}
                        temp[key] = temp2
                        temp[key]['Count'] = 1
                else:
                    pass 
            else:
                pass
        except ValueError:
            print("Invalid year: " + year)
            pass
           
    import csv
    csv_name = "/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"\
    "oncology_profile/Output_data/" + name + '.csv'
    with open(csv_name, "w", encoding = 'utf-8') as csvfile:
        column_name = "Number_of_publication_" + str(benchmark)
        fieldnames = ['HBE_ID', column_name, 'KOL']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        for key, value in temp.items():
            writer.writerow({'HBE_ID': key, 
                             column_name: value['Count'],
                             'KOL': value['KOL']})  
    
# Accumulative number of publications
publication(1, "number_of_publication_year_1")
publication(2, "number_of_publication_year_2")
publication(3, "number_of_publication_year_3")
publication(4, "number_of_publication_year_4")
publication(5, "number_of_publication_year_5")
publication(6, "number_of_publication_year_6")
publication(7, "number_of_publication_year_7")
publication(8, "number_of_publication_year_8")
publication(9, "number_of_publication_year_9")
publication(10, "number_of_publication_year_10")
publication(11, "number_of_publication_year_11")
publication(12, "number_of_publication_year_12")
publication(13, "number_of_publication_year_13")
publication(14, "number_of_publication_year_14")
publication(15, "number_of_publication_year_15")


# Compile "number_of_publication"
import pandas as pd
def read_data(list1):
    i=1
    df = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                     "Truven_rising_stars/oncology_profile/Output_data/"
                     "number_of_publication_year_" + str(list1[0]) + ".csv")
    for item in list1:
        if i==1:
            i+=1
            pass
        else:
            df_1 = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
            "Truven_rising_stars/oncology_profile/Output_data/"
            "number_of_publication_year_" + str(item) + ".csv")
            df_1 = df_1.drop("KOL", axis = 1)
            df = pd.merge(df, df_1, on = 'HBE_ID')
    
    temp_list = list()
    # Match year_of_birth
    for i in range(len(df)):
        key = df.iloc[i,0]
        if key in year_of_birth_dict:
            temp_list.append(year_of_birth_dict[key])
        else:
            temp_list.append("NA")
    df['Birth_year'] = temp_list
      
    return df

df_1_15 = read_data(list({1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}))
df_1_15.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
          "Truven_rising_stars/oncology_profile/Output_data/"
          "number_of_publication_1_15.csv", index = False)
        

##
#'Compile accumulative number of publications for "pubs_KOL"'
##
#
#import pandas as pd
#df = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
#                 "oncology_profile/Input_data/pubs_KOL.csv", 
#                 keep_default_na = False, encoding = 'utf-8', dtype = 'object')
#
## Subset 3 columns
#df = df.iloc[:,[0,3,16]]
#
#Full_pubs_year_first_publication = dict()
#
#for i in range(len(df)):
#    key = df.iloc[i,0]
#    value = df.iloc[i,2]
#    if pd.isnull(value) == False:
#        try: 
#            if (key in Full_pubs_year_first_publication):
#                if (int(Full_pubs_year_first_publication[key]) > int(value)):
#                    Full_pubs_year_first_publication[key] = value
#            else:
#                Full_pubs_year_first_publication[key] = value
#        except:
#            continue
#
#def publication(benchmark, name):
#    temp = dict()
#    for i in range(len(df)):
#        #print(i)
#        key = df.loc[i,'HBE Universal Code']
#        value = df.loc[i, 'PMID']
#        year = df.loc[i, 'Year']
#        try: 
#            if (len(year) <= 4):
#                first_publication_year = int(Full_pubs_year_first_publication[key])
#                if ((int(year) - first_publication_year) <= benchmark):
#                    if key in temp:
#                        temp[key] += 1
#                    else:
#                        temp[key] = 1
#                else:
#                    pass 
#            else:
#                pass
#        except ValueError:
#            print("Invalid year: " + year)
#            pass
#        
#        
#    import csv
#    csv_name = "/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"\
#    "oncology_profile/Output_data/" + name + '.csv'
#    with open(csv_name, "w", encoding = 'utf-8') as csvfile:
#        column_name = "Number_of_publication_" + str(benchmark)
#        fieldnames = ['HBE_ID', column_name]
#        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
#        writer.writeheader()
#
#        for key, value in temp.items():
#            writer.writerow({'HBE_ID': key, 
#                             column_name: value})  
#    
## Accumulative number of publications
#publication(1, "KOL_number_of_publication_year_1")
#publication(2, "KOL_number_of_publication_year_2")
#publication(3, "KOL_number_of_publication_year_3")
#publication(4, "KOL_number_of_publication_year_4")
#publication(5, "KOL_number_of_publication_year_5")
#publication(6, "KOL_number_of_publication_year_6")
#publication(7, "KOL_number_of_publication_year_7")
#publication(8, "KOL_number_of_publication_year_8")
#publication(9, "KOL_number_of_publication_year_9")
#publication(10, "KOL_number_of_publication_year_10")
#publication(11, "KOL_number_of_publication_year_11")
#publication(12, "KOL_number_of_publication_year_12")
#publication(13, "KOL_number_of_publication_year_13")
#publication(14, "KOL_number_of_publication_year_14")
#publication(15, "KOL_number_of_publication_year_15")
#
#
## Compile "KOL_number_of_publication"
#import pandas as pd
#def read_data(list1):
#    i=1
#    df = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
#                     "Truven_rising_stars/oncology_profile/Output_data/"
#                     "KOL_number_of_publication_year_" + str(list1[0]) + ".csv")
#    for item in list1:
#        if i==1:
#            i+=1
#            pass
#        else:
#            df_1 = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
#            "Truven_rising_stars/oncology_profile/Output_data/"
#            "KOL_number_of_publication_year_" + str(item) + ".csv")
#            df = pd.merge(df, df_1, on = 'HBE_ID')
#    return df
#
#df = read_data(list({1,2,3,4,5,6,7,8,9,10,11,12,13,14,15}))
#df.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
#          "Truven_rising_stars/oncology_profile/Output_data/"
#          "KOL_number_of_publication_1_15.csv", index = False)
#
## Conclusion: new "Oncology Profiles - Full pubs" data consists of KOL and nonKOL


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
   
