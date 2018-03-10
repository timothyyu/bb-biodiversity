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

import json
def example():
    res = engine.execute("SELECT * FROM samples")

    # return all rows as a JSON array of objects
    return json.dumps([dict(r) for r in res])

# app = Flask(__name__)

# @app.route("/")
def homepage():
	print("Server received request for homepage...")
	return("test")


# @app.route("/names")
def names():
    results = session.query(samples).statement
    results_list=list(np.ravel(results))
    return (jsonify(results_list))


print(example())
 
# @app.route('/otu')
# @app.route('/metadata/<sample>')
# @app.route('/wfreq/<sample>')
# @app.route('/samples/<sample>')

# if __name__ == "__main__":
# 	app.run(debug=True)