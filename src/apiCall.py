from os import read
import tweepy
import apiCodes
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
        self.national_trends = [('#AEWDynamite', 23458), ('Spotify', 3814681), ('Cubs', 34852), ('Apple Music', 333169), ('Stacey Abrams', 78600), ('Stroman', 13222), ('Miro', 19657), ('Wizkid', 146174), ('Alec Baldwin', 20690), ('SCOTUS', 159898), ('Igor', 17622), ('Most Played', 39722), ('Burna', 32427), ('Punk', 49321), ('Supreme Court', 284140), ('Tems', 32103), ('Ethan Crumbley', 21511), ('Susan Collins', 24192), ('Roe v Wade', 154698), ('Black 2', 43016), ('Hillary', 27057), ('Kemp', 12688)]#self.api.get_place_trends(self.us_woeid)

        return self.national_trends
    
    def callApi(self):
        self.national_trends = self.setApi()
        self.trends = []
        for trend in self.national_trends[0]["trends"][:50]:
            if type(trend["tweet_volume"]) == int:
                self.trends.append((trend["name"], trend["tweet_volume"]))
        self.trends.append(len(self.trends))
        self.trends.insert(0, time.time())

        return self.trends
    
    def getTrends(self):
        self.path = Path('src/trends.json')
        if self.path.is_file():
            with open(self.path) as readfile:
                self.trends = json.load(readfile)
            if self.trends[0] < time.time() - 900:
                trends = self.callApi(self.setApi())
            else:
                self.trends = self.callApi(self.setApi())
            with open(self.path, "w") as outfile:
                json.dump(self.trends, outfile)
    
a = ApiCall()
print(a.setApi())

# def callApi():
#     codes = apiCodes.Codes().assignValues()
#     auth = tweepy.OAuthHandler(codes["api_key"], codes["api_key_scrt"])
#     auth.set_access_token(codes["access_tkn"], codes["access_tkn_scrt"])
#     api = tweepy.API(auth)
#     us_woeid = 23424977
#     national_trends = api.get_place_trends(us_woeid)

#     return national_trends

# def getTrends(national_trends):
#     """
#     checks the twitter API for the top 50 trends in the united states WOEID, returns the trends with a valid tweet count in a list, starting with the total amount of returned 
#     """
#     trends = []
#     for trend in national_trends[0]["trends"][:50]:
#         if type(trend["tweet_volume"]) == int:
#             trends.append((trend["name"] , trend["tweet_volume"]))
#     trends.append((len(trends)))
#     trends.insert(0, time.time())
#     print(trends)
#     return trends

# def main():
#     path = Path('src/trends.json')
#     if path.is_file():
#         with open(path) as readfile:
#             trends = json.load(readfile)
#         if trends[0] < time.time() - 900:
#             trends = getTrends(callApi())
#     else:
#         trends = getTrends(callApi())
#     with open(path, 'w') as outfile:
#         json.dump(trends, outfile)
# main()


