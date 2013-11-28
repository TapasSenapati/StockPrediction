#import regex
import re
import csv
import pprint
import nltk.classify

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
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end


#Read the tweets one by one and process it
inpTweets = csv.reader(open('full-corpus.csv', 'rb'), delimiter=',')
stopWords = getStopWordList('stopWordsList.txt')
featureList = getFeatureList('myfeaturelist.txt')
count = 0;
tweets = []
for row in inpTweets:
    sentiment = row[1]
    tweet = row[4]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    tweets.append((featureVector, sentiment));
with open("AFINN-111.txt") as f:
        for line in f.readlines():
        #line = f.readline()
                word,val = line.strip().split("\t")
                if int(val) > 0:
                        sentiment = "positive"
                else:
                        sentiment = "negative"
                tweets.append((word,sentiment))
#end loop
#print tweets

training_set = nltk.classify.util.apply_features(extract_features, tweets)
#pp.pprint(training_set)

# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
#MaxEntClassifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, \
#encoding=None, labels=None, sparse=True, gaussian_prior_sigma=0, max_iter = 10)
# Test the classifier
testTweet = 'i am so fed up with microsoft\'s horseshit. i hope bill gates dies of malaria.'
processedTestTweet = processTweet(testTweet)
#print "\n\n"
#print extract_features(processedTestTweet)

sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
#sentiment = MaxEntClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)

