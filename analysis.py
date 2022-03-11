import pandas as pd
class Analysis:
    def __init__(self, csv_name):
        '''Makes '''
        if type(csv_name) != str:
            raise TypeError("csv_name should be a string, specifically the path to the csv of tweets")
        self.csv=csv_name
        self.df=pd.read_csv(csv_name) #you shouldn't alter the original df
        self.df=self.df.drop(columns=["Unnamed: 0"])
        
    def get_topics(self):
        '''Purpose:
        Arguments: 
        Return: '''
        from sklearn.feature_extraction.text import CountVectorizer
        vec = CountVectorizer(stop_words="english")
        counts = vec.fit_transform(self.df['text'])
        counts = counts.toarray()
        vec.get_feature_names()
        count_tweetsandusers = pd.DataFrame(counts, columns=vec.get_feature_names())
        big_count_tweetsandusers = pd.concat((self.df["text"],count_tweetsandusers), axis= 1)
        X = big_count_tweetsandusers.drop(columns = "text")
        from sklearn.decomposition import NMF
        model = NMF(n_components = 10, init="random", random_state=0)
        model.fit(X)
        import numpy as np
        def top_words(X, model, component, num_words):
            orders = np.argsort(model.components_, axis = 1)
            important_words = np.array(X.columns)[orders]
            return important_words[component][-num_words:]
        for i in range (**kwargs):
            print(top_words(X, model, i, **kwargs))
        return
    
    def get_sentiment(self):
        '''Purpose:
        Arguments: 
        Return: '''
        #Tracy's code, feel free to change whatever
        return 
    
    def predict(self):
        '''Purpose:
        Arguments: 
        Return: '''
        #Melina's code, feel free to change whatever
        
    def popularity(self, num):
        '''Purpose: To see which recent tweets are the most popular. Popularity is defined by the combined amount of likes, replies, and retweets
        Arguments: num is the amount of tweets we want to see
        Return: prints tweet
        '''
        if type(num) != int:
            raise TypeError("csv_name should be a string, specifically the path to the csv of tweets")
        new=pd.DataFrame(self.df["text"])
        new["popularity"]= self.df["retweet_count_x"]+ self.df["reply_count_x"]+ self.df["like_count_x"]
        new=new.sort_values("popularity", ascending=False).reset_index()
        for i in range(num):
            print("\033[1m#" + str(i+1) +" with " + str(new["popularity"][i+1]) + " popularity score: \033[0m")
            print(new["text"][i+1] +"\n")
        
