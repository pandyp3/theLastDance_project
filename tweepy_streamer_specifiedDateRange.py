# -*- coding: utf-8 -*-
"""
Created on Sun May 10 14:22:54 2020

@author: Parth
"""

from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
import numpy as np
import pandas as pd
import csv
import os
import html
import re


import twitter_credentials
####input your credentials here

auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = API(auth,wait_on_rate_limit=True)

def get_tweets():

    df = pd.DataFrame(columns=['id', 'Created Date', 'Tweet'])
    idList = []
    dateList = []
    tweetList = []
    for tweet in Cursor(api.search,q="#thelastDance",count=100, lang="en", since="2020-05-24", until="2020-05-31").items(10000):
        idList.append(tweet.id)
        dateList.append(tweet.created_at)
        tweetList.append(tweet.text)
    
    df['id'] = idList    
    df['Created Date'] = dateList
    df['Tweet'] = tweetList
    
    df.to_csv(r"C:\Users\Parth\Documents\Python Scripts\tweet_data_May1_May2.csv")
    
get_tweets()