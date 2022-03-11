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


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, start_date, end_date, max_results = 100):
    
    search_url = "https://api.twitter.com/2/tweets/search/recent" #Change to the endpoint you want to collect data from

#CHANGE THIS PART TO DISPLAY DIFFERENT VALUES
    query_params = {'query': keyword,
                    'max_results': max_results,
                    'expansions': 'author_id,geo.place_id', #'author_id,in_reply_to_user_id,geo.place_id', expansions controls which of the below fields you want to see
                    'tweet.fields': 'text,public_metrics,referenced_tweets,geo,created_at', #'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'name,username,created_at,description,public_metrics,verified', #'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,country,country_code,geo,name,place_type', #'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def make_call(bearer_token, keyword="ucla -is:retweet lang:en", start_time = "2022-02-01T00:00:00.000Z", end_time = "2022-02-28T00:00:00.000Z", max_results = 100):
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
    tweets["retweet_count"] = tweets["public_metrics"].map(lambda x:x["retweet_count"])
    tweets["reply_count"] = tweets["public_metrics"].map(lambda x:x["reply_count"])
    tweets["like_count"] = tweets["public_metrics"].map(lambda x:x["like_count"])
    df=pd.merge(tweets,users, on="author_id")
    df.to_csv('uclatweets.csv')
    
#make_call('')
#how to run this in the command line....
