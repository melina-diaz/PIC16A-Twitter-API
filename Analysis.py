class Analysis:
    def __init__(csv_name):
        '''Makes '''
        if type(csv_name) != str:
            raise TypeError("csv_name should be a string, specifically the path to the csv of tweets")
        self.csv=csv_name
        self.df=pd.read_csv(csv_name) #you shouldn't alter the original df
        
    def get_topics():
        '''Purpose:
        Arguments: 
        Return: '''
        #Michelle's code, feel free to change whatever
        return
    
    def get_sentiment():
        '''Purpose:
        Arguments: 
        Return: '''
        #Tracy's code, feel free to change whatever
        return 
    
    def predict():
        '''Purpose:
        Arguments: 
        Return: '''
        #Melina's code, feel free to change whatever
        
    def popularity(num):
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
            print("\033[1m#" + str(i) +" with " + str(new["popularity"][i]) + " popularity score: \033[0m")
            print(new["text"][i] +"\n")
        