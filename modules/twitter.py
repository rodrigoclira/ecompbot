import oauth2
import urllib

from config import *

def update(status):
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    signmethod = oauth2.SignatureMethod_HMAC_SHA1()
        
    URL = "http://api.twitter.com/1/statuses/update.json"
    cliente = oauth2.Client(consumer,token)
    data = {'status': status}

    resp, content = cliente.request(URL, 'POST', urllib.urlencode(data))
    #print resp,content
       
       
if __name__ == '__main__':
    update('Testando')