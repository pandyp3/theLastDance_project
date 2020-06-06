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


###Create df to contain player names and variations of name (nickname, handle etc.)
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
        
def determine_score():
    
    df = match_player_to_tweet()

    #start by creating a df of the words and scores
    word_file = open(r"C:\\Users\\Parth\\Documents\\Learning\\NLP Project\\corpus.txt")
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

def calculate_average_player_score():

    scorecsv = pd.read_csv(r"C:\Users\Parth\Documents\Python Scripts\tweetDataCleaned.csv")
    
    #Remove the timestamp from the created date
    scorecsv['Created Date'] = pd.to_datetime(scorecsv['Created Date']).dt.date
    
    #create dataframe grouping player mentions, calculating average score
    tempAvgScores = scorecsv.groupby(['Players Mentioned', 'Created Date'])['Score'].mean()
    
    # print(tempAvgScores)
    
    # tempAvgScores.to_csv(r"C:\\Users\\Parth\\Documents\\Python Scripts\\tweetDataCleanedScoresGroup.csv")
    
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
    
    # df_scores.to_csv(r"C:\\Users\\Parth\\Documents\\Python Scripts\\tweetDataCleanedScoresGroup.csv")
            
    #If we want to graph this over multiple dates, we will need to keep the Created Date, and transform it into just a date

# calculate_average_player_score()

def plot_dataframe():
    
    df_scores = calculate_average_player_score()
    
    df_scores['Players Mentioned'] = df_scores['Players Mentioned'].map(lambda x: x.lstrip("['").rstrip("']"))
 
    # create new dataframes segregating players into different dfs
    # df_scores.sort_values(by='Players Mentioned', axis=1, inplace=True)
    # df_scores.set_index(keys=['Players Mentioned'], drop=False, inplace=True)
    # name=df_scores['Players Mentioned'].unique().tolist()
       
    ax = sns.lineplot(x='Created Date', y='Score', hue='Players Mentioned', data=df_scores).set_title('Player Sentiment Scoring from Twitter #theLastDance')
    plt.show()
    
    # plt.style.use('seaborn-darkgrid')
    # palette = plt.get_cmap('Set1')
    
plot_dataframe()
    
