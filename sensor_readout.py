import time
import board
import busio
import adafruit_ccs811                      # importing the module for interacting with the breakout board and the sensor


i2c = busio.I2C(board.SCL, board.SDA)       # initialize the I2C Bus of the Pi
ccs811 = adafruit_ccs811.CCS811(i2c)        # initialize the sensor 

def readout():

    co2 = ccs811.eco2                       # requesting the measurements from the sensor
    tvoc = ccs811.tvoc
    temp = ccs811.temperature 

    return co2, tvoc, temp


def warning():                              # optional warning if CO2 concentration reaches a threshold

    if(ccs811.eco2 > 1000):

        return True