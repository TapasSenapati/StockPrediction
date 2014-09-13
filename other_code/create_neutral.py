import csv

fp =open("full-corpus.csv","rb")
tweets = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
with open("training2.csv","a") as f:
	writer = csv.writer(f, delimiter=',',
                            quotechar='"',escapechar='\\')
	for row in tweets:
		write_row = []
		if row[1] == "neutral":
			write_row = [row[1],row[2],row[3],"NO_QUERY","garbage",row[4]]
			writer.writerow(write_row)

