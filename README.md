# Controle-PID-com-python

## Importação das Bibliotecas:

scipy.io.loadmat, numpy, matplotlib.pyplot, controle, tkinter.

## Código para instalação das bibliotecas:
- pip install scipy
- pip install matplotlib
- pip install control
- pip install tk

Carrega o arquivo dataset do nosso grupo: 'Dataset_Grupo4.mat'.

São estraidos os dados: degrau, saída e tempo.

E nisso é plotado o grafico saida e degrau pelo tempo.





## Identificação do Sistema em Malha Aberta:

- Utiliza os métodos Smith e Sundaresan para identificar os parâmetros do sistema.
- Compara os resultados obtidos pelos métodos Smith e Sundaresan e escolhe qual deles apresentar um erro quadrático médio menor em relação aos dados experimentais.
- O Metódo escolhido foi o smith, portanto os parâmetros identificados utilizados por esse metodo são escolhidos (k, tau, theta).


## Projeto do Controlador PID em Malha Aberta:

- Define o sistema de controle.
- Gera um sistema de atraso usando a função ctrl.pade.
- Utiliza os métodos CHR20 e CohenCoon para projetar controladores PID.





## Implementação e Análise em Malha Fechada:

- Ao combinar o PID com o sistema com atrasado, cria um sistema de controle em malha fechada.
- Plota a resposta ao degrau da malha fechada usando o CHR20
- Imprimi os parametros máximo de pico, amplitude total e tempo de resposta para CHR20
- Faz o mesmo processo para o CohenCoon gerando os mesmos parâmetros.





## Interface grafica
- Cria uma janela principal usando Tkinter.
- Adiciona campos de entrada (Entry) para os valores de Kp, Ti, e Td.
- Cria botões para os métodos CHR20 e CohenCoon.

## Funções de Atualização e Cálculo:
- calcular_resposta: Calcula a resposta ao degrau com um conjunto específico de parâmetros Kp, Ti, e Td.
- atualizar: Atualiza e imprime parâmetros para os métodos CHR20 e CohenCoon com os parâmetros fornecidos.
- atualizar_com_valores: Obtém valores dos campos de entrada e chama a função atualizar.

## Executa a interface gráfica.

## Autores
[
Jonathan Stefan Covelo de Carvalho,
Marcelo Henrique Souza Abrantes,
Gabriel Bissacot Fraguas
]
