#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:27:20 2017

@author: yuchenli

@content: 
    statistical analysis of 
        Profile_Trials_Local
        Profile_Trials_Standard
        Profile_Press
        Profile_Sanctions
        Profile_Payments
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

trails = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen project/"
                     "Truven - rising stars/statistical analysis/"
                     "Profile_Trials_Standard.csv")
sanctions = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen project/"
                        "Truven - rising stars/statistical analysis/"
                        "Profile_Sanctions.csv")
press = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen project/"
                    "Truven - rising stars/statistical analysis/"
                    "Profile_Press.csv")
payment = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen project/"
                      "Truven - rising stars/statistical analysis/"
                      "Profile_Payments.csv")
trails.dtypes

# Trails:
sns.countplot(y = "Role", data = trails, 
              order = trails.Role.value_counts().iloc[:5].index)
#sns.countplot(y = "", data = trails)

# Sanctions:
sns.countplot(y = "PS_Category", data = sanctions)

# Press:
sns.countplot(y = 'Source', data = press,
              order = press.Source.value_counts().iloc[:15].index)

# Payment:
payment.dtypes
sns.countplot(y = 'PPAY_Category', data = payment, 
              order = payment.PPAY_Category.value_counts().iloc[:15].index)

# Replace dollar sign and comma
payment.PPAY_Amount = payment.PPAY_Amount.str.replace('$','')
payment.PPAY_Amount = payment.PPAY_Amount.str.replace(',','')
payment.PPAY_Amount = pd.to_numeric(payment.PPAY_Amount)
Company_amount_sum = payment.groupby("PPAY_Company",as_index=False).sum(\
                                    numeric_only = None)

sns.countplot(y = 'PPAY_Company', data = payment, 
              order = payment.PPAY_Company.value_counts().iloc[:30].index)

