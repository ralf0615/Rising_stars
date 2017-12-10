#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 7 21:01:12 2017

@author: cheng-xili

Modified on 2017-09-14 13:40:31

@author: Yuchen Li
"""

from __future__ import print_function

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import statistics

print(__doc__)

# Process trials_count_3_4
'''
trials_count = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                           "Truven_rising_stars/k_means/trials_count_3_4.csv", 
                           na_values =[ 'NA','?'])
df = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars"
                 "/k_means/features.csv", na_values =[ 'NA','?'])

trials_count_dict = dict()
for i in range(len(trials_count)):
    key = trials_count.loc[i,'HBE_ID']
    value = trials_count.loc[i,'trials_count']
    trials_count_dict[key] = value
    
trials_count_3_4 = list()
for i in range(len(df)):
    key = df.loc[i,'ID']
    try:
        trials_count_3_4.append(trials_count_dict[key])
    except:
        trials_count_3_4.append(0)
        
df['trials_count_3_4'] = trials_count_3_4 # add trails_count_phase_3_4

df.to_csv("/Users/yuchenli/Box Sync/Yuchen_project/Truven_rising_stars/"
          "/k_means/features_1.csv", encoding = 'utf-8')
'''
     
# Standardization
df_1 = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
                           "Truven_rising_stars/k_means/features_1.csv", 
                           na_values =[ 'NA','?'])
def stand(df, column):
    list_temp = list(df[column])
    list_temp_2 = list()
    average = statistics.mean(list_temp)
    standard_deviation = statistics.stdev(list_temp)
    for element in list_temp:
        list_temp_2.append((element - average)/standard_deviation)
    name = str(column) + '_std'
    df[name] = list_temp_2
    return df

stand(df_1, 'SJR_score')
stand(df_1, 'trials_count_3_4')


# Generating the sample data from make_blobs
# This particular setting has one distinct cluster and 3 clusters placed close
# together.

"""
X, y = make_blobs(n_samples=500,
                  n_features=2,
                  centers=4,
                  cluster_std=1,
                  center_box=(-10.0, 10.0),
                  shuffle=True,
                  random_state=1)  # For reproducibility
"""

#X = df[['score','press_count','event_count']]
def km_train(df, column_names, number_of_clusters):
    X = df[column_names]
    #X = df[['score']]
    #range_n_clusters = [2, 3, 4, 5, 6, 7, 8, 9]
    range_n_clusters = [number_of_clusters]

    for n_clusters in range_n_clusters:    

        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        clusterer = KMeans(n_clusters = n_clusters)
        cluster_labels = clusterer.fit_predict(X)
    
        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)

        # Compute the silhouette scores for each sample
        #sample_silhouette_values = silhouette_samples(X, cluster_labels)

    #y = df[['KOL']]
    # Test the majority category, minority are always KOL
    """
    if (sum(list(cluster_labels)) >= len(list(cluster_labels))/2):
        predict = pd.DataFrame({"Predict": 1-cluster_labels})
    else:
        predict = pd.DataFrame({"Predict": cluster_labels})
        
    df['Predict'] = predict.Predict
    
    accuracy = {'True_Negative':[], 'False_Positive':[], 'True_Positive':[], 
                'False_Negative':[]}
    for i in range(len(df)):
        if (df.loc[i,'KOL'] == 1 and df.loc[i,'Predict'] == 1):
            accuracy['True_Positive'].append(df.loc[i,'ID'])
        elif (df.loc[i,'KOL'] == 1 and df.loc[i,'Predict'] == 0):
            accuracy['False_Negative'].append(df.loc[i,'ID'])
        elif (df.loc[i,'KOL'] == 0 and df.loc[i,'Predict'] == 1):
            accuracy['False_Positive'].append(df.loc[i,'ID']) 
        else:
            accuracy['True_Negative'].append(df.loc[i,'ID'])
    
    return accuracy
    """
    predict = pd.DataFrame({"Predict": cluster_labels})
    df['Predict'] = predict.Predict
    return df

# Testing
'''
SJR_alone = km_train(['SJR_score'])
SJR_event = km_train(['SJR_score', 'event_count'])
SJR_trials = km_train(['SJR_score', 'trials_count'])
SJR_trials_press = km_train(['SJR_score', 'trials_count', 'press_count'])
SJR_trials_press_event = km_train(['SJR_score', 'trials_count', 'press_count',
                                   'event_count'])
trials_alone = km_train(['trials_count'])
press_alone = km_train(['press_count'])   
index_alone = km_train(['index'])
funding_total_amount = km_train(['funding_total_amount'])
'''
km_3 = km_train(df_1, ['SJR_score_std', 'trials_count_3_4_std'], 3)


# Plot km_3
plt.figure(figsize=(14,7))
colormap = np.array(['red', 'lime', 'black', 'brown'])

# Plot the original classifications
plt.subplot(1, 2, 1)
plt.scatter(km_3.SJR_score_std, km_3.trials_count_3_4_std, 
            c = colormap[km_3.KOL], s = 40)
plt.title('Original Classification')
plt.xlabel('SJR_score')
plt.ylabel("Trials_count")

# Plot the models classifications
km_3_color = np.choose(km_3.Predict, [0,1,2]).astype(np.int64)
plt.subplot(1, 2, 2)
plt.scatter(km_3.SJR_score_std, km_3.trials_count_3_4_std, 
            c = colormap[km_3_color], s = 40)
plt.title('K Mean Classification with k = 3')
plt.xlabel('SJR_score')
plt.ylabel("Trials_count")

# Plot km_4
km_4 = km_train(df_1, ['SJR_score_std', 'trials_count_3_4_std'], 4)

plt.figure(figsize=(14,7))

# Plot the original classifications
plt.subplot(1, 2, 1)
plt.scatter(km_4.SJR_score_std, km_4.trials_count_3_4_std, 
            c = colormap[km_4.KOL], s = 40)
plt.title('Original Classification')
plt.xlabel('SJR_score')
plt.ylabel("Trials_count")

# Plot the models classifications
km_4_color = np.choose(km_4.Predict, [0,1,2,3]).astype(np.int64)
plt.subplot(1, 2, 2)
plt.scatter(km_4.SJR_score_std, km_4.trials_count_3_4_std, 
            c = colormap[km_4_color], s = 40)
plt.title('K Mean Classification with k = 4')
plt.xlabel('SJR_score')
plt.ylabel("Trials_count")

# Plot km_2
km_2 = km_train(df_1, ['SJR_score_std', 'trials_count_3_4_std'], 2)

plt.figure(figsize=(14,7))

# Plot the original classifications
plt.subplot(1, 2, 1)
plt.scatter(km_2.SJR_score_std, km_2.trials_count_3_4_std, 
            c = colormap[km_2.KOL], s = 40)
plt.title('Original Classification')
plt.xlabel('SJR_score')
plt.ylabel("Trials_count")

# Plot the models classifications
km_2_color = np.choose(km_2.Predict, [0,1,2,3]).astype(np.int64)
plt.subplot(1, 2, 2)
plt.scatter(km_2.SJR_score_std, km_2.trials_count_3_4_std, 
            c = colormap[km_2_color], s = 40)
plt.title('K Mean Classification with k = 2')
plt.xlabel('SJR_score')
plt.ylabel("Trials_count")