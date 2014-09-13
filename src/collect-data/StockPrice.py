import urllib2
import json
import time

class GoogleFinanceAPI:
    def __init__(self):
        self.prefix = "http://finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT&f=nab"
    
    def get(self,symbol,exchange):
        url = self.prefix+"%s.%s"%(symbol,exchange)
        u = urllib2.urlopen(url)
        content = u.read()
        
        obj = json.loads(content[3:])
        return obj[0]
        
        
if __name__ == "__main__":
    c = GoogleFinanceAPI()
    
    while 1:
        quote = c.get("BHEL","BO")
        print quote
        time.sleep(30)
