#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 10:35:42 2018

@author: yuchenli
@content: convert "Publication Date" in Oncology Profiles - Full pubs" to YYYY
          format
"""

# Import "Oncology Profiles - Full pubs.csv", name it as df
import pandas as pd
df = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                 'Rising_stars/oncology_profile/Input_data/'
                 'Oncology Profiles - Full pubs.csv', keep_default_na = False)
