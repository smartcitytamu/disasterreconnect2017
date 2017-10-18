from flask import Flask, render_template, request, jsonify, json
import pymongo
import json
import os
import ssl
from bson.json_util import dumps

def connect_article_db():
    url = "mongodb://127.0.0.1:27017"
    client = pymongo.MongoClient(url)
    db = client['aggieChallenge']
    collection = db['articles']
    return collection

app = Flask(__name__)

path = "static"
shard_info = "@weatherdata-shard-00-00-vhgp9.mongodb.net:27017,weatherdata-shard-00-01-vhgp9.mongodb.net:27017,weatherdata-shard-00-02-vhgp9.mongodb.net:27017/test?ssl=true&replicaSet=WeatherData-shard-0&authSource=admin"

client = pymongo.MongoClient(
    "mongodb://" + os.environ['ATLAS_USER'] + ":" + os.environ['ATLAS_PASSWORD'] + shard_info,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE)

db = client["WeatherData"]

tweets = db['testTrial2']

count=0

outfile=open(path+'/temp1.json','w+')
#outfile.write('[')
print(list(tweets.find()))
s=dumps(tweets.find())
outfile.write(s)
'''for tweet in tweets:
    #print(tweet)
    del(tweet['_id'])
    tempT=dumps(tweet)
    #=''
    #json.dump(tempT,outfile)
    outfile.write(tempT)
    if(count<tweets.retrieved-1):
        outfile.write('\n')
        outfile.write(',')

    count+=1

outfile.write(']')
'''
outfile.close()

global article_db
article_db = connect_article_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo.html")
def demo():
    return render_template("intro.html")

@app.route("/headlines.json")
def headlines():
    try:
        listed_words = request.args.get('keywords', default='ZZZZZZ')  # if no keywords input, try not to match anything
        keywords = listed_words.split(',')
        #build out regex for each keyword (whitespace on each side)
        #for i, word in enumerate(keywords):
        #    keywords[i] = '\s' + word + '\s'

        # Code will be here
        jsonOut = dumps(article_db.find({'title' : {'$regex' : '.*(' + '|'.join(keywords) + ').*'}}))

    except Exception as e:
        print(str(e))

    return jsonOut

@app.route("/_getdb")
def getDB():
    print("lol")

if __name__ == "__main__":
    app.run()
