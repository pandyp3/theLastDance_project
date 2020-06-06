# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:00:53 2020

@author: Parth
"""
import pandas as pd

import re
import string


def players():

    playercsv = pd.read_csv(r"C:\Users\Parth\Documents\Python Scripts\player_names.csv")
    
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

def cleanup_tweets():
    
    #We're going to refer back to the main tweet csv and clean it up
    temp = pd.read_csv(r"C:\Users\Parth\Documents\Python Scripts\tweet_data_May24_May31.csv")
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