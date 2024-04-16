from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import sys
sys.path.append('identificacao')  # Adiciona o diretório 'funcoes' ao caminho de busca
from Smith import Smith
from Sundaresan import Sundaresan
# Carrega o dataset 
mat=loadmat('dataset/Dataset_Grupo4.mat')

# Variáveis
struct_degrau = mat.get('TARGET_DATA____ProjetoC213_Degrau')
degrau = struct_degrau[1].tolist()  # Converte para lista
tempo = struct_degrau[0].tolist()  # Converte para lista
struct_saida = mat.get('TARGET_DATA____ProjetoC213_Saida')
saida = struct_saida[1, :].tolist()  # Converte para lista

# Plotagem do grafico 
plot1=plt.plot(tempo,saida, label='Saída')
plot2=plt.plot(tempo,degrau,label='degrau de entrada')
plt.xlabel ( ' t [ s ] ')
plt.ylabel('Amplitude')
plt.legend(loc='lower right')

AmplitudeDegrau = np.mean(degrau)
valorInicial = saida[0]

# Obtendo parametros da função Smith
smith = Smith(np.mean(degrau), tempo, saida)
sys_smith = ctrl.TransferFunction([smith[0], 1], [smith[1], 1])
t, y = ctrl.step_response(sys_smith * AmplitudeDegrau, tempo)
saida_smith = y +  valorInicial
erro_smith = np.sqrt(np.mean((saida - saida_smith)**2))

# Obtendo parametros da função Sundaresan
sundaresan = Sundaresan(np.mean(degrau), tempo, saida)
sys_sundaresan = ctrl.TransferFunction([sundaresan[0], 1], [sundaresan[1], 1])
t, y = ctrl.step_response(sys_sundaresan * AmplitudeDegrau, tempo)
saida_sundaresan = y +  valorInicial
erro_sundaresan = np.sqrt(np.mean((saida - saida_sundaresan)**2))

if erro_smith < erro_sundaresan:
    k = smith[0]
    tau = smith[1]
    theta = smith[2]

else :
    k = sundaresan[0]
    tau = sundaresan[1]
    theta = sundaresan[2]
   

print("valor de k:", k, tau, theta)

# Criar o sistema de controle
sys = ctrl.TransferFunction([k], [tau, 1])

n_pade = 20
( num_pade , den_pade ) = ctrl.pade ( theta , n_pade )
H_pade = ctrl.TransferFunction( num_pade , den_pade )

# Modelo CHR com 20% de sobrevalor

Kp = 0.95 * tau / (k * theta)
Ti = 1.357 * tau
Td = 0.4730 * theta

# Criar a função de transferência do controlador PID
num_pid = [Kp * Td, Kp, Kp / Ti]
den_pid = [1, 0]
PID = ctrl.TransferFunction(num_pid, den_pid)

# Função de transferência do sistema com atraso
sys_atraso = ctrl.series(sys, H_pade)

# Série de PID e sistema com atraso
Cs = ctrl.series(PID, sys_atraso)

# Plotar a resposta ao degrau da malha fechada
plt.figure()
t, y = ctrl.step_response(ctrl.feedback(Cs, 1))
plt.plot(t, y, label = 'CHR20%')
plt.xlabel('Tempo')
plt.ylabel('Amplitude')
plt.title('Resposta ao degrau da malha fechada')
plt.legend(loc='lower right')
plt.grid(True)

# Modelo Cohen e Coon

Kpc = (tau / (k * theta)) * ((16 * tau + 30) / (12 * tau))
Tic = theta * ((32 + 6 * theta / tau) / (13 + (8 * theta / tau)))
Tdc = 4 * theta / (11 + 2 * theta / tau)

# Criar a função de transferência do controlador PID
num_pidc = [Kpc * Tdc, Kpc * (1 + 0.5 * theta / tau), Kpc * theta / (2 * tau)]
den_pidc = [1, 0]
PIDc = ctrl.TransferFunction(num_pidc, den_pidc)

# Série de PID e sistema com atraso
Csc = ctrl.series(PIDc, sys_atraso)

# Plotar a resposta ao degrau da malha fechada
plt.figure()
t_cc, y_cc = ctrl.step_response(ctrl.feedback(Csc, 1))
plot2 = plt.plot(t_cc, y_cc, label='Cohen-Coon')
plt.xlabel('Tempo')
plt.ylabel('Amplitude')
plt.title('Resposta ao degrau da malha fechada')
plt.legend(loc='lower right')
plt.grid(True)

plt.show()
