#*****The following code is from https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a*****

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
    '''Purpose: Helps make make_call() run.
    Arguments: bearer_token: Your bearer token for Twitter's API
    Return: format of bearer token used for make_call()'''
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, start_date, end_date, max_results = 100):
    '''Purpose: Helps make make_call() run by getting the endpoint url and specifying parameters, which can be modified in this function
    Arguments: keyword: string of what to search for. It has the ability to specify word/user/place of tweet
               start_time, end_time: This doesn't affect results as far as I can tell, probably because we are using recent endpoint instead of all
               max_result: the amount of results to return in one API call, max at 100.
    Return: URL and parameters that the Twitter API searches for'''
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
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    '''Purpose: Helps make make_call() by calling the API and making the JSON
    Arguments: url: the endpoint URL returned by create_url()
               headers: the format of the bearer token made by create_headers()
               params: parameters of the call, returned by create_url()
               next_token: since only 100 calls can be returned in one API call, you can pick up from where you left off and access the remaining results with a next token
    Returns: JSON of results that fulfills url, headers, params and next_token. The JSON separates the tweets (data), users, places, and metadata.
    '''
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#***** End of unoriginal code****** 

def make_call(bearer_token, keyword="ucla -is:retweet lang:en", max_results = 100, filename="uclatweets"):
    '''
    Purpose: Calls the appropriate functions to turn the tweet data string from the API into a JSON, which is then converted into a CSV file on your computer. This function is customizable, you can change the amount of tweets returned, the keyword, the name of the JSON and CSV. Since we are using the recent endpoint, the CSV will only include tweets from the last 7 days.
    
    Arguments:
        bearer_token: the token from your Twitter API Developer account to use the API
        keyword: the criteria of the tweet/user/geo/etc you want to see. operators you can use https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query 'ucla -is:retweet lang:en' looks for tweets (not retweets) in english that have the substring ucla
        max_results: int of how many tweets you want returned. Has to be > 10. For > 100, will call API multiple times. If max_results > number of tweets available within the last week, then only the available tweets will be called
        filename: A string for what you want to name the outputted JSON and CSV files. If JSON and CSV files already exist with filename, they will be overwritten
        
    Return:
        Prints Twitter's endpoint codes. 200 if works properly, not 200 otherwise.
        Makes "filename".json, the uncleaned most recent output (with max_results mod 100 tweets) of the Twitter API
        makes "filename".csv, the cleaned output with max_results amount of tweets along with their users and attributes        
        
    '''
    #since we can only get 100 results at most at once, we have to put call them in batches
    if (max_results>100):
        curr_max_results=100
    else:
        curr_max_results=max_results
        
    #calls the appropriate functions to get tweet data
    headers = create_headers(bearer_token) 
    url = create_url(keyword, "2022-02-01T00:00:00.000Z", "2022-02-28T00:00:00.000Z", curr_max_results) 
    json_response = connect_to_endpoint(url[0], headers, url[1]) 
    
    # turn tweet data into a JSON file on your computer
    with open(filename+".json", 'w') as outfile:
        json.dump(json_response, outfile)
    file = json.load(open(filename+".json"))
    
    #extracts the tweet and user data from JSON and turn into dfs. 
    tweets = pd.DataFrame(file["data"])
    users = pd.DataFrame(file["includes"]["users"])        
        
    #clean dfs to extract public metrics and merge
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
    
    #save df as a CSV on your computer
    df.to_csv(filename+".csv")
    
    #I didn't want to do this part recursively, but it basically does the exact same thing as before, but 
    #takes in a next_token and decrements the max_results by 100
    while (max_results - 100 > 0):
        max_results = max_results - 100
        
        #if next_token doesn't exist, then stop the while loop. This will happen if you put max_results>100, but only <100 tweets exists
        try:
            file["meta"]["next_token"]
        except KeyError:
            break
        next_token = file["meta"]["next_token"]
        
        #limits the number of calls at once to be in [10, 100] because that's what the API is capable of
        if (max_results>100):
            curr_max_results=100
        elif(max_results<10):
            curr_max_results=10
        else:
            curr_max_results=max_results
        
        #already explained above
        headers = create_headers(bearer_token)
        url = create_url(keyword, "2022-02-01T00:00:00.000Z", "2022-02-28T00:00:00.000Z", curr_max_results)
        json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
        with open(filename+".json", 'w') as outfile:
            json.dump(json_response, outfile)
        file = json.load(open(filename+".json"))
        tweets = pd.DataFrame(file["data"])
        users = pd.DataFrame(file["includes"]["users"])
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
        
        #appends the current df to the previously saved df from the CSV and saves it to the CSV, essentially updating CSV with current df
        last=pd.read_csv(filename+".csv")
        last=last.drop(columns=["Unnamed: 0"])
        df=pd.concat([last, df], axis=0)
        df.to_csv(filename+".csv")
    
