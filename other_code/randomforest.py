import scipy
import re
import csv
import pprint
import nltk.classify
import json
import pickle
import os

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert \n to space
    tweet = re.sub('\n',' ',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet, stopWords):
    featureVector = []
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences 
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end

def getFeatureList(fileName):
    fp = open(fileName, 'r')
    line = fp.readline()
    featureList = []
    while line:
        line = line.strip()
        featureList.append(line)
        line = fp.readline()
    fp.close()
    return featureList
#end

#start extract_features
def extract_features(tweet):
    #print tweet
    #print"\n"+"-----------------"
    tweet_words = set(tweet)
    #print tweet_words
    features = {}
    for word in featureList:
        features[word] = (word in tweet_words)
  
    return features
#end


inpTweets = csv.reader(open('training2.csv', 'rb'), delimiter=',')
stopWords = getStopWordList('stopWordsList.txt')
featureList = getFeatureList('myfeaturelist3.txt')
count = 0;
tweets = []
train = []
target = []
for row in inpTweets:
    sentiment = row[1]
    tweet = row[5]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords) 
    tweets.append((featureVector, sentiment))
    train.append(extract_features(featureVector))
    if sentiment == "positive":
	int_sentiment = 1
    elif sentiment == "negative":
	int_sentiment = -1
    else:
	int_sentiment = 0
    target.append(int_sentiment)



rf = RandomForestClassifier(n_estimators=150, min_samples_split=2, n_jobs=4) 
rf.fit(train, target)

testTweet = 'i am just so upset with microsoft for ruining banjo kazooie ..'
processedTestTweet = processTweet(testTweet)
test = []
test.append(extract_features(getFeatureVector(processedTestTweet, stopWords)))

predicted_probs = rf.predict_proba(realtest)
print predicted_probs
