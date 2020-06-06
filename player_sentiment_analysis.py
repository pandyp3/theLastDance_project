# -*- coding: utf-8 -*-
"""
Created on Thu May  7 23:53:58 2020

@author: Parth
"""
import pandas as pd

import re
import string
import matplotlib.pyplot as plt
import seaborn as sns

import tweet_preprocessing


###Create df to contain player names and variations of name (nickname, handle etc.)
        
def determine_score(corpus_file_path):
    
    df = tweet_preprocessing.match_player_to_tweet()

    #start by creating a df of the words and scores
    #I leveraged a corpus of sentiment-driving terms
    word_file = open(corpus_file_path)
    words_scores = pd.read_csv(word_file, sep='\t', names=['Word', 'Score'])
    word_scores_df = pd.DataFrame(words_scores)
    
    #turn the tweets into lists of strings
    
    score_list = []
    for index, row in df.iterrows():
        base_score = 0
        master_list = row['Cleaned Tweet']
        for index, row in word_scores_df.iterrows():
            if str(row['Word']) in master_list:
                base_score = base_score + row['Score']
        score_list.append(base_score)
    
    df['Score'] = score_list

    newClass = []    
    for index, row in df.iterrows():  
        if row['Score'] < 0:
                newClassValue = 0
        elif row['Score'] > 0:
                newClassValue = 4
        else:
            newClassValue = 'NA'
        newClass.append(newClassValue)
        
    df['New Class'] = newClass
    
    # df_scores = df[['Players Mentioned', 'Score', 'New Class']].copy()
    
    return df
    
    # df.to_csv(r"C:\\Users\\Parth\\Documents\\Python Scripts\\tweetDataCleaned.csv")
    
# determine_score()

def calculate_average_player_score(tweetDataCleaned):

    #Refer to df created in tweet_preprocessing.py
    #NOTE: Constantly fetching and processing the dataframe results in latency
    #to speed up processing, i saved the df output from match_player_to_tweet() to csv so it only needs to be created once
    #you optionally can refer to the df instead of performing a read_csv on the output...
    scorecsv = pd.read_csv(tweetDataCleaned)
    
    #Remove the timestamp from the created date
    scorecsv['Created Date'] = pd.to_datetime(scorecsv['Created Date']).dt.date
    
    #create dataframe grouping player mentions, calculating average score
    tempAvgScores = scorecsv.groupby(['Players Mentioned', 'Created Date'])['Score'].mean()
    
    #output to csv
    
    df_scores = pd.DataFrame(tempAvgScores)
    df_scores = df_scores.reset_index()
    # remove Player Mentions with 2 or more names listed, remove blanks
    for index, row in df_scores.iterrows():
        playerName = row['Players Mentioned']
        if "," in playerName:
            df_scores = df_scores.drop([index]) 
        elif "[]" in playerName:
            df_scores = df_scores.drop([index])
    
    # print(df_scores)
            
    return df_scores
            
    #If we want to graph this over multiple dates, we will need to keep the Created Date, and transform it into just a date

# calculate_average_player_score()

def plot_dataframe():
    
    df_scores = calculate_average_player_score()
    
    df_scores['Players Mentioned'] = df_scores['Players Mentioned'].map(lambda x: x.lstrip("['").rstrip("']"))
       
    ax = sns.lineplot(x='Created Date', y='Score', hue='Players Mentioned', data=df_scores).set_title('Player Sentiment Scoring from Twitter #theLastDance')
    plt.show()
    
    # plt.style.use('seaborn-darkgrid')
    # palette = plt.get_cmap('Set1')
    
plot_dataframe()
    
