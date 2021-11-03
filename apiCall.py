
#Notes: tweepy import won't work , no clue why
# you can access apiCodes.py by unzipping the Codes.zip file, ask me for the password

import tweepy
from assets import apiCodes

# api_key = apiCodes.Codes().assignapi_key
# api_key_scrt = apiCodes.Codes().api_key_scrt
# access_tkn = apiCodes.Codes().access_tkn
# access_tkn_scrt = apiCodes.Codes().access_tkn_scrt
# print(apiCodes.Codes().assignValues())



def getTrends():
    trends = []
    for trend in national_trends[0]["trends"][:50]:
        if type(trend["tweet_volume"]) == int:
            trends.append((trend["name"], trend["tweet_volume"]))
    trends.append(len(trends))
    print(trends)
    return trends

def main():
    codes = apiCodes.Codes().assignValues()
    auth = tweepy.OAuthHandler(codes["api_key"], codes["api_key_scrt"])
    auth.set_access_token(codes["access_tkn"], codes["access_tkn_scrt"])
    api = tweepy.API(auth)
    us_woeid = 23424977
    national_trends = api.get_place_trends(id, 23424977)
    deck = getTrends()
    print(type(deck))
    # print(deck)

    return deck

main()


