# This script serves as a module to be imported to the main function mail_handler
# It is used to access the sensor connected to the Raspberry Pi 
# 
# author: philippti
# date: 20.11.2020


import board                                # CircuitPython module used to define id's for available Pins
import busio                                # python module supporting serial protocols 
import adafruit_ccs811                      # importing the module for interacting with the breakout board and the sensor


i2c = busio.I2C(board.SCL, board.SDA)       # initialize the I2C Bus of the Pi
ccs811 = adafruit_ccs811.CCS811(i2c)        # initialize the sensor 

def readout():

    co2 = ccs811.eco2                       # requesting the measurements from the sensor
    tvoc = ccs811.tvoc                      # tvoc: total volatile organic compounds
    temp = ccs811.temperature 

    return co2, tvoc, temp


def warning():                              # optional warning if CO2 concentration reaches a threshold

    if(ccs811.eco2 > 1000):

        return True