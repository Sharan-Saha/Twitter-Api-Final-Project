from os import read
import tweepy
from src import apiCodes
import json
import time
from pathlib import Path
# you can access apiCodes.py by unzipping the Codes.zip file, ask me for the password

class ApiCall:
    def __init__(self):

        self.codes = apiCodes.Codes().assignValues()
        self.auth = tweepy.OAuthHandler(self.codes["api_key"], self.codes["api_key_scrt"])
        self.auth.set_access_token(self.codes["access_tkn"], self.codes["access_tkn_scrt"])
        self.api = tweepy.API(self.auth)

        
    def setApi(self):
        
        self.us_woeid = 23424977
        self.national_trends = self.api.get_place_trends(self.us_woeid)

        return self.national_trends
    
    def callApi(self):
        self.national_trends = self.setApi()
        self.trends = []
        for trend in self.national_trends[0]["trends"][:50]:
            if type(trend["tweet_volume"]) == int:
                self.trends.append((trend["name"], trend["tweet_volume"]))
        self.trends.append(len(self.trends))
        self.trends.insert(0, time.time())
        print(self.trends)

        return self.trends
    
    def getTrends(self):
        self.path = Path('src/trends.json')
        if self.path.is_file():
            with open(self.path) as readfile:
                self.trends = json.load(readfile)
            if self.trends[0] < time.time() - 900:
                self.trends = self.callApi()
        else:
            self.trends = self.callApi()
            print("False")
        with open(self.path, "w") as outfile:
            json.dump(self.trends, outfile)

