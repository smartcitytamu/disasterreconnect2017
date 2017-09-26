from flask import Flask, render_template
import pymongo
import json
from bson.json_util import dumps

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

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/_getdb")
def getDB():
    print("lol")

if __name__ == "__main__":
    app.run()
