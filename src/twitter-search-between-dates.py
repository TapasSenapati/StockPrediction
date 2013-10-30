import tweepy
import oauth2 as oauth
import time

auth = tweepy.auth.OAuthHandler('mwGjl1cDvr9wsZfSOKlrvw', '2UElrZPqrSaoUUHdmkq1XcngMYaBjJzSGs4lUW9h98I')
auth.set_access_token('1437787351-xnDWc6myk4N4GQC2YK0u1EKDm89D0mfSzRIqmOa', 'dr6xwqJcnzcsv3be2HVS48pC12kzsemlDxXcZAXAY')
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
    time.sleep(0.5)
    store.append(tweet.user.name)
    print "\n"
     
print store
