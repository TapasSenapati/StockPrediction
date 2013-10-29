#USAGE: wordcount.py <tweetfile> <affinityfile>
import sys

# First will be the tweet file and second will be the affin file
files = []
for file in sys.argv[1:]:
    files.append(str(file))
text = ""
tweets = ""
affin = ""
count = 0
for file in files:
    f = open(file,"rU")
    for line in f:
        if count == 0:
            tweets += line
        else:
            affin += line
    count = 1

#print "Tweets"
#print tweets

#print "Affin"
#print affin

words_to_ignore = ["that","what","with","this","would","from","your","which","while","these"]
things_to_strip = [".",",","?",")","(","\"",":",";","'s"]
words_min_size = 4
wordcount = {}
 
wordstweet = tweets.lower().split()
 
for word in wordstweet:
    for thing in things_to_strip:
        if thing in word:
            word = word.replace(thing,"")
    if word not in words_to_ignore and len(word) >= words_min_size:
        if word in wordcount:
            wordcount[word] += 1
        else:
            wordcount[word] = 1
         
sortedbyfrequency =  sorted(wordcount,key=wordcount.get,reverse=True)
  
def print_txt(sortedbyfrequency):
    for word in sortedbyfrequency:
        print word, wordcount[word]
         
frequentwords = {}
def get_frequentWords(threshold):
    for word in sortedbyfrequency:
        if wordcount[word] > threshold:
            frequentwords[word] = wordcount[word]
             
#print_txt(sortedbyfrequency)
get_frequentWords(2)
#print "High Frequency words in tweet file"
#print_txt(frequentwords)

#get all the which are in tweet file and not in affin
wordsaffin1 = affin.lower().split() # How much dew would a dew drop drop if a dew drop did drop dew
#http://stackoverflow.com/questions/3159155/how-to-remove-all-integer-values-from-a-list-in-python
wordsaffin = [x for x in wordsaffin1 if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]

cnt=0
#print "words affin ", wordsaffin
candidates = []
#print "len(wordsaffin) ", len(wordsaffin)
for frequentword in frequentwords: # wood(4) chuck(4)
    #print "frequentword> ", frequentword
    for wordaffin in wordsaffin:
        #print "wordaffins> ", wordaffin
        if wordaffin != frequentword:
            cnt = cnt + 1
            #print "cnt ", cnt
        else:
            break
        if cnt == len(wordsaffin):
            candidates.append(frequentword)
            cnt = 0
print "Candidate words which should be considered to be added to affinity set: "
print candidates    
