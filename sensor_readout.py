# This script serves as a module to be imported to the main function mail_handler.py
# It is used to access the sensor connected to the Raspberry Pi and get a readout 
# Sensor used: CCS811 on a breakout board from joy-it
# The sensor is a metal oxide sensor measuring the total volatile organic compound concentration in the air
# and calculats the equivalent carbon dioxide concentration based on the assumption the sensor is used
# indoors and the main producers of CO2 are humans#
# 
# author: philippti
# date: 20.11.2020
"""
==============================================================================================================================================================================================
"""

""" imports """

import board                                # CircuitPython module used to define id's for available Pins
import busio                                # python module supporting serial protocols 
import adafruit_ccs811                      # importing the module for interacting with the breakout board and the sensor


""" initializing the sensor and board """

i2c = busio.I2C(board.SCL, board.SDA)       # initialize the I2C Bus of the Pi, use the board method to assign the right GPIO (general purpse input output) pins
ccs811 = adafruit_ccs811.CCS811(i2c)        # initialize the sensor using the module for the breakout board provided by Adafruit


""" funcions """

def readout():                              # simple method to readout the values of the sensor

    co2 = ccs811.eco2                       # storing the equivalent CO2 concentration in the air
    tvoc = ccs811.tvoc                      # tvoc: total volatile organic compounds
    temp = ccs811.temperature               # air temperature 

    return co2, tvoc, temp                  # return the three values as a tuple