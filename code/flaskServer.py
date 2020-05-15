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
import Adafruit_GPIO.I2C as I2C
import Adafruit_BMP.BMP085 as BMP085 
import Adafruit_DHT
import smtplib
import socket

#Globals Variables
redPin = 27
tempPin = 17
lightPin = 23
tempSensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BCM)
sensor = BMP085.BMP085() 
app = Flask(__name__)

# Variables for sending email
eFROM = "Taina.Malave@gmail.com"
eTO = "8456374836@vtext.com"
Subject = "Get Yo Pi From Outside"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

# function to send alert to my phone
def alert():
    Text = "It's DARK OUTSIDE! GET YOUR PI!"
    eMessage = 'Subject: {}\n\n{}'.format(Subject, Text)
    server.login("Taina.Malave@gmail.com", "elqvwmkbuzdrzwiq")
    server.sendmail(eFROM, eTO, eMessage)
    server.quit

# Function to Get Temp and Humidity
def readDHT(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempF = '{0:0.1f}'.format(temperature)
		humid = '{1:0.1f}'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')

	return tempF, humid

# Function to get Light or Dark
def light(lightPin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(lightPin, GPIO.IN)
    lOld = not GPIO.input(lightPin)
    time.sleep(0.5)
    if GPIO.input(lightPin) != lOld:
        if GPIO.input(lightPin):
            lightOrDark = 'DARK'
            alert()
        else:
            lightOrDark = 'LIGHT'
    lOld = GPIO.input(lightPin)
    return lightOrDark

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
    
    pressure = sensor.read_pressure() 
    pressureReading = '{0:0.2f}'.format(pressure)
    tempF, hum = readDHT(tempPin)
    lightOrDark = light(lightPin)
    wStats = [tempF, hum, pressureReading, lightOrDark]
    print (wStats)
    return Response(json.dumps(wStats), mimetype='application/json')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=2020, debug=True, use_reloader=False)