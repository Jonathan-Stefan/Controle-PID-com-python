import control as ctrl
import numpy as np
def Pid (Kp, Ti, Td):
    num_pid = [Kp * Td, Kp, Kp / Ti]
    den_pid = [1, 0]
    pid = ctrl.TransferFunction(num_pid, den_pid)

    return pid

def CHR20 (theta, tau, k):
    Kp = 0.95 * tau / (k * theta)
    Ti = 1.357 * tau
    Td = 0.4730 * theta
    return Kp, Ti, Td

def CohenCoon (theta, tau, k):
    Kp = (1.35 + 0.25 * (theta / tau)) * tau / (k * theta)
    Ti = (1.35 + 0.25 * (theta/tau)) / (0.54 + 0.33 * (theta / tau)) * theta
    Td = 0.5 * theta / (1.35 + 0.25*(theta/tau))
    
    return Kp, Ti, Td

def Calc_Param (t, y):
    # Calculando o máximo de pico, a amplitude total e o tempo de resposta
    maximo_pico = np.max(y)
    amplitude_total = np.abs(np.mean (y))  # valor da resposta ao degrau
    tempo_de_resposta = t[np.where(y >= 0.982 * np.mean(y))[0][0]]  # Tempo em que a resposta atinge 90% do valor final
    
    return maximo_pico, amplitude_total, tempo_de_resposta