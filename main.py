import RPi.GPIO as GPIO
import CRC
import serial
import time
import pid
import struct
import time
import uart



# Esp32 + Ler ou enviar + subCod + matricula + estado
solicitarTempInt = b'\x01\x23\xC1\x00\x08\x03\x01' # [7]
solicitaTempRef = b'\x01\x23\xC2\x00\x08\x03\x01' # [7]
usuario = b'\x01\x23\xC3\0\8\3\1' # [7]
enviaInt = b'\x01\x16\xD1\x00\x08\x03\x01' # [7]

ligarSistema = b'\x01\x16\xD3\x00\x08\x03\x01\1' # [8]
desligarSistema = b'\x01\x16\xD3\x00\x08\x03\x01\0' # [8]
algoritmoOn = b'\x01\x16\xD5\x00\x08\x03\x01\1' # [8]
algoritmoOff = b'\x01\x16\xD5\x00\x08\x03\x01\0' # [8]

ativaCurva = b'\x01\x16\xD4\x00\x08\x03\x01\1' # [8]
desativaCurva = b'\x01\x16\xD4\x00\x08\x03\x01\0' # [8]

enviaReferencia= b'\x01\x16\xD2\x00\x08\x03\x01' # [7]

#GPIO
pinResistor = 23
pinVentoinha = 24

def arqLog(tempAmb,tempInt,tempRef):
  with open('arquivoLog.csv', 'a+') as logfile:
    dateNow = time.strftime('%d-%m-%Y %H:%M:%S', time.gmtime())
    print(f'[{dateNow}] - tempAmbiente: {tempAmb:.1f}C° tempInt: {tempInt:.1f}C° tempRef: {tempRef:.1f}C°',file = logfile)


def pid_activation(pidRes, pinResistor, pinVentoinha):
    if pidRes > -40 and pidRes < 0:
        pidRes = -40
    print("PID: ", pidRes)
    pidResB = pidRes.to_bytes(4, 'little',signed=True)
    uart.enviaSinalControle(uart0,enviaInt, pidResB)  # Not sure what this function does, so it's not included in the Python version
    if pidRes < 0:
        GPIO.output(pinResistor, False)
        time.sleep(0.5)
        GPIO.output(pinVentoinha, True)
        time.sleep(0.5)
    elif pidRes > 0:
        GPIO.output(pinVentoinha, False)
        time.sleep(0.5)
        GPIO.output(pinResistor, True)
        time.sleep(0.5)


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




def init_gpio(pinResistor,pinVentoinha):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pinResistor, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pinVentoinha, GPIO.OUT, initial=GPIO.LOW)
    resistor = GPIO.PWM(pinResistor, 50)
    ventoinha = GPIO.PWM(pinVentoinha, 50)
    print("GPIO inicializado com sucesso!")
    return resistor, ventoinha



if __name__ == "__main__":
    ventoinha,resistor = init_gpio(pinVentoinha,pinResistor)
    uart0 = uart.init_uart()
    init_estados(uart0)
    aquecimento = False
    estadoModoManual = 0
    while True:

        #Ler temperatura interna e de Refererencia
        tempInt = uart.solicitarTemperatura(uart0,solicitarTempInt)
        print('TempInt: ' + str(tempInt))
        tempRef = uart.solicitarTemperatura(uart0,solicitaTempRef)
        print('TempREF: ' + str(tempRef))

        time.sleep(1)

        #Ler comando do usuario
        cmd = uart.lerCmd(uart0)
        cmd = str(hex(cmd[3]))
        print('Comando usuario: ' + cmd)

        if cmd == '0xa1':
            print("Ligar forno...")
            uart.enviarCmd(uart0,ligarSistema)
        elif cmd == '0xa2':
            print("Desligar forno...")
            uart.enviarCmd(uart0,desligarSistema)
        elif cmd == '0xa3':
            print('iniciando aquecimento...')
            uart.enviarCmd(uart0,algoritmoOn)
            aquecimento = True
                    
        
        elif cmd == '0xa4':
            print('desligando aquecimento...')
            uart.enviarCmd(uart0,algoritmoOff)
            aquecimento = False

        elif cmd == '0xa5':
            if estadoModoManual == 0:
                print('ativando modo manual / curva...')
                uart.enviarCmd(uart0,ativaCurva)
                tempInt = uart.solicitarTemperatura(uart0,solicitarTempInt)
                tempRef = uart.solicitarTemperatura(uart0,solicitaTempRef)
                pid.pid_atualiza_referencia(tempRef)
                # uart.enviaReferencia(uart0,enviaReferencia,tempRef)
                estadoModoManual = 1
            else: 
                print('Desativando modo manual / curva...')
                uart.enviarCmd(uart0,desativaCurva)
                estadoModoManual = 0
            
        
        elif aquecimento == True:
            
            tempInt = uart.solicitarTemperatura(uart0,solicitarTempInt)
            tempRef = uart.solicitarTemperatura(uart0,solicitaTempRef)
            pid.pid_atualiza_referencia(tempRef)
            controle = int(pid.pid_controle(tempInt))
            controleBytes = controle.to_bytes(4, 'little',signed=True) #signed True?
            uart.enviaSinalControle(uart0,enviaInt,controleBytes)
            # controle = int(pid.pid_controle(tempInt))
            pid_activation(controle, pinResistor, pinVentoinha)

        arqLog(25,tempInt,tempRef)
            
        # elif KeyboardInterrupt:
        #     uart.enviarCmd(uart0,desligarSistema)
        #     uart.enviarCmd(uart0,algoritmoOff)
        #     uart.enviarCmd(uart0,desativaCurva)
        #     GPIO.output(pinResistor, GPIO.LOW)
        #     GPIO.output(pinVentoinha, GPIO.LOW)
        #     print('Encerrando sistema!')
          