# import RPI.gpio as GPIO 
import serial
import time
import os
import sys

solicitarTemp = [0x01,0x23,0xC1,0,8,3,1]

uart0_filestream = None

def init_uart():
    global uart0_filestream
    try:
        uart0_filestream = os.open("/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)
        print("UART inicializada com sucesso!")
    except:
        print("Error ao inicializar UART!")

init_uart()