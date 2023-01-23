saida_medida = 0.0
sinal_de_controle = 0.0
referencia = 0.0
Kp = 0.0  
Ki = 0.0  
Kd = 0.0  
T = 1.0   
last_time = 0
erro_total = 0.0
erro_anterior = 0.0
sinal_de_controle_MAX = 100.0
sinal_de_controle_MIN = -100.0

def pid_configura_constantes(Kp_, Ki_, Kd_):
    global Kp, Ki, Kd
    Kp = Kp_
    Ki = Ki_
    Kd = Kd_

def pid_atualiza_referencia(referencia_):
    global referencia
    referencia = referencia_

def pid_controle(saida_medida_):
    global sinal_de_controle, erro_total, erro_anterior
    erro = referencia - saida_medida_

    erro_total += erro  

    if erro_total >= sinal_de_controle_MAX:
        erro_total = sinal_de_controle_MAX
    elif erro_total <= sinal_de_controle_MIN:
        erro_total = sinal_de_controle_MIN

    delta_error = erro - erro_anterior 

    sinal_de_controle = Kp*erro + (Ki*T)*erro_total + (Kd/T)*delta_error  

    if sinal_de_controle >= sinal_de_controle_MAX:
        sinal_de_controle = sinal_de_controle_MAX
    elif sinal_de_controle <= sinal_de_controle_MIN:
        sinal_de_controle = sinal_de_controle_MIN

    erro_anterior = erro
    return sinal_de_controle
