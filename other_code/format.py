import json
import re
fname = sys.argv[1]
fname = re.sub('.json','.txt',fname)
fp=open(sys.argv[1])

var = json.load(fp)
with open(fname,"w") as f:
	for key in var.keys():
		key = re.sub('\n',' ',key)
		f.write(key+"\n")

fp.close()

