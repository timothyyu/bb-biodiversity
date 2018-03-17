###Imports

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from sqlalchemy import func

from flask import Flask, jsonify, render_template, request,url_for
import numpy as np
import pandas as pd
import datetime as dt
import json

###Sqlite data import

engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")
inspector = inspect(engine)
#reflect data into classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

#table references
otu_s = Base.classes.otu
samples= Base.classes.samples
samples_metadata = Base.classes.samples_metadata
#session link for python to database:
session = Session(engine)

###Flask

app = Flask(__name__)

@app.route("/")
def homepage():
	print("Server received request for homepage...")
	return render_template("index.html")

@app.route("/names")
def example():
	results = session.query(samples).statement
	results_df = pd.read_sql_query(sql =results, con= session.bind, index_col= 'otu_id')
	results_df_list = list(results_df)
	return jsonify(results_df_list)

@app.route('/otu')
def otu():
	results = session.query(otu_s.lowest_taxonomic_unit_found).all()
	results_df_list = list(np.ravel(results))
	return jsonify(results_df_list)

@app.route('/metadata/<sample>')
def metadata(sample):
	#if request.method == 'POST':
	results = session.query(samples_metadata.AGE, samples_metadata.BBTYPE, samples_metadata.ETHNICITY, 
	samples_metadata.GENDER, samples_metadata.LOCATION, samples_metadata.SAMPLEID).filter(samples_metadata.SAMPLEID == sample[3:]).all()
	metadata_dict_response={}
	
	#samples_metadata.SAMPLEID == sample[3:]


	for result in results: 
		metadata_dict_response["AGE"] = result[0]
		metadata_dict_response["BBTYPE"] = result[1]
		metadata_dict_response["ETHNICITY"] = result[2]
		metadata_dict_response["GENDER"] = result[3]
		metadata_dict_response["LOCATION"] =  result[4]
		metadata_dict_response["SAMPLEID"] = result[5]
	#print(metadata_dict_response)
	return jsonify(metadata_dict_response)
# @app.route('/wfreq/<sajmple>')
# @app.route('/samples/<sample>')

if __name__ == "__main__":
	app.run(debug=True)



#Import debugging
# print("========================================================")
# print("table names:")
# print(Base.classes.keys())

# print("========================================================")
# print("otu column names:")
# for col in otu.__table__.columns: 
# 	print ("col: " + col.description)
# print("========================================================")
# def samplesi():
# 	print("samples column names:")
# 	for col in samples.__table__.columns: 
# 		print ("col: " + col.description)
# print("========================================================")
# print("samples_metadata column names:")
# for col in samples_metadata.__table__.columns: 
# 	print ("col: " + col.description)
# print("========================================================")