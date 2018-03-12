#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:06:48 2018

@author: yuchenli
@content: compile accumulative number of publication for each physician
@note: replace xxxxxx with your own directory
"""

# Import packages
import pandas as pd

# Read KOL roster, pubs_KOL is the product of combining:
#    TOP_ONCOLOGY_Existing_Data_pt1
#    TOP_ONCOLOGY_Existing_Data_pt2
#    TOP_ONCOLOGY_Existing_Data_pt3
#    TOP_ONCOLOGY_Existing_Data_pt4
KOL_roster = pd.read_csv("xxxxxx/pubs_KOL.csv", keep_default_na = False, 
                         encoding = 'utf-8', dtype = 'object')

# Compile a list of KOL such that KOL can be marked among a group of physicians
KOL_roster_list = set(list(KOL_roster['HBE Universal Code']))


# Import "Oncology_profile_year_of_birth.csv"
year_of_birth = pd.read_csv("xxxxxx/Oncology_profile_year_of_birth.csv", 
                            keep_default_na = False, 
                            encoding = 'utf-8', dtype = 'object')

# Convert "year_of_birth" into "year_of_birth_dict", a dictionary containing
# "HBE_ID" as key and "year_of_birth" as value
year_of_birth_dict = dict()
for i in range(len(year_of_birth)):
    key = year_of_birth.loc[i,"HBE_ID"]
    value = int(year_of_birth.loc[i,"Year_of_birth"])
    year_of_birth_dict[key] = value
    


# Compile accumulative number of publications for "Full_pubs_with_year", product
# of running "convert_publication_date.py"
# Import "Full_pubs_with_year.csv"
df = pd.read_csv("xxxxxx/Full_pubs_with_year.csv", 
                 keep_default_na = False, encoding = 'utf-8', dtype = 'object')


    
# Make a copy of df as df_1 with less columns
df_1 = df.loc[:,["HBE Universal Code", "PMID", "Year"]]


# Construct a dictionary named Full_pubs_year_first_publication
# @key: "HBE_ID"
# @value: first year of publication
Full_pubs_year_first_publication = dict()
for i in range(len(df_1)):
    key = df_1.loc[i,"HBE Universal Code"]
    value = df_1.loc[i,"Year"]
    if pd.isnull(value) == False:
        try: 
            if (key in Full_pubs_year_first_publication):
                if (int(Full_pubs_year_first_publication[key]) > int(value)):
                    Full_pubs_year_first_publication[key] = value
            else:
                Full_pubs_year_first_publication[key] = value
        except:
            continue


# Define publication function that generate accumulative number of publication
# since first year of publication
# @input: benchmark: x year since first year of publication
#         name: the name of the csv file that is written to your directory
# @output: save accumulative number of publication as csv to your directory
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
    csv_name = "xxxxxxx/" + name + '.csv'
    with open(csv_name, "w", encoding = 'utf-8') as csvfile:
        column_name = "Number_of_publication_" + str(benchmark)
        fieldnames = ['HBE_ID', column_name, 'KOL']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        for key, value in temp.items():
            writer.writerow({'HBE_ID': key, 
                             column_name: value['Count'],
                             'KOL': value['KOL']})
    print(name + ".csv saved!")
    
# Generate first 15 years of accumulative number of publication
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


# Combine previously generated csv files into one

# Define a read_data function that import all previously generated csv files,
# combine them and return one single dataframe
# @input: make sure it is consist with the second input of the function: publication
# @output: a dataframe consisting of "HBE_ID" and first 1 to 15 years of number
#          of publication since first year of publication
def read_data(list1):
    i=1
    df = pd.read_csv("xxxxxx/number_of_publication_year_" + str(list1[0]) + ".csv")
    for item in list1:
        if i==1:
            i+=1
            pass
        else:
            df_1 = pd.read_csv("xxxxxx/number_of_publication_year_" + str(item) + ".csv")
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
df_1_15.to_csv("xxxxxx/number_of_publication_1_15.csv", index = False)
