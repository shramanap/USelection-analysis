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
FIELDS = {'entities.hashtags.text':True,'_id':False} 



@app.route("/")
def chart():
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    	collection = connection[DBS_NAME][COLLECTION_NAME]
    	projects = collection.find(projection=FIELDS)
    	hashtags=[]
    	hashtags = [ hashtag['text']
 		for project in projects
 			for hashtag in project['entities']['hashtags']]
 	dct = {}
 	dct={w: 1 if w not in dct and not dct.update({w: 1}) 
                  else dct[w] + 1
                  if not dct.update({w: dct[w] + 1}) else 1 for w in hashtags}
        del dct["USelections"]
        del dct["Trump"]
        del dct["clinton"]
        dct=sorted(dct.items(),key=operator.itemgetter(1),reverse=True)[:10]
        labels,values = map(list,zip(*dct))
       	return render_template('chart.html', values=values, labels=labels)
    	

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5002,debug=True)
