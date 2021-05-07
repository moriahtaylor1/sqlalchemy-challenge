import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Precipitation = Base.classes.hawaii

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
#convert query reuslts to a dictionary with date and the key and prcp as the value
#return JSON representation of your dictionary
def precipitation():
    #create session
    session = Session(engine)
    #select date and prcp
    engine.execute('SELECT date, prcp FROM Measurement').fetchall()
    
    #query all precipitation measurements
    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()
    session.close()
    
    #convert list of tuples into normal list
    all_measures = list(np.ravel(results))
    
    return jsonify(all_measures)

@app.route("/api/v1.0/stations")

@app.route("/api/v1.0/tobs")

@app.route("/api/v1.0/<start>")

@app.route("/api/v1.0/<start>/<end>")


if __name__ == '__main__':
    app.run(debug=True)

