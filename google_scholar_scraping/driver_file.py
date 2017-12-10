#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 21:45:32 2017

@author: yanglinli
"""

from scholar import SearchScholarQuery,ScholarQuerier,ScholarSettings,ScholarConf
import pandas as pd
from time import sleep
from random import randint
import csv

ScholarConf.COOKIE_JAR_FILE = 'cookies.txt'
min_sleep_time_sec = 5
max_sleep_time_sec = 10

df = pd.read_csv("../data_seperate_sheet/Profile_Publications_Standard.csv")

#cites =[]
#citation_list = [] # [year of pub]

with open('citations_counts_25307.csv', "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for k,v in df['Article Title'][25307:].iteritems(): 
        # why is df['Article Title'] of type dict??
        
        querier = ScholarQuerier()
        settings = ScholarSettings()
        settings.set_citation_format(ScholarSettings.CITFORM_BIBTEX)
        querier.apply_settings(settings)
        query = SearchScholarQuery()
        query.set_phrase(v)
        query.set_scope(True)
        querier.send_query(query)
        if querier.articles:
            cites=querier.articles[0].__getitem__('num_citations')
            citation_list=querier.articles[0].__getitem__('url_citations')
        else:
            cites=0
            citation_list= ""
            
    #    json_results = []
    #    file_name = 'query_data/cites_for_article_'+str(k+1)+'.json'
    #    for art in querier.articles:
    #        json_results.append(
    #            {key: art.attrs[key][0] for key in art.attrs.keys()})
    #    with open(file_name, 'wb') as f:
    #        json.dump(json_results, f)
        print('{} iter *** {} cited'.format(k+1,cites))
        writer.writerow([cites,citation_list])
        querier.save_cookies()
        sleep(randint(min_sleep_time_sec, max_sleep_time_sec))



