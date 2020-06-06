# theLastDance_project
A simple Twitter data project that looks for mentions in tweets using the hashtag #theLastDance

create_tweet_csv.py
- For ease of analysis, Twitter data is pulled and stored to avoid excessive requests to the Twitter API endpoint
- The number of tweets returned and stored can be configured directly when the api.search method is called (in the example I've specified 1000)
- I've imported the credential file which contains the OAuth information required

***(2020-06-06)The file has been updated to search for a defined created date interval, and fetch more tweets***

analyze_twitter_data.py
- Based on player_names.csv file format, I've created a dataframe with player names and permutations of names to search. New player searches can be added to this csv file
- Using basic regex I've cleaned the Twitter data to allow for comparison between the permutations and tweets and produced a count for the number of player mentions over the sample data
> Note: Each tweet is one count - if a player is referred to several times in a single Tweet, it is still considered one "mention"

player_names.csv
- Contains the format for players and name permutations to search

player_sentiment_analysis.py
- 
