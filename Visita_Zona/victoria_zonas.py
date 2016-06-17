import re, sys, signal, os, time, datetime
import serial
### Instalar Requets
import requests
import RPi.GPIO as GPIO
import json

GPIO.setmode(GPIO.BOARD)
GPIO.setup(10,GPIO.OUT)

BITRATE = 9600


DEFAULT_CONFIG = {
    "address": "http://10.1.8.170:9000/api/visitors/",
    "led": False,
    "zona": "Zona1"
  }


def load_config(filepath):

    global led
    global url
    global zona


    print 'Loading config...'
    try:
        with open(filepath) as config_file:
            try:
                config_data = json.load(config_file)
            except ValueError as e:
                print '[FATAL] Error parsing config file: ' + str(e)
                sys.exit(-1)
    except IOError as e:
        print '[FATAL] Error loading config file: ' + str(e)

    config = config_data.get('config', DEFAULT_CONFIG)

    url = config.get('address')
    led = config.get('led')
    zona = config.get('zona')


def encender():
    GPIO.output(11,True)
    time.sleep(1)
    GPIO.output(11,False)

def mandar_zona(rfid):
    global led
    global url
    global zona

    if led:
        encender()
    consulta = url + rfid + '/' + zona
    print consulta
    r = requests.get(consulta)
    print r
    print r.json()




def main(argv):
    filepath = 'config.json'
    if len(argv) > 1:
        filepath = argv[1]


    load_config(filepath)


if __name__ == "__main__":
    main(sys.argv)

    ser = serial.Serial('/dev/ttyUSB0', BITRATE)
    rfidPattern = re.compile(b'[\W_]+')
    try:
        ser.flushInput()
        ser.flushOutput()
    except Exception, e:
        print "error open serial port: " + str(e)
        exit()

    if ser.isOpen():
        while True:
            line = ser.readline()
            last_received = line.strip()
            #print rfid
            match = rfidPattern.sub('', last_received)
	    print match
            mandar_zona(match)
