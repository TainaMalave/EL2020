# Temperature Log 

## What is the purpose of this branch?: 
   - This branch contains all the information needed in order to get your touch sensor to blink an LED on the Raspberry Pi and read the temperature of the area that you're in, into a CSV file. 

## What is needed?: 
    • Hardware: Raspberry Pi, breadboard, LED, touch sensor, temperature sensor. 

    • Software: You will need to install the Adafruit DHT Python library. Do this by simply typing in the following:

        • sudo python3 -m pip install -upgrade pip setuptools wheel
        • sudo pip3 install Adafruit_DHT

## Assuming you wired everything correctly...
   -  Once you wire everything, correctly, and you run tempLog.py - it should proceed to blink the LED and then read the temperature into a CSV file. 
