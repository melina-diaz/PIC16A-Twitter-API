# PIC16A-Twitter-API
Made by Melina Diaz, Tracy Charles, Michelle Pang

Goals:
- Using the Twitter API, make a dataframe of tweets about UCLA
- Do cool stuff like sentiment analysis, clustering, etc. on the dataframe


Use `curl -H "Authorization: Bearer BEARER TOKEN" URL` in command line

URL examples are:
- https://api.twitter.com/2/tweets/search/recent?query=from:ucla returns the 10 most recent tweets (id, text) from UCLA


We need to figure out:
- How to call other things (look at sample code)
- How to turn json to csv
- How to turn the return of ^function above into a saveable form of data
