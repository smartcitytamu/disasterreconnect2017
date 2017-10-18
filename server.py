from flask import Flask, render_template, request, jsonify, json
import pymongo
import json
from bson.json_util import dumps

def connect_article_db():
    url = "mongodb://127.0.0.1:27017"
    client = pymongo.MongoClient(url)
    db = client['aggieChallenge']
    collection = db['articles']
    return collection

app = Flask(__name__)

path = "static"
client = pymongo.MongoClient("mongodb://TAMU:aggie123@weatherdata-shard-00-00-vhgp9.mongodb.net:27017,weatherdata-shard-00-01-vhgp9.mongodb.net:27017,weatherdata-shard-00-02-vhgp9.mongodb.net:27017/test?ssl=true&replicaSet=WeatherData-shard-0&authSource=admin")
db = client["WeatherData"]

tweets = db.testTrial2.find()

count=0

outfile=open(path+'/temp1.json','w+')
#outfile.write('[')
s=dumps(tweets)
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
def hello():
    return render_template("index.html")

@app.route("/headlines")
def headlines():
    try:
        listed_words = request.args.get('keywords', default='ZZZZZZ')  # if no keywords input, try not to match anything
        keywords = listed_words.split(',')
        # Code will be here
        jsonStr = article_db.find({'title' : {'$regex' : '.*(' + '|'.join(keywords) + ').*'}})

    except Exception as e:
        print(str(e))

    return jsonify(jsonStr)

@app.route("/_getdb")
def getDB():
    print("lol")

if __name__ == "__main__":
    app.run()
