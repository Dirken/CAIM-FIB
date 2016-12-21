from os import path
from codecs import encode, decode
from pymongo import MongoClient
from bson.code import Code

conn = MongoClient()
db = conn.practica
N = 0;



db.corpus.drop()
with open("groceries.csv") as f:
    for line in f:
		N = N + 1
		text = []
		for word in line.strip().split(","):
			word = decode(word.strip(),"latin2","ignore")
			text.append(word)
		d = {}
		d["content"] = text
		db.corpus.insert(d)


mapperTerms = Code(""" function() { for (var i = 0; i < this.content.length; i++) emit(this.content[i],1); }""")

mapperPairs = Code("""
  function() {
    for (var i = 0; i < this.content.length; i++) {
    	for (var j = i+1; j < this.content.length; j++) {
	        emit(this.content[i]+"#"+this.content[j],1);
	        emit(this.content[j]+"#"+this.content[i],1);
    	}
    }
  }""")


reducer = Code("""
  function(key,values) {
    var sum = 0;
    for (var i = 0; i < values.length; i++) {
      sum += values[i];
    }
    return sum;
  }""")

pairs = db.corpus.map_reduce(mapperPairs, reducer, "pairCounts")
terms = db.corpus.map_reduce(mapperTerms, reducer, "termCounts")
documents = db.pairCounts.find()
db.result.drop()

support = 1
confidence = 1

for i in documents:
  auxdoc = db.termCounts.find({"_id":i["_id"].split("#")[0]})
  result = ({"_id":i["_id"], "support":100*i["value"]/N, "confidence":100*i["value"]/auxdoc[0]["value"]})
  db.result.insert(result)

dades = [[1,1],[1,25],[1,50],[1,75],[5,25],[7,25],[20,25],[50,25]]

for i in dades:
  support = i[0]
  confidence = i[1]
  documents = db.result.find({"support":{"$gt":support}, "confidence":{"$gt":confidence}})
  size = 0
  for j in documents:
    size += 1
  print size, "rules with support confidence ", support, confidence