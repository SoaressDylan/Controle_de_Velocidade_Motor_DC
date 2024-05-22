# Controle de Velocidade Motor DC
 O Código está dividido entre Arduino, Python e Matlab.
# Arduíno:
   Em primeira instância, o calculo de furos(N) foi calculado, com N sendo apresentado a partir de uma medição com o auxílio de um tacômetro, chegamos em N = 400 , em sequência foi calculado seu alfa, através da seguinte relação:
V(rpm) =  ((cont/n)/(delta(T)*10^-6)) . 60 , onde n*delta(T) = alfa.
Assim , chegamos a relação de alfa = 60;
o Código foi implementado a partir da saída PWM (Modulação por Largura de Pulso), não foi necessário bibliotecas a serem incluídas.
# Python:
 Os Arquivos para a leitura e a obtenção de gráficos e sua Função de Transferência em Malha Aberta , foram realizadas pelo python, aqui foram necessária a inclusão de algumas bibliotecas como:
serial - para gerar um arquivo txt tivemos que conectar com a saída serial do arduino
os - biblioteca para gerar o txt.
keyboard  - Importa a biblioteca keyboard.
datetime - obter o horário para facilitar a descrição dos arquivos gerados.
time - o horário apresentado.

Para a modelagem da Resposta ao Degrau:
tkinter - Para o pop-up de escolher o txt com os dados
tkinter import filedialog  - Para o pop-up de escolher o txt com os dados
matplotlib.pyplot-  Para o plot dos gráficos
math- Para gerar as curvas modeladas
os - Para criar uma pasta com os gráficos
sympy - Para enccontrar a função de transferência
control - biblioteca de controle

# MatLab:
 A fim de obter o gráfico de Bode , foi utilizado as funções de bodeplot  com os dados já obtidos anteriormente.
