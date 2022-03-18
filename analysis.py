import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

class Analysis:
    def __init__(self, csv_name):
        '''Constructor of Analysis object. Stores csv file name and dataframe'''
        if type(csv_name) != str:
            raise TypeError("csv_name should be a string, specifically the path to the csv of tweets")
        self.csv=csv_name
        self.df=pd.read_csv(csv_name) #you shouldn't alter the original df
        self.df=self.df.drop(columns=["Unnamed: 0"])
        
    def get_topics(self, num_topics=10, num_words=4):
        '''Purpose: to identify what topics are most-talked about at UCLA 
        Arguments: num_topics is the number of topics the words are grouped by and num_words is the number of words associated with each topic
        Return: most frequently used words associated with by topic '''
        def clean_link(string):
            string = re.sub('https://t.co\S*\w+|\n', ' ', string)
            return string
        vec = CountVectorizer(stop_words="english")
        new=self.df
        new['text'] = new['text'].apply(clean_link)
        counts = vec.fit_transform(new['text'])
        counts = counts.toarray()
        vec.get_feature_names()
        count_tweetsandusers = pd.DataFrame(counts, columns=vec.get_feature_names())
        big_count_tweetsandusers = pd.concat((new["text"],count_tweetsandusers), axis= 1)
        X = big_count_tweetsandusers.drop(columns = "text")
        model = NMF(num_topics, init="random", random_state=0)
        model.fit(X)
        def top_words(X, model, component, num_words):
            orders = np.argsort(model.components_, axis = 1)
            important_words = np.array(X.columns)[orders]
            return important_words[component][-num_words:]
        for i in range(num_topics):
            print(top_words(X, model, i, num_words))
        return
    
    def get_sentiment(self):
        '''
        Purpose: Categorize each tweet into Negative, Neutral, or Positive Sentiments. 
                 Compare the counts and map out words that are associated with each sentiment.
        Arguments: self
        Returns: 1. Bar plot of tweet counts for each sentiment
                 2. Word cloud of negative sentiment tweets
                 3. Word cloud of neutral sentiment tweets
                 4. Word cloud of positive sentiment tweets
                 NOTE:   The word cloud functions generate word clouds that are positioned 
                         and styled differently each run. Therefore, it is expected that
                         the word clouds are not precisely the same for each user running
                         the code.
        '''

        # get new subset dataframe 
        df1 = self.df[['created_at_x', 'text']]

        # define function to create sentiment column using TextBlob
        def get_sentiment(text):
            if TextBlob(text).sentiment.polarity > 0:
                return 'Positive'
            elif TextBlob(text).sentiment.polarity < 0:
                return 'Negative'
            else:
                return 'Neutral'

        # create 'sentiment' column for df1
        df1['sentiment'] = df1['text'].apply(get_sentiment)

        # create groupedby table
        groupedby_sentiment = df1.groupby('sentiment').size()

        # create bar graph for sentiments
        fig, ax = plt.subplots(1, figsize = (5, 5))
        ax.bar(groupedby_sentiment.index, groupedby_sentiment, color = ['red', 'grey', 'green'])
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')
        fig.suptitle('Sentiment Analysis of Tweets')

        # define function to add number labels on graph
        def addlabels(x,y):
            for i in range(len(x)):
                ax.text(i, y[i], str((100 * y[i] / len(df1)).round(2)) + " %", ha = 'center')
        addlabels(groupedby_sentiment.index, groupedby_sentiment)

        # define function to clean each sentiment text
        def get_cleaned_text(df1, sentiment):
            # get dataframe for specfic sentiment
            out = df1.groupby('sentiment').get_group(sentiment)
            out = out['text']
            out = ' '.join(x for x in out)
            # get rid of links
            out = re.sub('https://t.co\S*\w+|\n', ' ', out)
            # get rid of punctuation
            out = re.sub(r'[^\w\s]', ' ', out)
            # get rid of numbers
            out = ''.join(x for x in out if not x.isdigit())
            # get rid of character len <=3 strings
            out = ' '.join([x for x in out.split() if len(x) > 3])
            # change all characters to lowercase
            out = out.lower()
            return out

        # get text of each sentiment
        negative_text = get_cleaned_text(df1, 'Negative')
        neutral_text = get_cleaned_text(df1, 'Neutral')
        positive_text = get_cleaned_text(df1, 'Positive')

        # define functions for color scheme in word clouds
        def red_color_func(word, font_size, position, orientation, random_state = None, **kwargs):
            return("hsl(0, 100%%, %d%%)" % np.random.randint(10, 70))

        def grey_color_func(word, font_size, position, orientation, random_state = None, **kwargs):
            return("hsl(0, 0%%, %d%%)" % np.random.randint(10, 70))

        def green_color_func(word, font_size, position, orientation, random_state = None, **kwargs):
            return("hsl(75, 100%%, %d%%)" % np.random.randint(10, 50))

        # define function to create word clouds
        def get_word_cloud(text, func, title):
            wordcloud = WordCloud(background_color = 'white').generate(text)
            wordcloud.recolor(color_func = func)
            plt.figure(figsize = (8, 8))
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.title(title)
            plt.imshow(wordcloud, interpolation = 'bilinear')
            return plt
        
        negative_word_cloud = get_word_cloud(negative_text, red_color_func, 'Word Cloud of Negative Tweets')
        neutral_word_cloud = get_word_cloud(neutral_text, grey_color_func, 'Word Cloud of Neutral Tweets')
        positive_word_cloud = get_word_cloud(neutral_text, green_color_func, 'Word Cloud of Positive Tweets')

        return fig, negative_word_cloud, neutral_word_cloud, positive_word_cloud
        
    def popularity(self, num):
        '''Purpose: To see which recent tweets are the most popular. Popularity is defined by the combined amount of likes, replies, and retweets
        Arguments: num is the amount of tweets we want to see
        Return: prints tweet
        '''
        if type(num) != int:
            raise TypeError("num should be an integer")
        
        #makes copy of dataframe, cleans it, and adds popularity column
        new=pd.DataFrame(self.df["text"])
        new["username"]=self.df["username"]
        new["popularity"]= self.df["retweet_count_x"]+ self.df["reply_count_x"]+ self.df["like_count_x"]
        
        #sorts by popularity
        new=new.sort_values("popularity", ascending=False).reset_index()
        
        #prints num tweets
        for i in range(num):
            try:
                print("\033[1m#" + str(i+1) +" with " + str(new["popularity"][i+1]) + " popularity score by @" + str(new["username"][i+1]) + " :\033[0m")
                print(new["text"][i+1] +"\n")
            except(KeyError): #if out of scope aka num > # rows in df, then don't call error, just stop printing
                break
        
