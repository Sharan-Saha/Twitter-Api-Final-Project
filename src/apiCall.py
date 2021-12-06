import tweepy
from src import apiCodes
import json
import time
from pathlib import Path
#You can access apiCodes.py by unzipping the Codes.zip file, ask me(Senih) for the password

class ApiCall:

    
    def __init__(self):
        '''
        Initializes codes, auth, access_token, and api 
        Parameters: None
        Returns:None
        '''
        self.codes = apiCodes.Codes().assignValues()
        self.auth = tweepy.OAuthHandler(self.codes["api_key"], self.codes["api_key_scrt"])
        self.auth.set_access_token(self.codes["access_tkn"], self.codes["access_tkn_scrt"])
        self.api = tweepy.API(self.auth)

      
    def setApi(self):
        '''
        Gets and returns the national trends with and without tweet counts
        Parameters: None
        Returns: self.national_trends
        '''
        self.us_woeid = 23424977
        try:
            self.national_trends = self.api.get_place_trends(self.us_woeid)
            return self.national_trends
        except:
            print("Api Call Not Succesful")

    
    def callApi(self):
        '''
        Initializes a trends list and for each item that has a corresponding tweet in national_trends, appends it to trends
        Parameters: None
        Returns: self.trends 
        '''
        self.national_trends = self.setApi()
        self.trends = []
        for trend in self.national_trends[0]["trends"][:50]: #For every trend, we make sure there is a number associated with it
            if type(trend["tweet_volume"]) == int:
                self.trends.append((trend["name"], trend["tweet_volume"]))#If there is a number associated with it, we append that to the trends
        self.trends.append(len(self.trends))#Adds the length of the trends to the end of the list
        self.trends.insert(0, time.time()) #Adds the time of call to the beginning of the list
        print("Trends Updated!")
        return self.trends
        
    def getTrends(self):
        '''
        Checks to see if trends.json exists. If it does, it reads the data in the file and if that data is longer than 15 minutes it updates the items in the trends list and dumps it in the json file. If the file doesn't exist, it creates a trends.json file and and dumps the most up to date trends list into the newly created file
        Parameters: None
        Returns: None

        '''
        self.path = Path('src/trends.json')
        if self.path.is_file():
            with open(self.path) as readfile:
                self.trends = json.load(readfile)
            if self.trends[0] < time.time() - 900:# If it has been longer than 15 minutes, the trends are updated
                self.trends = self.callApi()
        else:
            self.trends = self.callApi()
        with open(self.path, "w") as outfile:
            json.dump(self.trends, outfile)
