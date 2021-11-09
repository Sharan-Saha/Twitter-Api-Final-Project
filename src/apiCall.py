import tweepy
from assets import apiCodes
#Notes: tweepy import won't work , no clue why
# you can access apiCodes.py by unzipping the Codes.zip file, ask me for the password



def getTrends(national_trends):
    trends = []
    for trend in national_trends[0]["trends"][:50]:
        if type(trend["tweet_volume"]) == int:
            trends.append((trend["name"], trend["tweet_volume"]))
    trends.append(len(trends))
    print(trends)
    return trends

def main():
    print(tweepy.__file__)
    codes = apiCodes.Codes().assignValues()
    auth = tweepy.OAuthHandler(codes["api_key"], codes["api_key_scrt"])
    auth.set_access_token(codes["access_tkn"], codes["access_tkn_scrt"])
    api = tweepy.API(auth)
    us_woeid = 23424977
    national_trends = api.get_place_trends(id, us_woeid)
    deck = getTrends(national_trends)
    print(type(deck))
    # print(deck)

    return deck

main()


