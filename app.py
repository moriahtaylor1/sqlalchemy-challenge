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
Measurement = Base.classes.measurement
Station = Base.classes.station

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
#convert query results to a dictionary with date and the key and prcp as the value
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
    
    #create a dictionary from the raw data and append to a list of all_measures
    all_measures=[]
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        all_measures.append(precip_dict)
    #jsonify dictionary
    return jsonify(all_measures)
        

@app.route("/api/v1.0/stations")
#return a JSON list of all stations from the dataset
def stations():
    #create session
    session = Session(engine)
    #select date and prcp
    engine.execute('SELECT name FROM Station').fetchall()
    
    #query all precipitation measurements
    results = session.query(Station.name).all()
    session.close()
    
    #convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    #jsonify list
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
#query dates and temps of most active station for the last year 
#return a json list of TOBS for the previous year
def tobs():
    #create session
    session = Session(execute)
    #select all
    engine.execute('SELECT date, tobs FROM Measurement')
    
    #query date and temps for most active station
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station=='USC00519281').all()
    session.close()
    
    #create list
    active_temps = list(np.ravel(results))
    #jsonify list of temps
    return jsonify(active_temps)

@app.route("/api/v1.0/<start>")
#when given the start only, calculate the min, avg, max for all dates
#greater than or equal to the start date
def start_only(start):
    
    #select only date and tobs
    engine.execute('SELECT date, tobs FROM Measurement').fetchall()
    
    #query from start date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    session.close()
    
    #create list
    temps_from_start = list(np.ravel(results))
    #jsonify list
    return jsonify(temps_from_start)
    
    

@app.route("/api/v1.0/<start>/<end>")
#when given the start and end date, calculate the min/max/avg for dates
#between the start and end date inclusive
def start_end(start, end)
    #select only date and tobs
    engine.execute('SELECT date, tobs FROM Measurement').fetchall()
    
    #query from start date to end date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    session.close()
    
    #create list
    temps_in_range = list(np.ravel(results))
    #jsonify list
    return jsonify(temps_in_range)


if __name__ == '__main__':
    app.run(debug=True)

