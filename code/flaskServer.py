#!/usr/bin/python

#THis script creates a Flask server, and serves the index.html out of the templates folder.
#It also creates an app route to be called via ajax from javascript in the index.html to query
#the database that is being written to by tempReader.py, and return the data as a json object.

#This was written for Joshua Simons's Embedded Linux Class at SUNY New Paltz 2020
#And is licenses under the MIT Software License

#Import libraries as needed
from flask import Flask, render_template, jsonify, Response
import sqlite3 as sql
import json
import RPi.GPIO as GPIO 
import time
from weatherLogger import readDHT
import Adafruit_BMP.BMP085 as BMP085 

#Globals
redPin = 27
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sqlData")
def chartData():
    con = sql.connect('weather.db')
    cur = con.cursor()
    con.row_factory = sql.Row
    cur.execute("SELECT date, temperature FROM weather WHERE temperature > 60")
    dataset = cur.fetchall()
    print (dataset)
    chartData = []
    for row in dataset:
        chartData.append({"Date": row[0], "Temperature": float(row[1])})
    return Response(json.dumps(chartData), mimetype='application/json')

@app.route("/stats")
def weatherStats():
    sensor = BMP085.BMP085() # Calling the sensor 
    pressure = sensor.read_pressure() 
    tempF, hum = readDHT(tempPin)
    wStats = [pressureReading, tempF, hum]
    return Response(json.dumps(wStats), mimetype='application/json')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=2020, debug=True, use_reloader=False)