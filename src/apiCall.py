import tweepy
import apiCodes
import json
import time
from pathlib import Path
#IT F***ING WORKS!!
# you can access apiCodes.py by unzipping the Codes.zip file, ask me for the password

def callApi():
    codes = apiCodes.Codes().assignValues()
    auth = tweepy.OAuthHandler(codes["api_key"], codes["api_key_scrt"])
    auth.set_access_token(codes["access_tkn"], codes["access_tkn_scrt"])
    api = tweepy.API(auth)
    us_woeid = 23424977
    national_trends = api.get_place_trends(us_woeid)
    # print(deck)

    return national_trends

def getTrends(national_trends):
    """
    checks the twitter API for the top 50 trends in the united states WOEID, returns the trends with a valid tweet count in a list, starting with the total amount of returned 
    """
    trends = []
    for trend in national_trends[0]["trends"][:50]:
        if type(trend["tweet_volume"]) == int:
            trends.append((trend["name"] , trend["tweet_volume"]))
    trends.append((len(trends)))
    trends.insert(0, time.time())
    print(trends)
    return trends

def main():
    # (time.time())
    path = Path('src/trends.json')
    if path.is_file():
        with open(path) as readfile:
            trends = json.load(readfile)
        if trends[0] < time.time() - 900:
            trends = getTrends(callApi())
    else:
        trends = getTrends(callApi())
    with open(path, 'w') as outfile:
        json.dump(trends, outfile)
    

main()


