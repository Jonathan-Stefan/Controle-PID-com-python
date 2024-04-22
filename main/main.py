from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import sys
sys.path.append('identificacao')  # Adiciona o diretório 'identificacao' ao caminho de busca
from Smith import Smith
from Sundaresan import Sundaresan
import sys
sys.path.append('funcoes')  # Adiciona o diretório 'funcoes' ao caminho de busca
from Funcoes import Pid, CHR20, CohenCoon, Calc_Param
import tkinter as tk
from tkinter import ttk
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
   
# Criar o sistema de controle
sys = ctrl.TransferFunction([k], [tau, 1])

n_pade = 10
( num_pade , den_pade ) = ctrl.pade ( theta , n_pade )
H_pade = ctrl.TransferFunction( num_pade , den_pade )

# Função de transferência do sistema com atraso
sys_atraso = ctrl.series(sys, H_pade)

# Modelo CHR com 20% de sobrevalor
chr = CHR20 (theta, tau, k)

# Criar a função de transferência do controlador PID
PID = Pid (chr[0], chr[1], chr[2])
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

infoschr = Calc_Param(t, y)

print("Parametros para metodo CHR20%")
print("Máximo de pico", infoschr[0])
print("Amplitude total", infoschr[1])
print("Tempo de resposta", infoschr[2])

# Modelo Cohen e Coon
cohenCoon = CohenCoon(theta, tau, k)

# Criar a função de transferência do controlador PID usando o metodo Cohen Coon
PID = Pid (cohenCoon[0], cohenCoon[1], cohenCoon[2])
Cs = ctrl.series(PID, sys_atraso) # Série de PID e sistema com atraso

# Plotar a resposta ao degrau da malha fechada
plt.figure()
t, y = ctrl.step_response(ctrl.feedback(Cs, 1))
plt.plot(t, y, label='Cohen-Coon')
plt.xlabel('Tempo')
plt.ylabel('Amplitude')
plt.title('Resposta ao degrau da malha fechada')
plt.legend(loc='lower right')
plt.grid(True)

infosCc = Calc_Param(t, y)

print("\nParametros para metodo Cohen Coon")
print("Máximo de pico", infosCc[0])
print("Amplitude total", infosCc[1])
print("Tempo de resposta", infosCc[2])

plt.show()
    
# Criar a janela principal
root = tk.Tk()
root.title("Controle PID")

# Definir o tamanho da janela
largura_janela = 400
altura_janela = 300

# Obter a largura e a altura da tela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

# Calcular as coordenadas para colocar a janela no centro da tela
x_pos = largura_tela // 2 - largura_janela // 2
y_pos = altura_tela // 2 - altura_janela // 2

# Definir a geometria da janela
root.geometry(f'{largura_janela}x{altura_janela}+{x_pos}+{y_pos}')



# Botão para calcular e atualizar a resposta ao degrau
label_kp = ttk.Label(root, text="Kp:")
label_kp.grid(row=0, column=1, padx=5, pady=5)
entry_kp = tk.Entry(root)
entry_kp.grid(row=0, column=2)

entry_ti = tk.Entry(root)
label_kp = ttk.Label(root, text="Ti:")
label_kp.grid(row=1, column=1, padx=5, pady=5)
entry_ti.grid(row=1, column=2)

entry_td = tk.Entry(root)
label_kp = ttk.Label(root, text="Td:")
label_kp.grid(row=2, column=1, padx=5, pady=5)
entry_td.grid(row=2, column=2)

def calcular_resposta(Kp, Ti, Td):
    PID = Pid(Kp, Ti, Td)
    Cs = ctrl.series(PID, sys_atraso) # Série de PID e sistema com atraso
    t, y = ctrl.step_response(ctrl.feedback(Cs, 1))
    return t, y

def atualizar(Kp, Ti, Td):
    t, y = calcular_resposta(Kp, Ti, Td)
    # Calcular parâmetros para o método CHR20
    saida_chr20 = Calc_Param(t, y)
    print("Parâmetros para CHR20:")
    print("Máximo Pico:", saida_chr20[0])
    print("Amplitude Total:", saida_chr20[1])
    print("Tempo de Resposta:", saida_chr20[2])
    
    # Calcular parâmetros para o método CohenCoon
    saida_cohen_coon = Calc_Param(t, y)  # Seu código para calcular os parâmetros do CohenCoon aqui
    print("\nParâmetros para CohenCoon:")
    print("Máximo Pico:", saida_cohen_coon[0])
    print("Amplitude Total:", saida_cohen_coon[1])
    print("Tempo de Resposta:", saida_cohen_coon[2])

def atualizar_com_valores():
    # Obter valores de Kp, Ti e Td dos Entry widgets
    Kp = float(entry_kp.get())
    Ti = float(entry_ti.get())
    Td = float(entry_td.get())
    # Chamar atualizar() com os valores obtidos
    atualizar(Kp, Ti, Td)

# Botão CHR20
button_chr20 = ttk.Button(root, text="CHR20", command=atualizar_com_valores)
button_chr20.grid(row=0, column=0, padx=5, pady=5)

# Botão CohenCoon
button_cohen_coon = ttk.Button(root, text="CohenCoon", command=atualizar_com_valores)
button_cohen_coon.grid(row=1, column=0, padx=5, pady=5)



# Mostrar a janela
root.mainloop()