import tweepy
import oauth2 as oauth

auth = tweepy.auth.OAuthHandler('ihCnDKwZWZoXpeb7z3rQQ', 'TGcMdTGcxIQVC8dWeVrTNjjJhaU3GrsREE3U6jCqWc') #shayan's
auth.set_access_token('1320599683-uTYgL1xAIWMUnIJlK9rKMFigukmoc6z5eGdnrDI', 'LW3oTRP69Qof08Act9iH13HzfN4ZOAzihxvvrUMWqI')
api = tweepy.API(auth)
# print api.me().name
# for status in tweepy.Cursor(api.user_timeline,id='microsoft').items(15):
#     print status.text+'\n'
store = []
searchLanguage = 'en'
for tweet in tweepy.Cursor(api.search, q="Microsoft", rpp=10000, 
                           result_type="recent",
                           #include_entities=True,
                           since = '2013-10-26',
                           until= '2013-10-27',
                           lang=searchLanguage.encode("utf_8", "replace"),#"en",
                           with_twitter_user_id=True).items():
    print tweet.id, tweet.created_at#, tweet.text #tweet.user.name
    store.append(tweet.user.name)
    print "\n"
     
print store
