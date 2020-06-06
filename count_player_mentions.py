# -*- coding: utf-8 -*-
"""
Created on Thu May  7 23:53:58 2020

@author: Parth
"""


import numpy as np
import pandas as pd
import csv
import os
import html
import re
import string

import tweet_preprocessing

def count_player_mention():
    """
    Create a new dataframe that contains the player names as lists of
    strings eg. ['Michael Jordan']
    For each name, iterate through the Players Mentioned column in the
    main df and perform a count
    Create a counter object and, from that, a dataframe
    """
    playerdf = tweet_preprocessing.players()
    df = tweet_preprocessing.match_player_to_tweet()
    
    # temp = pd.read_csv(r"C:\Users\Parth\Documents\Python Scripts\player_names.csv")
    
    # numdf = pd.DataFrame(temp)
    
    countList = []
    for index, row in playerdf.iterrows():
        counter = 0
        n = row['Name']
        # print([n])
        for index, row in df.iterrows():
            o = row['Players Mentioned']
            # print(set(o))
            # print(set([n]))
            p = list(set([n])   & set(o))
            if p:
                # print('True')
                counter += 1
        countList.append(counter)
        
        #straight assignment seems to be a problem for some reason
        #this work around, well, works
        playerdf['Count'] = pd.Series(countList)
        
    print(playerdf)
    print(countList)
    
count_player_mention()
        
