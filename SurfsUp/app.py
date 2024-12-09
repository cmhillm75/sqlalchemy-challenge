# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import os

#################################################
# Database Setup

# Absolute path to the database file
db_path = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'hawaii.sqlite')
engine = create_engine(f"sqlite:///{db_path}")

# Declare a Base using 'automap_base()'
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called 'Measurement' and
# the station class to a variable called 'Station'
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)

#################################################
# Flask Routes

# Define the homepage route
@app.route('/')
def homepage():
    return (
        f"This is the homepage for my Climate API, please copy the links below and add dates where required:<br/><br/>"
        f"There are 5 additional links below to provide additional information:<br/><br/>"
        f"This is the precipitation route which provides the most recent 12 months of data in the table:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"This is the stations route, it lists the names of the 9 stations in Hawaii:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"This is the temperature observations route, it provides the dates for the most recent 12 months in the table and its temperature:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"This is the start date route, it gives temp data after the date you use. (Input a date on the end of the url in 'YYYY-MM-DD' format):<br/>"
        f"/api/v1.0/&lt;start&gt;<br/><br/>"
        f"This is the date range route, it gives temp data for your range of dates. (Input a start and end date in 'YYYY-MM-DD'/'YY-MM-DD' format):<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )
###############################################
# Precipitation route for last 12 monhts of data. 
# Create a date/prcp dictionary and return JSON of the station data.
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the date 12 months ago from the most recent date in the dataset
    recent_date_str = session.query(func.max(Measurement.date)).scalar()
    recent_date = dt.datetime.strptime(recent_date_str, '%Y-%m-%d')
    date_12_months_ago = recent_date - dt.timedelta(days=365)

    # Query for precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_12_months_ago).all()

    # Convert the query results to a dictionary
    precip_data = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precip_data)

###############################################
# Create stations route and return a json list of the 9 stations.
@app.route('/api/v1.0/stations')
def stations():
    # Query for stations
    results = session.query(Station.station, Station.name).all()
    stations_data = []
    for station, name in results:
        stations_data.append({"station": station, "name": name})
    return jsonify(stations_data)

###############################################
# tobs (temperature observations) route for most active station for most recent year.
# Return a JSON list of temp observations for previous year.
@app.route('/api/v1.0/tobs')
def tobs():
    # Identify the most active station
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(
        func.count(Measurement.station).desc()).first()[0]

    # Calculate the date 12 months ago from the most recent date in the dataset
    recent_date_str = session.query(func.max(Measurement.date)).scalar()
    recent_date = dt.datetime.strptime(recent_date_str, '%Y-%m-%d')
    date_12_months_ago = recent_date - dt.timedelta(days=365)

    # Query for temperature observations of the most active station for the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == most_active_station).filter(Measurement.date >= date_12_months_ago).all()

    # Convert the query results to a list of dictionaries
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]

    # Return the JSON representation of the list
    return jsonify(tobs_data)

###############################################
# Define start route, Use one date from data and get the min, max and avg temps from that
# date to the most recent date. See instructions on the homepage route.
@app.route('/api/v1.0/<start>')
def start(start):
    try:
        # Parse the start date
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Please add a date at the end of the url in the Date format of YYYY-MM-DD"}), 400
    
    # Query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')
    ).filter(Measurement.date >= start).all()
    
    if not results or results[0].TMIN is None:
        return jsonify({"Start Date": start, "TMIN": None, "TAVG": None, "TMAX": None}), 404
   
    # Create a dictionary to store the results
    temp_stats = {
        "Start Date": start,
        "TMIN": results[0].TMIN,
        "TAVG": round(results[0].TAVG, 2),
        "TMAX": results[0].TMAX
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_stats)

###############################################
# Define start and end route to show the min, max and avg temps for that date range.
# This is just like the start route except we add an end date to the range.
@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    try:
        # Parse the start and end dates
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Please add start/end dates to the end of the URL in the format of YYYY-MM-DD/YYYY-MM-DD"}), 400

    # Query for temperature data between the start and end dates
    results = session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Check if results contain None values
    if not results or results[0].TMIN is None:
        return jsonify({"Start Date": start, "End Date": end, "TMIN": None, "TAVG": None, "TMAX": None}), 404
    
    # Create a dictionary to store the results
    temp_data = {
        "Start Date": start,
        "End Date": end,
        "TMIN": results[0].TMIN,
        "TAVG": round(results[0].TAVG, 2),
        "TMAX": results[0].TMAX
    }

    # Return the JSON representation of the dictionary
    return jsonify(temp_data)

###############################################
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
