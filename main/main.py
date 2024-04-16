from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import sys
sys.path.append('identificacao')  # Adiciona o diretório 'funcoes' ao caminho de busca
from Smith import Smith
from Sundaresan import Sundaresan
import tkinter as tk
from tkinter import ttk
# Carrega o dataset 
mat=loadmat('dataset/Dataset_Grupo4.mat')

# Função chamada quando o botão é pressionado
def atualizar():
    Kp = float(entry_kp.get())
    Ti = float(entry_ti.get())
    Td = float(entry_td.get())
    
    # Calcular a resposta ao degrau
    calcular_resposta(Kp, Ti, Td)
    
# Criar a janela principal
root = tk.Tk()
root.title("Controle PID")

# Criar os campos de entrada e etiquetas para Kp, Ti e Td
label_kp = ttk.Label(root, text="Kp:")
label_kp.grid(row=0, column=0, padx=5, pady=5)
entry_kp = ttk.Entry(root)
entry_kp.grid(row=0, column=1, padx=5, pady=5)
entry_kp.insert(0, "1.0")  # Valor padrão

label_ti = ttk.Label(root, text="Ti:")
label_ti.grid(row=1, column=0, padx=5, pady=5)
entry_ti = ttk.Entry(root)
entry_ti.grid(row=1, column=1, padx=5, pady=5)
entry_ti.insert(0, "1.0")  # Valor padrão

label_td = ttk.Label(root, text="Td:")
label_td.grid(row=2, column=0, padx=5, pady=5)
entry_td = ttk.Entry(root)
entry_td.grid(row=2, column=1, padx=5, pady=5)
entry_td.insert(0, "1.0")  # Valor padrão

# Botão para calcular e atualizar a resposta ao degrau
button_atualizar = ttk.Button(root, text="Atualizar", command=atualizar)
button_atualizar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Mostrar a janela
root.mainloop()

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

n_pade = 6
( num_pade , den_pade ) = ctrl.pade ( theta , n_pade )
H_pade = ctrl.TransferFunction( num_pade , den_pade )

# Função de transferência do sistema com atraso
sys_atraso = ctrl.series(sys, H_pade)

# Modelo CHR com 20% de sobrevalor

Kp = 0.95 * tau / (k * theta)
Ti = 1.357 * tau
Td = 0.4730 * theta

# Criar a função de transferência do controlador PID
num_pid = [Kp * Td, Kp, Kp / Ti]
den_pid = [1, 0]
PID = ctrl.TransferFunction(num_pid, den_pid)
Cs = ctrl.series(PID, sys_atraso) # Série de PID e sistema com atraso

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

# Criar a função de transferência do controlador PID usando o metodo Cohen Coon
num_pidc = [Kpc * Tdc, Kpc * (1 + 0.5 * theta / tau), Kpc * theta / (2 * tau)] 
den_pidc = [1, 0]
PIDc = ctrl.TransferFunction(num_pidc, den_pidc)
Csc = ctrl.series(PIDc, sys_atraso) # Série de PID e sistema com atraso

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

# Função chamada quando o botão é pressionado
def atualizar():
    Kp = float(entry_kp.get())
    Ti = float(entry_ti.get())
    Td = float(entry_td.get())
    
    # Calcular a resposta ao degrau
    calcular_resposta(Kp, Ti, Td)
    
# Criar a janela principal
root = tk.Tk()
root.title("Controle PID")

# Criar os campos de entrada e etiquetas para Kp, Ti e Td
label_kp = ttk.Label(root, text="Kp:")
label_kp.grid(row=0, column=0, padx=5, pady=5)
entry_kp = ttk.Entry(root)
entry_kp.grid(row=0, column=1, padx=5, pady=5)
entry_kp.insert(0, "1.0")  # Valor padrão

label_ti = ttk.Label(root, text="Ti:")
label_ti.grid(row=1, column=0, padx=5, pady=5)
entry_ti = ttk.Entry(root)
entry_ti.grid(row=1, column=1, padx=5, pady=5)
entry_ti.insert(0, "1.0")  # Valor padrão

label_td = ttk.Label(root, text="Td:")
label_td.grid(row=2, column=0, padx=5, pady=5)
entry_td = ttk.Entry(root)
entry_td.grid(row=2, column=1, padx=5, pady=5)
entry_td.insert(0, "1.0")  # Valor padrão

# Botão para calcular e atualizar a resposta ao degrau
button_atualizar = ttk.Button(root, text="Atualizar", command=atualizar)
button_atualizar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Mostrar a janela
root.mainloop()