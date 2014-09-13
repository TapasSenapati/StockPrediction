import csv
import re
import sys
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    tweet = re.sub('\n',' ',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet


def calculate_sentiment(scores,line):
	tweet = processTweet(line)
	wordList = re.sub("[^\w]", " ",  tweet).split()
	sentiment = 0
	for word in wordList:
		if word in scores.keys():	
			sentiment += scores[word]
	if sentiment > 0:
		return "positive"
	elif sentiment < 0:
		return "negative"
	else:
		return "neutral"

	
reader = csv.reader(open(sys.argv[1],"rb"),delimiter=",")
f=open("AFINN-111.txt")
scores = {} # initialize an empty dictionary
for line in f:
	term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  	scores[term] = int(score)  # Convert the score to an integer.

#print calculate_sentiment(scores,"I am not happy")

writer = csv.writer(open("mytraining2.csv","wb"), delimiter=',',quotechar='"',escapechar='\\')
for row in reader:
	write_row = []
	
	sentiment = calculate_sentiment(scores,row[5])
	write_row = [sentiment,row[1],row[2],row[3],row[4],row[5]]
	writer.writerow(write_row)


f.close()


