from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
import re
from collections import Counter
from collections import OrderedDict
import operator
app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'test'
COLLECTION_NAME = 'tweets'
FIELDS = {'text':True,'entities':True,'_id':False} 

@app.route("/")
def index():
    return render_template("test.html")

@app.route("/PRECOG")
def chart():
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    	collection = connection[DBS_NAME][COLLECTION_NAME]
    	projects = collection.find(projection=FIELDS)
    	image=collection.find({"entities.media": {"$exists":True}}).count()
    	text=collection.find({"text": {"$exists":True}}).count()
    	it=collection.find({"entities.media": {"$exists":True}},{"text": {"$exists":True}}).count()
    	labels=['text','image','image+text']
    	values=[text,image,it]
       	return render_template('chart.html', values=values, labels=labels)
    	

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)
