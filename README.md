# PIC16A-Twitter-API
Made by Melina Diaz, Tracy Charles, Michelle Pang

**What's happening?**
- Using the Twitter API, we made a dataframe of tweets about UCLA. With this dataframe, we can do cool stuff like sentiment analysis, clustering, etc.


**Files:**
3. Although we provided a `making_dataframe.py` makes the JSON and CSV files that are necessary to make the dataframe. You don't need this, since we supplied a CSV file, but if you want to modify the CSV file to look for different keywords, include different features, this is how you would do it. Run make_call(bearer_token, ...)


1. **Project name:** UCLA's Twitter API Project
2. **Names of group members (if you don’t want to for privacy, add usernames):** Melina Diaz, Tracy Charles, Michelle Pang
3. **Short description of the project:** Using the Twitter API, we made a dataframe of tweets about UCLA and made inferences about the tweets using clusters and sentiment analysis to determine what is currently trending around UCLA and if the general consensus are positive or negative. Additionally, the Twitter API allows us to extract more details about the original tweet such as the number of retweets, followers and likes which hints to the credibility and influence of the tweet.
4. **Instructions on how to install the package requirements.** Firstly, download the code, use `conda create --name NEWENV --file requirements.txt` to download packages used in 'making_dataframe.py' and 'analysis.py' files. Then, open the 'demo.ipynb' file and run all codes to generate the results as shown in the next point. 
5. **Detailed description of the demo file (how to run it, what output one should expect to see, and explanations of result):** `demo.ipynb` is the end-to-end demo.
6. **Scope and limitations, including ethical implications, accessibility concerns, and ideas for potential extensions:** Although this package is publicly available, users who wish to access the tweets will require a Bearer Token that can be created through the Twitter API developer portal. Some possible extensions include any topic that preferably has a lot of public consensus such as public figures, politics, weather conditions etc.
7. **License and terms of use (probably MIT license)**.
8. **References and acknowledgement:** Twitter API developer platform
9. **Background and source of the dataset:** We generated this dataset, which consists of the most recent tweets about UCLA
10. **Links to any tutorials you used, and at least 3 specific things you implemented that differentiates your project from what’s already in the tutorial:**
- https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a This tutorial shoed how to collect tweets with Twitter's API and form a dataframe, but we didn't like the way the user had to run the functions individually, so we consolidated the function calls. We also didn't like the columns included, so we rewrote how the JSON is turned into a cleaned CSV. We also had to change the keywords and parameters to make the dataframe UCLA-specific, which we learned from https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
