import smbus2
import bme280

def init_I2C():
    bus = smbus2.SMBus(1)
    address = 0x76
    sensor = bme280.load_calibration_params(bus, address=0x76)
    dados = bme280.sample(bus, address, sensor)
    tempAmb = dados.temperature
    return tempAmb



  