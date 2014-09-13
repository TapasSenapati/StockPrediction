import json
import re
import sys
fname = sys.argv[1]
fname = re.sub('.json','.csv',fname)
fp=open(sys.argv[1])

var = json.load(fp)
with open(fname,"w") as f:
	for key in var.keys():
		key = re.sub('\n',' ',key)
		key = re.sub('\r',' ',key)
		f.write("neutral,"+key+"\n")

fp.close()

