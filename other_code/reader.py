arr = []
with open("AFINN-111.txt") as f:
	for line in f.readlines():
	#line = f.readline()
		word,val = line.strip().split("\t")
		if int(val) > 0:
			sentiment = "positive"
		else:
			sentiment = "negative"
		arr.append((word,sentiment))

print arr
