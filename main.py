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
solicitarTempInt2 = [b'\x01', b'\x23',b'\xC1',b'\x00',b'\x08',b'\x03',b'\x01']
solicitaTempRef = b'\x01\x23\xC2\0\8\3\1' # [7]
usuario = b'\x01\x23\xC3\0\8\3\1' # [7]
enviaInt = b'\x01\x23\xC3\0\8\3\1' # [7]

ligarSistema = b'\x01\x16\xD3\x00\x08\x03\x01\1' # [8]
desligarSistema = b'\x01\x16\xD3\x00\x08\x03\x01\0' # [8]
algoritmoOn = b'\x01\x16\xD5\x00\x08\x03\x01\1' # [8]
algoritmoOff = b'\x01\x16\xD5\x00\x08\x03\x01\0' # [8]

ativaCurva = b'\x01\x16\xD4\0\8\3\1\1' # [8]
desativaCurva = b'\x01\x16\xD4\0\8\3\1\0' # [8]

enviaReferencia= b'\x01\x16\xD2\0\8\3\1' # [7]

def requestFloat(protocolo,uart0):
    tx_buffer = bytearray(20)
    p_tx_buffer = tx_buffer

    p_tx_buffer[0] = protocolo[0]
    p_tx_buffer[1] = protocolo[1]
    p_tx_buffer[2] = protocolo[2]
    p_tx_buffer[3] = protocolo[3]
    p_tx_buffer[4] = protocolo[4]
    p_tx_buffer[5] = protocolo[5]
    p_tx_buffer[6] = protocolo[6]

    crc = CRC.calcula_CRC(tx_buffer, len(tx_buffer))
    p_tx_buffer[7] = crc & 0xFF
    p_tx_buffer[8] = (crc >> 8) & 0xFF

    if uart0 != -1:
        escreve_uart = uart0.write(tx_buffer)
        if escreve_uart < 0:
            print("UART TX error")
            return 0

    time.sleep(0.7)

    if uart0 != -1:
        rx_buffer = uart0.read(9)

        crc = CRC.calcula_CRC(rx_buffer, 7)
        if (crc & 0xFF) != rx_buffer[7] and ((crc >> 8) & 0xFF) != rx_buffer[8]:
            print("Erro de CRC")
            requestFloat(protocolo)

        if len(rx_buffer) < 0:
            return 0
        elif len(rx_buffer) == 0:
            return 0
        else:
            temp = rx_buffer[3:7]
            temperatura = struct.unpack("f", temp)
            return temperatura

# def CRC.verificaCRC(resp, crc_resp):
#   crc_calc = CRC.calcula_CRC(resp,7).to_bytes(2,'little')
#   if crc_calc == crc_resp:
#     return 'OK'
#   else:
#     print(f'Error-CRC\nCRC recebido: {crc_resp}\nCRC calculado: {crc_calc}')
#     return f'CRC-ERROR'

def init_estados():
    pid.pid_configura_constantes(30.0,0.2,400.0)
    pid.pid_atualiza_referencia(80.0)
    print(pid.pid_controle(35.0))



# def init_uart():
#     try:
#         uart0 = serial.Serial("/dev/serial0",9600)
#         print("UART inicializada com sucesso!")
#         return uart0
#     except:
#         print("Error ao inicializar UART!")


# def close_uart(uart0):
#     uart0.close()
#     print("UART fechada com sucesso!")

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    print("GPIO inicializado com sucesso!")


# def lerCmd(uart0):
#     dados = b'\x01\x23\xC3\x00\x08\x03\x01' # C3 Solicita comandos do usuário
#     crc = CRC.calcula_CRC(dados,7)

#     crc = crc.to_bytes(2,'little')
#     dados = dados + crc
    
#     uart0.write(dados)
#     resposta = uart0.read(9)
#     if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
#         print('Error no Calculo CRC, tentando de novo...')
#         lerCmd(uart0)
#     time.sleep(1)
    
#     return resposta

# def enviarCmd(uart0,comando):
#     dados = comando
#     crc = CRC.calcula_CRC(dados,8)
#     crc = crc.to_bytes(2,'little')
#     dados = comando + crc
#     print("enviando...")
#     uart0.write(dados)
#     resposta = uart0.read(9)
#     if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
#         print('Error no Calculo CRC, tentando de novo...')
#         lerCmd(uart0)
#     # time.sleep(1)
#     # return str(hex(resposta[3]))


def solicitarTemperatura(uart0,temp):
    message = temp # C1 = solicitar temperatura
    # print(message)
    crc = CRC.calcula_CRC(message,7)
    crc = crc.to_bytes(2,'little')
    message = message + crc
    print("escrevendo...")
    uart0.write(message)
    resposta = uart0.read(9)
    time.sleep(1)
    # print(int(hex(resposta[3]),16)  + (int(hex(resposta[4]),16)<< 8) + (int(hex(resposta[5]),16) << 16) + (int(hex(resposta[6]),16) << 24))
    return resposta


if __name__ == "__main__":
    init_gpio()
    uart0 = uart.init_uart()
    # solicitarTemperatura(uart0)
    # requestFloat(solicitarTempInt2,uart0)
    # enviarCmd(uart0)
    
    while True:
        tempInt = solicitarTemperatura(uart0,solicitarTempInt)
        tempInt = int(hex(tempInt[3]),16) + int(hex(tempInt[4]),16) + int(hex(tempInt[5]),16) + int(hex(tempInt[6]),16)
        print(tempInt)
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
            print('cancelando...')
            uart.enviarCmd(uart0,algoritmoOff)