import time
import board
import busio
import adafruit_ccs811


i2c = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)

def readout():

    co2 = ccs811.eco2
    tvoc = ccs811.tvoc
    temp = ccs811.temperature

    return co2, tvoc, temp


def warning():

    if(ccs811.eco2 > 1000):

        return True