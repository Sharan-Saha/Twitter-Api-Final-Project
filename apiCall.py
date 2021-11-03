
#Notes: tweepy import won't work , no clue why
# you can access apiCodes.py by unzipping the Codes.zip file, ask me for the password

# import tweepy



from assets import apiCodes
tw = "tweepy"
# api_key = apiCodes.Codes().assignapi_key
# api_key_scrt = apiCodes.Codes().api_key_scrt
# access_tkn = apiCodes.Codes().access_tkn
# access_tkn_scrt = apiCodes.Codes().access_tkn_scrt
print(apiCodes.Codes().assignValues())

"""
### Hey guys my secret auth tokens supposed to be here but I will not be pushing them with the repo ###
auth = tw.OAuthHandler(api_key, api_key_scrt)
auth.set_access_token(access_tkn, access_tkn_scrt)

api = tw.API(auth)

us_woeid = 23424977
national_trends = api.get_place_trends(id, us_woeid)

def getTrends():
    trends = []
    for trend in national_trends[0]["trends"][:50]:
        if type(trend["tweet_volume"]) == int:
            trends.append((trend["name"], trend["tweet_volume"]))
    trends.append(len(trends))
    return trends

def main():
    deck = getTrends()
    print(type(deck))
    print(deck)

    return deck

main()
"""

