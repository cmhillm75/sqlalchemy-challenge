# sqlalchemy-challenge

Surfsup folder holds the climate_stater.ipynb and the app.py API app files.
Resources folder holds the 2 xls csv files and the hawaii.sqlite.
The path from the apps to resources is (../Resources/hawaii.sqlite").

## Part 1 of the assignment uses climate_start.ipynb

Requires use of jupyter notebook

There are 3 portions of the jupyter sqlalchemy review.
The first is import the dependencies, create the engine and establish the bases
i.e. get the table names. Then create a session and show the columns.

The second is to complete the precipitation analaysis centered around using
dt.datetime to obtain start, end dates and then determine the interverals for plotting.
Utilize a DataFrame and matplotlib to create the bar chart/graph where our date comes
primarily from the 'measurement' table.

The third is to utilize the 'stations' table and expand on using the dt.datetime and
func.min/avg/max after showing the list of stations locations and their id then analyze
the most active station 'USC00519281'. From there create a histogram of which needed
to conver the date from a string to datetime in order to subtract from the most
recent date.

## Part 2 of the assignment uses the app.py to run the climate API

Requires use of VScode, git terminal and web browser

Using the framework for activities for module 10, day 3 in creating the API app,
started the app with listing the dependencies, the datebase setup, set up Flask and
add the run function at the end. Added os to create a db_path as was not able to get system
to recognize the path without.

The instructions list for a total of 6 routes. Using the standard route format, utilized the
assignment instructions to name each route and commented out for each the desired outcome.

The endpoints in order are:
'homepage' ('/') lists instructions and the endpoints for all routes.
'precipitation' ('/api/v1.0/precipitation') lists prcp data for most recent 12 months.
'stations' ('/api/v1.0/stations') provides a json of the 9 Hawaii stations.
'tobs' ('/api/v1.0/tobs') provides the observed times for the most active station based on the most recent year.
'start' ('/api/v1.0/start') provides a TMIN, TMAX, TAVG from a user specified date to the end date of the dataset.
'start_end' ('/api/v1.0/start_end') provides a TMIN, TMAX, TAVG from a user specified date range in the dataset.