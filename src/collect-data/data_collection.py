#! /usr/local/bin/python
import os
import sys
import json
import time
import tweepy
import oauth2 as oauth
import csv
from datetime import date, timedelta

def getCompanyTweets(company_name, fetch_date, priority_handles, official_handles_content):

    auth = tweepy.auth.OAuthHandler('ihCnDKwZWZoXpeb7z3rQQ', 'TGcMdTGcxIQVC8dWeVrTNjjJhaU3GrsREE3U6jCqWc')
    auth.set_access_token('1320599683-uTYgL1xAIWMUnIJlK9rKMFigukmoc6z5eGdnrDI', 'LW3oTRP69Qof08Act9iH13HzfN4ZOAzihxvvrUMWqI')

    api = tweepy.API(auth)
    store = []
    searchLanguage = 'en'
    t=time.strptime(fetch_date,'%Y-%m-%d')
    newdate=date(t.tm_year,t.tm_mon,t.tm_mday)+timedelta(1)
    next_date = newdate.strftime('%Y-%m-%d')
    newdate =date(t.tm_year,t.tm_mon,t.tm_mday)-timedelta(1) 
    prev_date = newdate.strftime('%Y-%m-%d')
    
    twit_dict = {}
    
    output_file = company_name + '_' + fetch_date + '.csv'
    opening_time = time.strptime(prev_date+" 17:00:00",'%Y-%m-%d %H:%M:%S')
    closing_time = time.strptime(fetch_date+" 17:00:00",'%Y-%m-%d %H:%M:%S')
    for tweet in tweepy.Cursor(api.search, q=company_name, rpp=10000, 
                               result_type="mixed",
                               include_entities=True,
                               since = prev_date,
                               until= next_date,
                               lang="en",
                               with_twitter_user_id=True).items():
	if closing_time > time.strptime(str(tweet.created_at),'%Y-%m-%d %H:%M:%S') and opening_time <= time.strptime(str(tweet.created_at),'%Y-%m-%d %H:%M:%S'):
		#time.sleep(0.5#)
		#continue
        	print "Created at - " + str(tweet.created_at) + " Tweeted by - " + tweet.user.screen_name + " Text - " + tweet.text.encode('ascii', 'ignore')
		text = tweet.text.encode('ascii', 'ignore')
	
        	if text:
            		twit_dict[text] = [tweet.user.screen_name]
	else:
		print "Created at(ignored) - " + str(tweet.created_at) + " Tweeted by - " + tweet.user.screen_name + " Text - " + tweet.text.encode('ascii', 'ignore')
        time.sleep(0.5)
    
    for line in official_handles_content:
        line = line.split(':')
        company = line[0]
        handle = line[1]
        if company != company_name:
            priority_handles.append(handle)

    # print '\n'.join(priority_handles)
    
    twit_priority_dict = assign_priorities(twit_dict, priority_handles)
    if twit_priority_dict:
	writer=csv.writer(open(output_file,"w"),delimiter=',')

        for key in twit_dict.keys():
		row = []
		row=[key,"neutral"]
		writer.writerow(row)
            #outfile.close()
      	print "\n****** Tweets for company - " + company_name + " successfully written into file - " + output_file + "******\n"
    else:
        print "****** NO TWEETS FOUND ******"
        
def assign_priorities(twit_dict, priority_handles):
    for tweet, handle in twit_dict.items():
        if priority_handles.count(handle) > 0:
            twit_dict[tweet] = 1
        else:
            twit_dict[tweet] = 0
    return twit_dict

def main():

    company_filename = 'company_list.txt'
    handles_filename = 'twitter_handles.txt'
    official_handles_filename = 'official_handles.txt'
    
    if not os.path.isfile(company_filename):
        print 'company_list.txt file is missing!'
        sys.exit(1)
    if not os.path.isfile(handles_filename):
        print 'twitter_handles.txt file is missing!'
        sys.exit(1)
    if not os.path.isfile(official_handles_filename):
        print 'official_handles.txt file is missing!'
        sys.exit(1)

    with open(company_filename) as f:
        content = f.read()
        f.close()

    with open('twitter_handles.txt', 'r') as f:
        priority_handles_content = f.read()
        f.close()

    with open('official_handles.txt', 'r') as f:
        official_handles_content = f.read()
        f.close()

    companyList = content.split('\n')
    companyList = [x for x in companyList if x != '']

    priority_handles = priority_handles_content.split('\n')
    priority_handles = [x for x in priority_handles if x != '']

    official_handles_content = official_handles_content.split('\n')
    official_handles_content = [x for x in official_handles_content if x != '']

    for line in companyList:
        line = line.split(':')
        company_name = line[0]
        fetch = line[1]
        date = line[2]
        if fetch == 'y':
            print "-----------------------------------"
            print company_name
            print "-----------------------------------"
            getCompanyTweets(company_name, date, priority_handles, official_handles_content)

main()
