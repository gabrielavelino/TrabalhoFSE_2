# TrabalhoFSE_2 - Forno de solda

## Aluno
|Matrícula | Aluno |
| -- | -- |
| 18/0100831  |  Gabriel Avelino Freire |

## Objetivos

O trabalho tem como objetivo simular um sistema que representa o controle de um forno de soldagem de placas de circuitos. O aluno irá desenvolver um software para o controle desse sistema, com um resistor para aumentar o nível de calor e uma ventoinha para reduzir as altas temperaturas.

## Componentes do Sistema
O sistema é composto por:

- Ambiente fechado controlado com o resistor de potência e ventoinha;
- 01 Sensor DS18B20 (1-Wire) para a medição da temperatura interna (TI) do sistema;
- 01 Sensor BME280 (I2C) para a medição da temperatura externa (TE);
- 01 Conversor lógico bidirecional (3.3V / 5V);
- 01 Driver de potência para acionamento de duas cargas (L297);
- 01 ESP32;
- 01 Raspberry Pi 4;

## Linguagem e bibliotecas

**Linguagem**:
- Python3<br>

**Bibliotecas**:
- RPi.GPIO
- Serial
- Time
- Struct

## Arquitetura de arquivos

O projeto encontra-se na pasta principal divido em arquivos que são importados e modularizados para a main. Sendo esses arquivos:

### main.py
    - Arquivo onde a lógica do programa acontece, chama os demais arquivos e contrala o sistema do forno.

### CRC.py
    - Arquivo que foi disponibilizado pelo professor e reescrito para Python, para realizar o cálculo do CRC

### pid.py
    - Outro arquivo disponibilizado pelo professor que realiza o algoritmo do PID para voltar a porcentagem dos resistores e ventoinhas. Também transcrito para Python.

### uart.py
    - Arquivo onde possui as funções importadas pela main.py que realiza as comunicações necessárias com a ESP32.

## Como funciona

1 - Clonar esse repositorio

2 - Acessar a pasta raiz cd .\TrabalhoFSE_2

3 - Copiar os arquivos via scp: scp -P 13508 -r .\TrabalhoFSE_2 <user_>@<000.00.00.00>:~

4 - Acessar o ssh: ssh <user_>@<000.00.00.00> -p 13508

5 - Acessar a pasta dentro do ssh: cd .\TrabalhoFSE_2

6 - Rodar no terminal: python main.py

OBS: Para finalizar a aplicação execute **CONTROL_C**





