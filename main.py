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


def lerCmd(uart0):
    dados = bytearray(b'\x01\x23\xC3\x00\x08\x03\x01') # C3 Solicita comandos do usuário
    crc = CRC.calcula_CRC(dados,7)
    print(str(hex(crc)))
    crc = crc.to_bytes(2,'little')
    dados.extend(crc)
    print("escrevendo...")
    uart0.write(dados)
    resposta = uart0.read(9)
    print(hex(resposta[3]))
    time.sleep(1)
    return str(hex(resposta[3]))

def enviarCmd(uart0):
    dados = bytearray(b'\x01\x16\xD3\x00\x08\x03\x01\x00') # C3 Solicita comandos do usuário
    crc = CRC.calcula_CRC(dados,8)
    crc = crc.to_bytes(2,'little')
    dados.extend(crc)
    print("enviando...")
    uart0.write(dados)
    resposta = uart0.read(9)
    time.sleep(1)
    return str(hex(resposta[3]))


def solicitarTemp(uart0):
    message = bytearray(b'\x01\x23\xC1\x00\x08\x03\x01') # C1 = solicitar temperatura
    crc = CRC.calcula_CRC(message,7)
    crc = crc.to_bytes(2,'little')
    message.extend(crc)
    print("escrevendo...")
    uart0.write(message)
    resposta = uart0.read(9)
    time.sleep(1)
    print(str(hex(resposta)))
    return str(hex(resposta[3]))


if __name__ == "__main__":
#   init_gpio()
    uart0 = init_uart()
    solicitarTemp(uart0)
    # enviarCmd(uart0)
    while True:
        cmd = lerCmd(uart0)
        if cmd == '0xa1':
            print("Ligar forno...")
        elif cmd == '0ax2':
            print("Desligar forno...")
            close_uart(uart0)
            break