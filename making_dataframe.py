# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time

#*****The following code is from https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a*****
def create_headers(bearer_token):
    '''docstring'''
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, start_date, end_date, max_results = 100):
    '''docstring'''
    search_url = "https://api.twitter.com/2/tweets/search/recent" #Change to the endpoint you want to collect data from

#*****CHANGE THIS PART TO DISPLAY DIFFERENT VALUES. Next to each field is all possible options******
    query_params = {'query': keyword,
                    'max_results': max_results,
                    # expansions is if you want the author, geo, etc. attributes included below to show up in the JSON
                    'expansions': 'author_id,geo.place_id', #'author_id,in_reply_to_user_id,geo.place_id'
                    # attributes of the tweets
                    'tweet.fields': 'text,public_metrics,referenced_tweets,geo,created_at', #'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    # attributes of the users
                    'user.fields': 'name,username,created_at,description,public_metrics,verified', #'id,name,username,created_at,description,public_metrics,verified',
                    # attributes of the places
                    'place.fields': 'full_name,country,country_code,geo,name,place_type', #'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}} #if you have a next_token put it here
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    '''docstring'''
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#***** End of unoriginal code****** 



def make_call(bearer_token, keyword="ucla -is:retweet lang:en", start_time = "2022-02-01T00:00:00.000Z", end_time = "2022-02-28T00:00:00.000Z", max_results = 100):
    '''
    Purpose: Calls the appropriate functions to turn the tweet data string from the API into 
    a JSON, which is then converted into a CSV file on computer
    csv and json file can't already exist
    
    Arguments:
        bearer_token: the token from your Twitter API Developer account to use your API
        keyword: the criteria that the tweet/user/geo/etc needs to fulfill in order to be returned. operators you can use https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query Default looks for tweets (not retweets) in english that have the substring ucla
        start_time, end_time: I honestly don't know what this does, doesn't affect results as far as I can tell, probably because we are using recent endpoint instead of all
        max_results: tweets returned, int [10, 100]
        
    Return:
        prints Twitter's endpoint code. 200 if works properly, not 200 otherwise.
        makes uclajson.json, the uncleaned output of the Twitter API in the same folder as this file
        makes uclatweets.csv, the cleaned output with twitters, users and their attributes        
        
    '''
    headers = create_headers(bearer_token)
    url = create_url(keyword, start_time,end_time, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1])
    with open('uclajson.json', 'w') as outfile:
        json.dump(json_response, outfile)
    file = json.load(open(r'uclajson.json'))
    tweets = pd.DataFrame(file["data"])
    users = pd.DataFrame(file["includes"]["users"])
    places = pd.DataFrame(file["includes"]["places"])
    users["author_id"]=users["id"]
    tweets["retweet_count_x"] = tweets["public_metrics"].map(lambda x:x["retweet_count"])
    tweets["reply_count_x"] = tweets["public_metrics"].map(lambda x:x["reply_count"])
    tweets["like_count_x"] = tweets["public_metrics"].map(lambda x:x["like_count"])
    users["followers_count_y"] = users["public_metrics"].map(lambda x:x["followers_count"])
    users["following_count_y"] = users["public_metrics"].map(lambda x:x["following_count"])
    users["tweet_count_y"] = users["public_metrics"].map(lambda x:x["tweet_count"])
    users["listed_count_y"] = users["public_metrics"].map(lambda x:x["listed_count"])
    df=pd.merge(tweets,users, on="author_id")
    df=df.drop(columns=["public_metrics_x", "author_id", "public_metrics_y"])
    df.to_csv('uclatweets.csv')
    