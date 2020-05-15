#Import Libraries
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as sql
import smtplib


#Globals
redPin = 27
greenPin = 22
tempPin = 17

#Temp and Humidity Sensor
tempSensor = Adafruit_DHT.DHT11

#LED Variables---------------------------------------------------------------------------------------
#Duration of each Blink
blinkDur = .1
#Number of times to Blink the LED
blinkTime = 7
#----------------------------------------------------------------------------------------------------


#Connect to the database
con = sql.connect('weather.db')
cur = con.cursor()

#Set the initial checkbit to 0.  This will throw a warning when run, but will still work just fine
eChk = 0

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)

def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readDHT(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempF = '{0:0.1f}'.format(temperature)
		humid = '{1:0.1f}'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')

	return tempF, humid

#Dummy time for first itteration of the loop
oldTime = 60

#Read Temperature right off the bat
tempF, hum = readDHT(tempPin)

try:
	while True:
		if time.time() - oldTime > 59:
			tempF, humid = readDHT(tempPin)
			cur.execute('INSERT INTO weather values(?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'),tempF,humid))
			con.commit()
			print('Temp is: ' + tempF)
			oldTime = time.time()

except KeyboardInterrupt:
	os.system('clear')
	con.close()
	print ("Temperature Logger and Web App Exited Cleanly")
	exit(0)
	GPIO.cleanup