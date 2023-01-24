import serial
import time
import CRC
import struct

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

def lerCmd(uart0):
    dados = b'\x01\x23\xC3\x00\x08\x03\x01' # C3 Solicita comandos do usuário
    crc = CRC.calcula_CRC(dados,7)

    crc = crc.to_bytes(2,'little')
    dados = dados + crc
    
    uart0.write(dados)
    resposta = uart0.read(9)
    if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
        print('Error no Calculo CRC, tentando de novo...')
        lerCmd(uart0)
    time.sleep(1)
    
    return resposta

def enviarCmd(uart0,comando):
    dados = comando
    crc = CRC.calcula_CRC(dados,8)
    crc = crc.to_bytes(2,'little')
    dados = comando + crc
    # print("enviando...")
    uart0.write(dados)
    resposta = uart0.read(9)
    if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
        print('Error no Calculo CRC, tentando de novo...')
        enviarCmd(uart0,comando)
    # time.sleep(1)
    # return str(hex(resposta[3]))

def solicitarTemperatura(uart0,temp):
    
    message = temp # C1 = solicitar temperatura
    
    crc = CRC.calcula_CRC(message,7)
    crc = crc.to_bytes(2,'little')
    message = message + crc
    # print("escrevendo temperatura...")
    uart0.write(message)
    resposta = uart0.read(9)
    if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
        print('Error no Calculo CRC, tentando de novo...')
        solicitarTemperatura(uart0,temp)
    time.sleep(1)
    tempInt = [resposta[3],resposta[4],resposta[5],resposta[6]]
    temperatura = struct.unpack('f', bytearray(tempInt))[0]
    return temperatura

def enviaSinalControle(uart0,comando,controle):
    
    message = comando + controle
    crc = CRC.calcula_CRC(message,11)
    crc = crc.to_bytes(2,'little')
    message = message + crc
    uart0.write(message)
    # resposta = uart0.read(9)
    # if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
    #     print('Error no Calculo CRC, tentando de novo...')
    #     enviaSinalControle(controle)
    # time.sleep(1)
    # return resposta

def enviaReferencia(uart0,comando,tempRef):
        
        message = comando + tempRef
        crc = CRC.calcula_CRC(message,11)
        crc = crc.to_bytes(2,'little')
        message = message + crc
        uart0.write(message)
        resposta = uart0.read(5)
        if(CRC.verificaCRC(resposta, resposta[-2:]) == 'CRC-ERROR'):
            print('Error no Calculo CRC, tentando de novo...')
            enviaReferencia(uart0,comando,tempRef)
        # time.sleep(1)
        # return resposta

def enviaTempAmbiente(uart0,comando,tempAmb):
    
    message = comando + tempAmb # Envia a temperatura ambiente
    
    crc = CRC.calcula_CRC(message,11)
    crc = crc.to_bytes(2,'little')
    message = message + crc
    # print("escrevendo temperatura...")
    uart0.write(message)
