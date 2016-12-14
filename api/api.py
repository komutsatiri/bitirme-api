# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin
from pymongo import MongoClient
import os


app = Flask(__name__)
CORS(app)

mongodb_host = os.environ['DB_PORT_27017_TCP_ADDR'];
client = MongoClient(mongodb_host,27018)
collection = client.conflict_db.events

@app.route('/', methods=['GET'])
def hello_world():
	output = 'Hi, give me some parameters, would you?'
	return jsonify({'result' : output})


@app.route('/markers/dyad=<int:dyad_new_id>&min=<int:minimum>&max=<int:maximum>', methods=['GET'])
@app.route('/markers/dyad=<int:dyad_new_id>', defaults={'minimum':None, 'maximum':None}, methods=['GET'])
@app.route('/markers', defaults={'dyad_new_id':None, 'minimum':None,'maximum':None}, methods=['GET'])
def get_markers(dyad_new_id,minimum,maximum):
	output = []
	counter = 0
	
	if dyad_new_id is not None and minimum is None and maximum is None:
		print 'dyad is given'
		for q in collection.find({'dyad_new_id': dyad_new_id},{'_id':False}).sort([('date_start',1)]):
			output.append({'id' : q['id'], 'lat' : q['latitude'], 'lon' : q['longitude'],
							'time' : q['date_start']})
			counter = counter + 1
		return jsonify({'result' : output, 'number of records': counter})
	elif dyad_new_id is not None and minimum is not None and maximum is not None:
		print 'dyad, death_range are given'
		for q in collection.find({'dyad_new_id': dyad_new_id, 'best':{'$gte':minimum,'$lte':maximum}},{'_id':False}).sort([('date_start',1)]):
			output.append({'id' : q['id'], 'lat' : q['latitude'], 'lon' : q['longitude'],
							'time' : q['date_start']})
			counter = counter + 1
		return jsonify({'result' : output, 'number of records': counter})	

	if dyad_new_id is None and minimum is  None and maximum is  None:
		print 'nothing given'
		for q in collection.find({},{'_id':False}).sort([('date_start',1)]):
			output.append({'id' : q['id'], 'lat' : q['latitude'], 'lon' : q['longitude'],
							'time' : q['date_start']})
			counter = counter + 1
		return jsonify({'result' : output, 'number of records': counter})	
			
@app.route('/details/<int:event_id>', methods=['GET'])
def get_details(event_id):
	q = collection.find_one({'id': event_id,},{'_id':False})
	if q:
		output = {'source_article': q['source_article'], 'dyad_name': q['dyad_name']}
	else:
		print q
		output = 'No results found'	
	return jsonify({'result' : output})

@app.route('/dyads', methods=['GET'])
def get_dyads():
	output = {}
	counter = 0
	ids = collection.distinct('dyad_new_id')
	names = collection.distinct('dyad_name')
	try:
		for q,w in enumerate(ids):
			output[w] = names[q]
			counter = counter + 1
	except:
		output = 'Things went terribly wrong'			
	return jsonify({'result' : output, 'number of records': counter})

@app.route('/death_range', methods=['GET'])
def get_minmax():
	output = {}
	divider = 8
	try:
		for q in collection.find({},{'best':True,'_id':False}).sort([('best',1)]).limit(1):
			best_min = q['best']
		for w in collection.find({},{'best':True,'_id':False}).sort([('best',-1)]).limit(1):
			best_max = w['best']
	except:
		output = 'Things went terribly wrong'
	avg = (best_max - best_min + 1)/divider
	for x in range(0,divider):
		i = (best_min+(x)*avg)
		j = (best_min+(x+1)*avg-1)
		output[x] = str(i) + '-' + str(j)
	return jsonify({'result' : output})	



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True )
