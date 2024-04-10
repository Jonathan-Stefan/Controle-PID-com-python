from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
mat=loadmat('dataset/Dataset_Grupo4.mat')

#Variáveis
struct_degrau = mat.get('TARGET_DATA____ProjetoC213_Degrau')
degrau=struct_degrau[1] #vetor linha
tempo=struct_degrau[0]#vetor linha
struct_saida=mat.get('TARGET_DATA____ProjetoC213_Saida')
saida=struct_saida[1,:]#vetor linha

# Plotagem do grafico 
plot1=plt.plot(tempo,saida, label='Saída')
plot2=plt.plot(tempo,degrau,label='degrau de entrada')
plt.xlabel ( ' t [ s ] ')
plt.ylabel('Amplitude')
plt.legend(loc="upper left")

#plt.grid ()
#plt.show()

# Usando o teorema do valor final, calculamos o valor de K
ValorFinal = saida[-1]
AmplitudeDegrau = degrau[-1]
k = ValorFinal/AmplitudeDegrau

print("valor de k:", k)

# Calculando o atraso
theta = 0
tau = 0
for i in range(len(saida)):
    if saida[i] != 0 and theta == 0:
        theta = tempo[i - 1]
    
    if saida[i] >= (0.9821 * ValorFinal):
        tau = (tempo[i] - theta) / 4
        break

print("valor do atraso de transporte:", theta)
print("valor da constante de tempo:", tau)

# Criar o sistema de controle
sys = ctrl.TransferFunction([k], [tau, 1])


# Definir o atraso de entrada no sistema
num, den = ctrl.pade(theta, 1)
sys_atraso = ctrl.TransferFunction(num, den) * sys


# Gerar a resposta ao degrau do sistema com atraso
tempo_resposta, resposta = ctrl.step_response(sys_atraso*AmplitudeDegrau)

# Plotar a resposta ao degrau
plt.figure()
plt.plot(tempo_resposta, resposta)

# Plotar os dados reais
plt.plot(tempo, saida, 'r--')

# Configurações do gráfico
plt.xlabel('tempo')
plt.ylabel('saida [°C]')
plt.legend(['Identificação', 'Real'], loc='upper right')
plt.title('Dados Reais vs Identificação')
plt.grid(True)

# Salvar o gráfico como PNG
#plt.savefig('RealXIdentificacao.png')

# Modelo CHR com 20% de sobrevalor

Kp = 0.95 * tau / (k * theta)
Ti = 1.357 * tau
Td = 0.4730 * theta

# Criando o controlador PID
num_pid = [Kp*Td, Kp, Kp/Ti]
den_pid = [1, 0]
PID = ctrl.TransferFunction(num_pid, den_pid)

# Criando o sistema em série
Cs = ctrl.series(PID, sys_atraso)

#plots
t = np . linspace (0 , 40 , 100)
# Plotando a resposta ao degrau do sistema em malha fechada
plt.figure()
ctrl.step_response(ctrl.feedback(Cs, 1))
plt.grid(True)
plt.xlabel('Tempo')
plt.ylabel('Resposta ao Degrau')
plt.title('Resposta ao Degrau do Sistema em Malha Fechada')

# Exibindo o gráfico
#plt.show()

print (Cs, PID, Kp, Ti, Td)