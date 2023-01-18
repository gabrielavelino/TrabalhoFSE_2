import RPi.GPIO as GPIO
import CRC
import serial
import time
import os
import sys

# solicitarTemp = [0x01,0x23,0xC1,0,8,3,1]



def init_uart():
    try:
        uart0 = serial.Serial("/dev/serial0",9600)
        print("UART inicializada com sucesso!")
        return uart0
    except:
        print("Error ao inicializar UART!")


def close_uart(uart0):
    uart0.close()
    print("UART fechada com sucesso!")

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    resistor = GPIO.PWM(23, 1000)
    ventilador = GPIO.PWM(24, 1000)
    print("GPIO inicializado com sucesso!")


if __name__ == "__main__":
#   init_gpio()
  uart0 = init_uart()
  close_uart(uart0)