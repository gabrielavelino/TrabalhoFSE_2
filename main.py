import RPi.GPIO as GPIO
import CRC
import serial
import time
import os
import sys
import pid
import struct
import time
import uart


# Esp32 + Ler ou enviar + subCod + matricula + estado
solicitarTempInt = b'\x01\x23\xC1\x00\x08\x03\x01' # [7]
# solicitarTempInt2 = [b'\x01', b'\x23',b'\xC1',b'\x00',b'\x08',b'\x03',b'\x01']
solicitaTempRef = b'\x01\x23\xC2\x00\x08\x03\x01' # [7]
usuario = b'\x01\x23\xC3\0\8\3\1' # [7]
enviaInt = b'\x01\x23\xC3\0\8\3\1' # [7]

ligarSistema = b'\x01\x16\xD3\x00\x08\x03\x01\1' # [8]
desligarSistema = b'\x01\x16\xD3\x00\x08\x03\x01\0' # [8]
algoritmoOn = b'\x01\x16\xD5\x00\x08\x03\x01\1' # [8]
algoritmoOff = b'\x01\x16\xD5\x00\x08\x03\x01\0' # [8]

ativaCurva = b'\x01\x16\xD4\x00\x08\x03\x01\1' # [8]
desativaCurva = b'\x01\x16\xD4\x00\x08\x03\x01\0' # [8]

enviaReferencia= b'\x01\x16\xD2\0\8\3\1' # [7]


def init_estados(uart0):
    pid.pid_configura_constantes(30.0,0.2,400.0)
    pid.pid_atualiza_referencia(80.0)
    print(pid.pid_controle(35.0))
    print('-----inicializando estados----')
    uart.enviarCmd(uart0,desligarSistema)
    print('Desligando sistema...\n')
    uart.enviarCmd(uart0,algoritmoOff)
    print('Desligando funcionamento...\n')
    uart.enviarCmd(uart0,desativaCurva)
    print('Desligando curva...\n')




def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    print("GPIO inicializado com sucesso!")



# def solicitarTemperatura(uart0,temp):
#     # print('entrou aqui')
#     message = temp # C1 = solicitar temperatura
#     # print(message)
#     crc = CRC.calcula_CRC(message,7)
#     crc = crc.to_bytes(2,'little')
#     message = message + crc
#     print("escrevendo temperatura...")
#     uart0.write(message)
#     resposta = uart0.read(9)
#     if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
#         print('Error no Calculo CRC, tentando de novo...')
#         solicitarTemperatura(uart0,temp)
#     time.sleep(1)
#     tempInt = [resposta[3],resposta[4],resposta[5],resposta[6]]
#     temperatura = struct.unpack('f', bytearray(tempInt))[0]
#     return temperatura
#     # print(int(hex(resposta[3]),16)  + (int(hex(resposta[4]),16)<< 8) + (int(hex(resposta[5]),16) << 16) + (int(hex(resposta[6]),16) << 24))
#     # return resposta


if __name__ == "__main__":
    init_gpio()
    uart0 = uart.init_uart()
    init_estados(uart0)
    # solicitarTemperatura(uart0)
    # requestFloat(solicitarTempInt2,uart0)
    # enviarCmd(uart0)
    
    while True:
        tempInt = uart.solicitarTemperatura(uart0,solicitarTempInt)
        print('TempInt: ' + str(tempInt))
        tempRef = uart.solicitarTemperatura(uart0,solicitaTempRef)
        print('TempREF: ' + str(tempRef))
        time.sleep(1)
        cmd = uart.lerCmd(uart0)
        cmd = str(hex(cmd[3]))
        print(cmd)
        if cmd == '0xa1':
            print("Ligar forno...")
            uart.enviarCmd(uart0,ligarSistema)
        elif cmd == '0xa2':
            print("Desligar forno...")
            uart.enviarCmd(uart0,desligarSistema)
        elif cmd == '0xa3':
            print('iniciando aquecimento...')
            uart.enviarCmd(uart0,algoritmoOn)
        elif cmd == '0xa4':
            print('desligando aquecimento...')
            uart.enviarCmd(uart0,algoritmoOff)