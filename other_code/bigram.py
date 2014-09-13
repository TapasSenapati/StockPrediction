import nltk
import csv
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

#inpTweets = csv.reader(open('full-corpus.csv', 'rb'), delimiter=',')
#with open("bigram.txt","w") as f:
#	for row in inpTweets:
#		f.write(row[4])
#		f.write("\n")


# change this to read in your data
finder = BigramCollocationFinder.from_words(
   nltk.corpus.genesis.words('english-web.txt'))

# only bigrams that appear 3+ times
finder.apply_freq_filter(3) 

# return the 10 n-grams with the highest PMI
print finder.nbest(bigram_measures.pmi, 10)  
