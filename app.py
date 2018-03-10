###Imports
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from sqlalchemy import func

from flask import Flask, jsonify, render_template
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

#table references (r)
otu = Base.classes.otu
samples= Base.classes.samples
samples_metadata = Base.classes.samples_metadata
#session link for python to database:
session = Session(engine)

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

###Flask

app = Flask(__name__)

@app.route("/")
def homepage():
	print("Server received request for homepage...")
	return("test")

#revise: pandas ---> jsonify
@app.route("/names")
def example():
	results = session.query(samples).all()
	results_untuple = list(np.ravel(results))
	return jsonify(results_untuple)

#revise: pandas ----> jsonify only keys part of response
@app.route('/otu')
def otu():
	results = engine.execute("SELECT lowest_taxonomic_unit_found FROM otu")
	# return all rows as a JSON array of objects using list comprehension
	return json.dumps([dict(r) for r in results],separators=(',', ': '), skipkeys = True, indent=2,check_circular=True)

# @app.route('/metadata/<sample>')
# @app.route('/wfreq/<sajmple>')
# @app.route('/samples/<sample>')

if __name__ == "__main__":
	app.run(debug=True)
