#import regex
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

#start getFeatureList
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
        features['contains(%s)' % word] = (word in tweet_words)
   
    return features
#end
	

#Read the tweets one by one and process it
inpTweets = csv.reader(open('training.1600000.processed.noemoticon.csv', 'rb'), delimiter=',')
stopWords = getStopWordList('stopWordsList.txt')
featureList = getFeatureList('myfeaturelist2.txt')
count = 0;
tweets = []
for row in inpTweets:
    sentiment = row[1]
    tweet = row[5]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    tweets.append((featureVector, sentiment))
#with open("AFINN-111.txt") as f:
#        for line in f.readlines():
#                word,val = line.strip().split("\t")
#                if int(val) > 0:
#                        sentiment = "positive"
#                else:
#                        sentiment = "negative"
#                tweets.append((word,sentiment))
#end loop
#print tweets

training_set = nltk.classify.util.apply_features(extract_features, tweets)
#pp.pprint(training_set)

# Train the Naive Bayes classifier

if os.path.exists("nbclassify.p") == False:
	NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
	pickle.dump(NBClassifier,open( "nbclassify.p", "wb" ) )
	print "Written to file"
else:
	NBClassifier = pickle.load( open( "nbclassify.p", "rb" ) )
	print "Read from file"
#MaxEntClassifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, \
#encoding=None, labels=None, sparse=True, gaussian_prior_sigma=0, max_iter = 10)
# Test the classifier
#testTweet = 'i am just so upset with microsoft for ruining banjo kazooie ..'
#processedTestTweet = processTweet(testTweet)
#extract_features(getFeatureVector(processedTestTweet, stopWords))
#sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
#print "\n\n"
#print extract_features(processedTestTweet)
########################################
test_tweets = json.load(open("../data_files/MSFT_2013-11-28.json"))
f=open("output.csv","wb")
positive_sentiment = 0
negative_sentiment = 0
for key in test_tweets.keys():
	#print key+"\n"
	key_clean1 = key.replace("\n"," ")
	key_clean = key_clean1.replace(","," ")
	key_clean = key_clean.replace("microsoft","")
	processedTestTweet = processTweet(key_clean)
	
	sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
	if sentiment == "positive":
		positive_sentiment = positive_sentiment+1
	elif sentiment == "negative":
		negative_sentiment = negative_sentiment+1
	text = processedTestTweet+","+sentiment+"\n"
	f.write(text)
	
#sentiment = MaxEntClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
print "negative_sentiment = %d, positive_sentiment = %d\n" % (negative_sentiment, positive_sentiment)
#print NBClassifier.show_most_informative_features(10)
#print sentiment
