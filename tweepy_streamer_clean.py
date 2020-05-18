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

###Create df to contain player names and variations of name (nickname, handle etc.)
def players(playerNameFile):

    playercsv = pd.read_csv(playerNameFile)
    
    playerdf = pd.DataFrame(playercsv)
    
    """
    We need to turn the Permutations into a list of strings so we can do a
    comparison between it and the tweet
    """
    permutationList = []
    for index, row in playerdf.iterrows():
        val = row['Permutations']
        pl = list(val.split(','))
        permutationList.append(pl)
    
    playerdf['Permutation List'] = permutationList
        
    # print(playerdf)
            
    return playerdf

# players()

def cleanup_tweets(tweetFile):
    #We're going to refer back to the main tweet csv and clean it up
    temp = pd.read_csv(tweetFile)
    df = pd.DataFrame(temp)
    """
    remove the non-pertinent data from the tweet
    1. Remove the URL information
    2. Remove the HTML elements
    """
    #Remove mentions
    df['Cleaned Tweet'] = df['Tweet'].str.replace(r'@\S+', '')
    cleanedTweetList = []
    for index, row in df.iterrows():
        f = row['Cleaned Tweet']
        #remove urls
        g = re.sub(r'https?:\/\/t.c?o?\/\S+', '', str(f))
        #keep only ASCII characters
        printable = set(string.printable)
        h = ''.join(filter(lambda x: x in printable, g))
        #fix the ampersand issue
        i = re.sub(r'&amp;', '', h)
        #remove all hashtags
        j = re.sub(r'#\S+', '', i)
        #turn tweet into list of strings to iterate through
        k = re.sub(r'[^\w]', ' ', j).split()
        l = list(k)
        cleanedTweetList.append(l)
    
    # print(df.head())
    df['Cleaned Tweet'] = cleanedTweetList
    #remove the erroneous column that is the index of the previous df
    df = df.drop([0])
 
    # if not os.path.exists(r"C:\\Users\\Parth\\Documents\\Python Scripts\\tweets.csv"):
    #     df.to_csv(r"C:\\Users\\Parth\\Documents\\Python Scripts\\tweetDataCleaned.csv")
    # else:
    #     print('Already exists')
    
    return df
    
    
# cleanup_tweets()

def match_player_to_tweet():
    df = cleanup_tweets()
    playerdf = players()
    
    pmlCol = []
    for index, row in df.iterrows():
        m = row['Cleaned Tweet']
        playerMentionList = []
        for index, row in playerdf.iterrows():
            n = row['Name']
            o = row['Permutation List']
            p = list(set(m) & set(o))
            if p:
                playerMentionList.append(n)
            # check = any(item in o for item in m)
            # if check is True:
                # playerMentionList.append(n)
        pmlCol.append(list(playerMentionList))
    
    df['Players Mentioned'] = pmlCol
    
    return df
    
    # if not os.path.exists(r"C:\\Users\\Parth\\Documents\\Python Scripts\\tweetDataCleaned.csv"):
    #     df.to_csv(r"C:\\Users\\Parth\\Documents\\Python Scripts\\tweetDataCleaned.csv")
    # else:
    #     print('Already exists')

# match_player_to_tweet()

def count_player_mention():
    """
    Create a new dataframe that contains the player names as lists of
    strings eg. ['Michael Jordan']
    For each name, iterate through the Players Mentioned column in the
    main df and perform a count
    Create a counter object and, from that, a dataframe
    """
    playerdf = players()
    df = match_player_to_tweet()
    
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
        
