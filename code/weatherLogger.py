#Import Libraries
import Adafruit_GPIO.I2C as I2C
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as sql
#This is the library to make the sensor work. I did not create this. These sensors are also depricated and aren't used as much.
import Adafruit_BMP.BMP085 as BMP085 

#Globals
redPin = 27
greenPin = 22
tempPin = 17
lightPin = 23

#Temp and Humidity Sensor
tempSensor = Adafruit_DHT.DHT11

# Pressure Sensor Readings
sensor = BMP085.BMP085() # Calling the sensor 
pressure = sensor.read_pressure() 
pressureReading = '{0:0.2f}'.format(pressure)
altitude = sensor.read_altitude()
altitudeReading = '{0:0.2f}'.format(altitude)


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


def readDHT(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempF = '{0:0.1f}'.format(temperature)
		humid = '{1:0.1f}'.format(temperature, humidity)
	else:
		print('Error Reading Sensor')

	return tempF, humid


def light(lightPin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(lightPin, GPIO.IN)
	lOld = not GPIO.input(lightPin)
	time.sleep(0.5)
	if GPIO.input(lightPin) != lOld:
		if GPIO.input(lightPin):
			print ('It is DARK')
		else:
			print ('It is LIGHT') 
	lOld = GPIO.input(lightPin)

#Dummy time for first itteration of the loop
oldTime = 60

#Read Temperature right off the bat
tempF, hum = readDHT(tempPin)

try:
	while True:
		if time.time() - oldTime > 59:
			tempF, humid = readDHT(tempPin)
			cur.execute('INSERT INTO weather values(?,?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'),tempF,humid,pressureReading))
			con.commit()

			#Printing to the terminal so that I can keep track of the readings. 
			print('Temp is: ' + tempF)
			print('Humidity is: ' + humid)
			print('Pressure is: ' + pressureReading)
			print('The altitude is: ' + altitudeReading)
			light(lightPin)

			# This is the timer that will excute the code every 60 seconds.
			oldTime = time.time()



except KeyboardInterrupt:
	os.system('clear')
	con.close()
	print ("Weather Logger and Web App Exited Cleanly")
	exit(0)
	GPIO.cleanup