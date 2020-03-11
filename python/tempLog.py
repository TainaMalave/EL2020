# -*- coding: utf-8 -*-
#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import datetime
import os
import sqlite3

#Assign GPIO pins
redPin = 27
tempPin = 17
buttonPin = 26

#Temp and Humidity Sensor
tempSensor = Adafruit_DHT.DHT11
#LED Variables--------------------------------------------------------
#Duration of each Blink
blinkDur = .3
#Number of times to Blink the LED
blinkTime = 7
#---------------------------------------------------------------------

# connection to DB and making a cusor object so that i can access 
conn = sqlite3.connect('temperature.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS temperature
             (Date text, Temperature int, Humidity int)''')

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN)

def oneBlink(pin):
    GPIO.output(pin,True)
    time.sleep(blinkDur)
    GPIO.output(pin,False)
    time.sleep(blinkDur)

def readF(tempPin):
    humidity, temperature = Adafruit_DHT.read_retry(tempSensor,tempPin)
    temperature = temperature * 9/5.0 +32
    if humidity is not None and temperature is not None:
        tempFahr = '{0:0.1f}*F'.format(temperature)
        hum = '{0:0.1f}%'.format(humidity)
    else:
        print('Error Reading Sensor')
    return tempFahr, hum

try:
    starttime=time.time()
    while True:
        input_state = GPIO.input(buttonPin)
        if input_state == True:
            for i in range (blinkTime):
                oneBlink(redPin)
            time.sleep(.2)
            tempFahr, hum = readF(tempPin)
            date = datetime.datetime.now()
            print(tempFahr ,hum)
            params = (date, tempFahr, hum)
            c.execute('INSERT INTO temperature VALUES (?, ?, ?)',(params))
            conn.commit()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

except KeyboardInterrupt:
    os.system('clear')
    print('Thanks for Blinking and Thinking!')
    GPIO.cleanup()
